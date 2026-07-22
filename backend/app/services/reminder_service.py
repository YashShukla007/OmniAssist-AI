from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.healthcare import PatientProfile, Reminder
from backend.app.schemas.healthcare import ReminderResponse


class ReminderService:
    def list_for_patient(self, db: Session, patient: PatientProfile) -> list[Reminder]:
        return list(db.scalars(select(Reminder).where(Reminder.patient_id == patient.id).order_by(Reminder.scheduled_at.asc(), Reminder.id.asc())))

    def toggle_for_patient(self, db: Session, patient: PatientProfile, reminder_id: int) -> Reminder:
        reminder = db.scalar(select(Reminder).where(Reminder.id == reminder_id, Reminder.patient_id == patient.id))
        if reminder is None:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found.")
        reminder.status = "completed" if reminder.status != "completed" else "scheduled"
        db.flush()
        return reminder

    def as_response(self, reminder: Reminder) -> ReminderResponse:
        return ReminderResponse(id=reminder.id, appointment_id=reminder.appointment_id, reminder_type=reminder.reminder_type, message=reminder.message, scheduled_at=reminder.scheduled_at, status=reminder.status)


reminder_service = ReminderService()
