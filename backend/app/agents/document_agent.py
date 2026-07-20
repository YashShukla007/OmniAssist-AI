from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.healthcare import PatientDocument, PatientProfile


@dataclass(frozen=True)
class DocumentDecision:
    document_ids: list[int]
    missing_document_types: list[str]


class DocumentAgent:
    """Coordinates persisted patient document metadata and identifies missing requested files."""

    system_prompt = "You are the Document Agent. Classify uploaded administrative document metadata and identify duplicates or missing requested documents."

    def coordinate(self, db: Session, patient: PatientProfile, request_text: str, document_ids: list[int]) -> DocumentDecision:
        document_query = select(PatientDocument).where(
            PatientDocument.patient_id == patient.id,
        )
        if document_ids:
            document_query = document_query.where(PatientDocument.id.in_(document_ids))
        documents = list(db.scalars(document_query))
        requested_types = []
        normalised = request_text.lower()
        if "ecg" in normalised or "ekg" in normalised:
            requested_types.append("ecg_report")
        if "blood" in normalised:
            requested_types.append("blood_report")
        present_types = {document.document_type for document in documents}
        return DocumentDecision(document_ids=[document.id for document in documents], missing_document_types=[document_type for document_type in requested_types if document_type not in present_types])


document_agent = DocumentAgent()
