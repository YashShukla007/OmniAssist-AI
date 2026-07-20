from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.healthcare import Appointment, AppointmentSlot, Escalation, PatientDocument, PatientProfile, WorkflowRun
from backend.app.schemas.healthcare import AnalyticsBucket, HealthcareAnalyticsResponse


class HealthcareAnalyticsService:
    """Builds staff-only dashboard metrics from persisted coordination records."""

    def overview(self, db: Session) -> HealthcareAnalyticsResponse:
        patients = int(db.scalar(select(func.count(PatientProfile.id))) or 0)
        appointments = int(db.scalar(select(func.count(Appointment.id))) or 0)
        documents = int(db.scalar(select(func.count(PatientDocument.id))) or 0)
        open_escalations = int(db.scalar(select(func.count(Escalation.id)).where(Escalation.status == "open")) or 0)
        workflows_completed = int(db.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.status == "completed")) or 0)

        appointment_statuses = self._buckets(db.execute(select(Appointment.status, func.count(Appointment.id)).group_by(Appointment.status)).all())
        workflow_statuses = self._buckets(db.execute(select(WorkflowRun.status, func.count(WorkflowRun.id)).group_by(WorkflowRun.status)).all())
        today = datetime.utcnow().date()
        starts = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
        daily_counts = dict(
            db.execute(
                select(func.date(AppointmentSlot.start_time), func.count(Appointment.id))
                .join(Appointment, Appointment.slot_id == AppointmentSlot.id)
                .where(AppointmentSlot.start_time >= datetime.combine(starts[0], datetime.min.time()))
                .group_by(func.date(AppointmentSlot.start_time))
            ).all()
        )
        appointments_by_day = [AnalyticsBucket(label=item.strftime("%a"), value=int(daily_counts.get(item, daily_counts.get(item.isoformat(), 0)))) for item in starts]
        return HealthcareAnalyticsResponse(
            patients=patients,
            appointments=appointments,
            documents=documents,
            open_escalations=open_escalations,
            workflows_completed=workflows_completed,
            appointment_statuses=appointment_statuses,
            workflow_statuses=workflow_statuses,
            appointments_by_day=appointments_by_day,
        )

    @staticmethod
    def _buckets(rows: list[tuple[str, int]]) -> list[AnalyticsBucket]:
        return [AnalyticsBucket(label=str(label).replace("_", " "), value=int(value)) for label, value in rows]


healthcare_analytics_service = HealthcareAnalyticsService()
