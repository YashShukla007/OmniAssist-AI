from mimetypes import guess_type

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_user
from backend.app.core.authorization import require_roles
from backend.app.database.session import get_db
from backend.app.models.healthcare import AuditEvent, PatientProfile
from backend.app.models.user import User
from backend.app.schemas.healthcare import AppointmentCreate, AppointmentResponse, AppointmentSlotCreate, AppointmentSlotResponse, AppointmentUpdate, AuditEventResponse, DepartmentCreate, DepartmentResponse, DoctorCreate, DoctorResponse, DocumentResponse, EscalationResponse, EscalationReview, HealthcareAnalyticsResponse, PatientProfileResponse, PatientProfileUpdate, ReminderResponse, StaffWorkflowListResponse, WorkflowListResponse, WorkflowRequest, WorkflowResponse
from backend.app.services.appointment_service import appointment_service
from backend.app.services.audit_service import audit_service
from backend.app.services.document_service import document_service
from backend.app.services.healthcare_analytics_service import healthcare_analytics_service
from backend.app.services.hospital_operations_service import hospital_operations_service
from backend.app.services.patient_service import patient_service
from backend.app.services.reminder_service import reminder_service
from backend.app.services.workflow_service import workflow_service


router = APIRouter(prefix="/healthcare", tags=["Healthcare coordination"])


