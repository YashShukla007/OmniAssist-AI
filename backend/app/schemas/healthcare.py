from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError


class PatientProfileUpdate(BaseModel):
    date_of_birth: date | None = None
    phone: str | None = Field(default=None, max_length=30)
    preferred_language: str | None = Field(default=None, max_length=30)
    emergency_contact: str | None = Field(default=None, max_length=100)


class PatientProfileResponse(PatientProfileUpdate):
    id: int
    user_id: int

    model_config = {"from_attributes": True}


class AppointmentCreate(BaseModel):
    department: str = Field(min_length=2, max_length=100)
    preferred_date: date
    preferred_time: str | None = Field(default=None, max_length=20)
    reason: str = Field(min_length=3, max_length=500)


class AppointmentResponse(BaseModel):
    id: int
    department: str
    doctor_name: str
    start_time: datetime
    end_time: datetime
    status: str
    reason: str


class AppointmentUpdate(BaseModel):
    action: str = Field(pattern="^(reschedule|cancel)$")
    preferred_date: date | None = None
    preferred_time: str | None = Field(default=None, max_length=20)


class DoctorCreate(BaseModel):
    department_id: int
    name: str = Field(min_length=3, max_length=100)


class AppointmentSlotCreate(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def end_must_follow_start(self) -> "AppointmentSlotCreate":
        if self.end_time <= self.start_time:
            raise PydanticCustomError("invalid_slot_range", "Slot end time must be after its start time.")
        return self


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str
    active: bool

    model_config = {"from_attributes": True}


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=3, max_length=1000)


class DoctorResponse(BaseModel):
    id: int
    department_id: int
    name: str
    active: bool

    model_config = {"from_attributes": True}


class AppointmentSlotResponse(BaseModel):
    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    status: str

    model_config = {"from_attributes": True}


class DocumentResponse(BaseModel):
    id: int
    document_type: str
    original_filename: str
    status: str
    duplicate: bool = False
    created_at: datetime


class ReminderResponse(BaseModel):
    id: int
    appointment_id: int | None
    reminder_type: str
    message: str
    scheduled_at: datetime
    status: str


class WorkflowRequest(BaseModel):
    request: str = Field(min_length=3, max_length=2000)
    document_ids: list[int] = Field(default_factory=list, max_length=10)


class WorkflowResponse(BaseModel):
    id: int
    status: str
    current_step: str
    summary: str
    state: dict[str, Any]
    escalation_id: int | None = None


class WorkflowListResponse(BaseModel):
    id: int
    request_text: str
    status: str
    current_step: str
    state: dict[str, Any]
    created_at: datetime


class StaffWorkflowListResponse(WorkflowListResponse):
    patient_id: int
    patient_name: str


class EscalationResponse(BaseModel):
    id: int
    workflow_run_id: int
    reason: str
    status: str
    created_at: datetime
    reviewed_at: datetime | None


class EscalationReview(BaseModel):
    approved: bool
    note: str = Field(min_length=3, max_length=500)


class AuditEventResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int | None
    details: dict[str, Any]
    created_at: datetime


class AnalyticsBucket(BaseModel):
    label: str
    value: int


class HealthcareAnalyticsResponse(BaseModel):
    patients: int
    appointments: int
    documents: int
    open_escalations: int
    workflows_completed: int
    appointment_statuses: list[AnalyticsBucket]
    workflow_statuses: list[AnalyticsBucket]
    appointments_by_day: list[AnalyticsBucket]
