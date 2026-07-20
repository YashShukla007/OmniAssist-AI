from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.config.settings import settings
from backend.app.models.healthcare import PatientDocument, PatientProfile
from backend.app.schemas.healthcare import DocumentResponse


class DocumentService:
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg"}

    def classify_filename(self, filename: str) -> str:
        normalised = filename.lower()
        if "ecg" in normalised or "ekg" in normalised:
            return "ecg_report"
        if "blood" in normalised or "lab" in normalised:
            return "blood_report"
        if "prescription" in normalised:
            return "prescription"
        return "medical_document"

    async def store_upload(
        self,
        db: Session,
        patient: PatientProfile,
        upload: UploadFile,
    ) -> tuple[PatientDocument, bool]:
        filename = Path(upload.filename or "upload").name
        suffix = Path(filename).suffix.lower()
        if suffix not in self.allowed_extensions:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF, PNG, JPG, and JPEG documents can be uploaded.")

        content = await upload.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="The uploaded document is empty.")
        if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="The document exceeds the 10 MB upload limit.")

        checksum = sha256(content).hexdigest()
        duplicate = db.scalar(select(PatientDocument).where(PatientDocument.patient_id == patient.id, PatientDocument.checksum == checksum))
        if duplicate is not None:
            return duplicate, True

        upload_directory = Path(settings.UPLOAD_DIRECTORY) / str(patient.id)
        upload_directory.mkdir(parents=True, exist_ok=True)
        storage_path = upload_directory / f"{uuid4().hex}{suffix}"
        storage_path.write_bytes(content)

        document = PatientDocument(patient_id=patient.id, document_type=self.classify_filename(filename), storage_reference=str(storage_path), original_filename=filename, checksum=checksum, status="received")
        db.add(document)
        db.flush()
        return document, False

    def list_for_patient(self, db: Session, patient: PatientProfile) -> list[PatientDocument]:
        return list(db.scalars(select(PatientDocument).where(PatientDocument.patient_id == patient.id).order_by(PatientDocument.created_at.desc())))

    def get_file_for_patient(
        self,
        db: Session,
        patient: PatientProfile,
        document_id: int,
    ) -> tuple[PatientDocument, Path]:
        document = db.scalar(
            select(PatientDocument).where(
                PatientDocument.id == document_id,
                PatientDocument.patient_id == patient.id,
            )
        )
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

        stored_path = Path(document.storage_reference).resolve()
        upload_root = Path(settings.UPLOAD_DIRECTORY).resolve()
        if upload_root not in stored_path.parents or not stored_path.is_file():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The stored document file is unavailable.")
        return document, stored_path

    def delete_for_patient(self, db: Session, patient: PatientProfile, document_id: int) -> None:
        document = db.scalar(select(PatientDocument).where(PatientDocument.id == document_id, PatientDocument.patient_id == patient.id))
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
        self._remove_storage_file(document.storage_reference)
        db.delete(document)
        db.flush()

    async def replace_for_patient(self, db: Session, patient: PatientProfile, document_id: int, upload: UploadFile) -> PatientDocument:
        document = db.scalar(select(PatientDocument).where(PatientDocument.id == document_id, PatientDocument.patient_id == patient.id))
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
        filename = Path(upload.filename or "upload").name
        suffix = Path(filename).suffix.lower()
        if suffix not in self.allowed_extensions:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF, PNG, JPG, and JPEG documents can be uploaded.")
        content = await upload.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="The uploaded document is empty.")
        if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="The document exceeds the 10 MB upload limit.")
        checksum = sha256(content).hexdigest()
        duplicate = db.scalar(select(PatientDocument).where(PatientDocument.patient_id == patient.id, PatientDocument.checksum == checksum, PatientDocument.id != document.id))
        if duplicate is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An identical document is already stored for this patient.")
        upload_directory = Path(settings.UPLOAD_DIRECTORY) / str(patient.id)
        upload_directory.mkdir(parents=True, exist_ok=True)
        storage_path = upload_directory / f"{uuid4().hex}{suffix}"
        storage_path.write_bytes(content)
        self._remove_storage_file(document.storage_reference)
        document.storage_reference = str(storage_path)
        document.original_filename = filename
        document.document_type = self.classify_filename(filename)
        document.checksum = checksum
        document.status = "received"
        db.flush()
        return document

    @staticmethod
    def _remove_storage_file(storage_reference: str) -> None:
        upload_root = Path(settings.UPLOAD_DIRECTORY).resolve()
        stored_path = Path(storage_reference).resolve()
        if upload_root not in stored_path.parents:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Document storage reference is invalid.")
        if stored_path.exists():
            stored_path.unlink()

    def as_response(self, document: PatientDocument, duplicate: bool = False) -> DocumentResponse:
        return DocumentResponse(id=document.id, document_type=document.document_type, original_filename=document.original_filename, status=document.status, duplicate=duplicate, created_at=document.created_at)


document_service = DocumentService()