@router.get("/profile", response_model=PatientProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> PatientProfile:
    profile = patient_service.get_or_create_profile(db, current_user)
    db.commit()
    db.refresh(profile)
    return profile


@router.put("/profile", response_model=PatientProfileResponse)
def update_profile(update: PatientProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> PatientProfile:
    profile = patient_service.update_profile(db, patient_service.get_or_create_profile(db, current_user), update)
    audit_service.record(db, actor_id=current_user.id, action="patient_profile.updated", entity_type="patient_profile", entity_id=profile.id)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/appointments", response_model=list[AppointmentResponse])
def list_appointments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[AppointmentResponse]:
    profile = patient_service.get_or_create_profile(db, current_user)
    return [appointment_service.as_response(item) for item in appointment_service.list_for_patient(db, profile)]


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
def create_appointment(request: AppointmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AppointmentResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    appointment = appointment_service.create_for_patient(db, profile, request)
    audit_service.record(db, actor_id=current_user.id, action="appointment.created", entity_type="appointment", entity_id=appointment.id)
    db.commit()
    appointment = appointment_service.list_for_patient(db, profile)[0]
    return appointment_service.as_response(appointment)


@router.patch("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, update: AppointmentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> AppointmentResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    appointment = appointment_service.update_for_patient(db, profile, appointment_id, update)
    action = "appointment.rescheduled" if update.action == "reschedule" else "appointment.cancelled"
    audit_service.record(db, actor_id=current_user.id, action=action, entity_type="appointment", entity_id=appointment.id)
    db.commit()
    appointment = db.scalar(select(type(appointment)).where(type(appointment).id == appointment.id))
    return appointment_service.as_response(appointment)


@router.get("/documents", response_model=list[DocumentResponse])
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[DocumentResponse]:
    profile = patient_service.get_or_create_profile(db, current_user)
    return [document_service.as_response(item) for item in document_service.list_for_patient(db, profile)]


@router.get("/documents/{document_id}/content")
def get_document_content(
    document_id: int,
    download: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    document, stored_path = document_service.get_file_for_patient(db, profile, document_id)
    response = FileResponse(
        path=stored_path,
        media_type=guess_type(document.original_filename)[0] or "application/octet-stream",
        filename=document.original_filename,
    )
    if not download:
        response.headers["Content-Disposition"] = "inline"
    return response


@router.post("/documents", response_model=DocumentResponse, status_code=201)
async def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> DocumentResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    document, duplicate = await document_service.store_upload(db, profile, file)
    audit_service.record(db, actor_id=current_user.id, action="document.duplicate_detected" if duplicate else "document.uploaded", entity_type="patient_document", entity_id=document.id, details={"filename": document.original_filename})
    db.commit()
    return document_service.as_response(document, duplicate)


@router.put("/documents/{document_id}", response_model=DocumentResponse)
async def replace_document(document_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> DocumentResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    document = await document_service.replace_for_patient(db, profile, document_id, file)
    audit_service.record(db, actor_id=current_user.id, action="document.replaced", entity_type="patient_document", entity_id=document.id, details={"filename": document.original_filename})
    db.commit()
    db.refresh(document)
    return document_service.as_response(document)


@router.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    profile = patient_service.get_or_create_profile(db, current_user)
    document_service.delete_for_patient(db, profile, document_id)
    audit_service.record(db, actor_id=current_user.id, action="document.deleted", entity_type="patient_document", entity_id=document_id)
    db.commit()


@router.get("/reminders", response_model=list[ReminderResponse])
def list_reminders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ReminderResponse]:
    profile = patient_service.get_or_create_profile(db, current_user)
    return [reminder_service.as_response(item) for item in reminder_service.list_for_patient(db, profile)]


@router.post("/reminders/{reminder_id}/toggle", response_model=ReminderResponse)
def toggle_reminder(reminder_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ReminderResponse:
    profile = patient_service.get_or_create_profile(db, current_user)
    reminder = reminder_service.toggle_for_patient(db, profile, reminder_id)
    audit_service.record(db, actor_id=current_user.id, action="reminder.toggled", entity_type="reminder", entity_id=reminder.id)
    db.commit()
    return reminder_service.as_response(reminder)


@router.post("/workflows", response_model=WorkflowResponse, status_code=201)
async def create_workflow(request: WorkflowRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> WorkflowResponse:
    return await workflow_service.run(db, current_user, request)


@router.get("/workflows", response_model=list[WorkflowListResponse])
def list_workflows(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[WorkflowListResponse]:
    profile = patient_service.get_or_create_profile(db, current_user)
    return [WorkflowListResponse(id=item.id, request_text=item.request_text, status=item.status, current_step=item.current_step, state=item.state, created_at=item.created_at) for item in workflow_service.list_for_patient(db, profile)]


@router.get("/escalations", response_model=list[EscalationResponse])
def list_escalations(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> list[EscalationResponse]:
    return [EscalationResponse(id=item.id, workflow_run_id=item.workflow_run_id, reason=item.reason, status=item.status, created_at=item.created_at, reviewed_at=item.reviewed_at) for item in workflow_service.list_escalations(db)]


@router.get("/operations/workflows", response_model=list[StaffWorkflowListResponse])
def list_all_workflows(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> list[StaffWorkflowListResponse]:
    workflows = workflow_service.list_all(db)
    return [
        StaffWorkflowListResponse(
            id=item.id,
            request_text=item.request_text,
            status=item.status,
            current_step=item.current_step,
            state=item.state,
            created_at=item.created_at,
            patient_id=item.patient_id,
            patient_name=item.patient.user.username,
        )
        for item in workflows
    ]


@router.post("/escalations/{escalation_id}/review", response_model=EscalationResponse)
def review_escalation(escalation_id: int, review: EscalationReview, current_user: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> EscalationResponse:
    escalation = workflow_service.review_escalation(db, current_user, escalation_id, review)
    return EscalationResponse(id=escalation.id, workflow_run_id=escalation.workflow_run_id, reason=escalation.reason, status=escalation.status, created_at=escalation.created_at, reviewed_at=escalation.reviewed_at)


@router.get("/audit", response_model=list[AuditEventResponse])
def list_audit_events(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> list[AuditEventResponse]:
    events = db.scalars(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(100))
    return [AuditEventResponse(id=event.id, action=event.action, entity_type=event.entity_type, entity_id=event.entity_id, details=event.details, created_at=event.created_at) for event in events]


@router.get("/analytics", response_model=HealthcareAnalyticsResponse)
def get_analytics(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> HealthcareAnalyticsResponse:
    return healthcare_analytics_service.overview(db)


@router.get("/operations/departments", response_model=list[DepartmentResponse])
def list_departments(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> list[DepartmentResponse]:
    return hospital_operations_service.list_departments(db)


@router.post("/operations/departments", response_model=DepartmentResponse, status_code=201)
def create_department(request: DepartmentCreate, current_user: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> DepartmentResponse:
    department = hospital_operations_service.create_department(db, request)
    audit_service.record(db, actor_id=current_user.id, action="department.created", entity_type="department", entity_id=department.id)
    db.commit()
    db.refresh(department)
    return department


@router.get("/operations/doctors", response_model=list[DoctorResponse])
def list_doctors(_: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> list[DoctorResponse]:
    return hospital_operations_service.list_doctors(db)


@router.post("/operations/doctors", response_model=DoctorResponse, status_code=201)
def create_doctor(request: DoctorCreate, current_user: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> DoctorResponse:
    doctor = hospital_operations_service.create_doctor(db, request)
    audit_service.record(db, actor_id=current_user.id, action="doctor.created", entity_type="doctor", entity_id=doctor.id)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.post("/operations/slots", response_model=AppointmentSlotResponse, status_code=201)
def create_slot(request: AppointmentSlotCreate, current_user: User = Depends(require_roles("hospital_staff", "administrator")), db: Session = Depends(get_db)) -> AppointmentSlotResponse:
    slot = hospital_operations_service.create_slot(db, request)
    audit_service.record(db, actor_id=current_user.id, action="appointment_slot.created", entity_type="appointment_slot", entity_id=slot.id)
    db.commit()
    db.refresh(slot)
    return slot
