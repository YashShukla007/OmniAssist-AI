from datetime import timedelta

from sqlalchemy.orm import Session

from backend.app.models.healthcare import Appointment, PatientProfile, Reminder


class FollowUpAgent:
    """Creates persisted appointment reminders and follow-up tasks."""

    system_prompt = "You are the Follow-up Agent. Create non-clinical reminders and keep the patient informed about administrative next steps."

    def schedule(self, db: Session, patient: PatientProfile, appointment: Appointment) -> Reminder:
        reminder = Reminder(patient_id=patient.id, appointment_id=appointment.id, reminder_type="follow_up", message="Confirm any required documents before your appointment.", scheduled_at=appointment.slot.start_time - timedelta(hours=24))
        db.add(reminder)
        db.flush()
        return reminder


follow_up_agent = FollowUpAgent()
