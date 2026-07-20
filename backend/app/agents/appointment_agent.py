from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy.orm import Session

from backend.app.models.healthcare import Appointment, PatientProfile
from backend.app.schemas.healthcare import AppointmentCreate
from backend.app.services.appointment_service import appointment_service


@dataclass(frozen=True)
class AppointmentDecision:
    appointment: Appointment


class AppointmentAgent:
    """Uses the availability/booking tool to reserve a persisted administrative slot."""

    system_prompt = "You are the Appointment Agent. Check availability, avoid conflicts, and book only administrative appointments."

    appointment_terms = ("appointment", "book", "schedule", "visit", "follow-up", "follow up", "reschedule", "cancel")

    def requires_appointment(self, request_text: str) -> bool:
        return any(term in request_text.lower() for term in self.appointment_terms)

    def book(self, db: Session, patient: PatientProfile, department: str, request_text: str) -> AppointmentDecision:
        preferred_date = date.today() + timedelta(days=7)
        appointment = appointment_service.create_for_patient(db, patient, AppointmentCreate(department=department, preferred_date=preferred_date, reason=request_text[:500]))
        return AppointmentDecision(appointment=appointment)


appointment_agent = AppointmentAgent()
