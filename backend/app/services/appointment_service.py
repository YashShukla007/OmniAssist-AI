from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.healthcare import Appointment, AppointmentSlot, Department, Doctor, PatientProfile, Reminder
from backend.app.schemas.healthcare import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from backend.app.services.department_service import department_service


class AppointmentService:
    def _department(self, db: Session, department_name: str) -> Department:
        department_service.ensure_default_catalogue(db)
        department = db.scalar(select(Department).where(Department.name.ilike(department_name), Department.active.is_(True)))
        if department is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="That department is not available for administrative booking.")
        return department

    def _ensure_doctor(self, db: Session, department: Department) -> Doctor:
        doctor = db.scalar(select(Doctor).where(Doctor.department_id == department.id, Doctor.active.is_(True)).order_by(Doctor.id))
        if doctor is not None:
            return doctor
        doctor = Doctor(department_id=department.id, name=f"Dr. {department.name} Coordinator")
        db.add(doctor)
        db.flush()
        return doctor

    def _ensure_slots(self, db: Session, doctor: Doctor, preferred_date: date) -> None:
        existing = db.scalar(select(AppointmentSlot.id).where(AppointmentSlot.doctor_id == doctor.id, AppointmentSlot.start_time >= datetime.combine(preferred_date, time.min), AppointmentSlot.start_time < datetime.combine(preferred_date + timedelta(days=1), time.min)))
        if existing is not None:
            return
        for hour in (10, 14, 16):
            start = datetime.combine(preferred_date, time(hour=hour))
            db.add(AppointmentSlot(doctor_id=doctor.id, start_time=start, end_time=start + timedelta(minutes=30)))
        db.flush()

    def _preferred_time(self, value: str | None) -> time | None:
        if not value:
            return None
        for pattern in ("%I:%M %p", "%H:%M"):
            try:
                return datetime.strptime(value.strip().upper(), pattern).time()
            except ValueError:
                continue
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Preferred time must use HH:MM AM/PM or 24-hour HH:MM format.",
        )

    def _available_slot(self, db: Session, patient: PatientProfile, doctor: Doctor, preferred_date: date, preferred_time: str | None) -> AppointmentSlot:
        day_start = datetime.combine(preferred_date, time.min)
        day_end = day_start + timedelta(days=1)
        requested_time = self._preferred_time(preferred_time)
        slots = list(db.scalars(select(AppointmentSlot).where(AppointmentSlot.doctor_id == doctor.id, AppointmentSlot.status == "available", AppointmentSlot.start_time >= day_start, AppointmentSlot.start_time < day_end).order_by(AppointmentSlot.start_time)))
        if requested_time:
            slots.sort(key=lambda item: abs((item.start_time.time().hour * 60 + item.start_time.time().minute) - (requested_time.hour * 60 + requested_time.minute)))
        for slot in slots:
            patient_conflict = db.scalar(
                select(Appointment.id)
                .join(AppointmentSlot, Appointment.slot_id == AppointmentSlot.id)
                .where(
                    Appointment.patient_id == patient.id,
                    Appointment.status == "confirmed",
                    AppointmentSlot.start_time < slot.end_time,
                    AppointmentSlot.end_time > slot.start_time,
                )
            )
            if patient_conflict is None:
                return slot
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No conflict-free appointment slot is available on that date.")

    def create_for_patient(self, db: Session, patient: PatientProfile, request: AppointmentCreate) -> Appointment:
        if request.preferred_date < date.today():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Appointments cannot be requested for a past date.")
        department = self._department(db, request.department)
        doctor = self._ensure_doctor(db, department)
        self._ensure_slots(db, doctor, request.preferred_date)
        slot = self._available_slot(db, patient, doctor, request.preferred_date, request.preferred_time)
        slot.status = "booked"
        appointment = Appointment(patient_id=patient.id, doctor_id=doctor.id, slot_id=slot.id, status="confirmed", reason=request.reason)
        db.add(appointment)
        db.flush()
        reminder_time = max(datetime.utcnow() + timedelta(minutes=1), slot.start_time - timedelta(days=1))
        db.add(Reminder(patient_id=patient.id, appointment_id=appointment.id, reminder_type="appointment", message=f"Upcoming {department.name} appointment with {doctor.name}.", scheduled_at=reminder_time))
        db.flush()
        return appointment

    def update_for_patient(self, db: Session, patient: PatientProfile, appointment_id: int, update: AppointmentUpdate) -> Appointment:
        appointment = db.scalar(select(Appointment).options(joinedload(Appointment.doctor).joinedload(Doctor.department), joinedload(Appointment.slot)).where(Appointment.id == appointment_id, Appointment.patient_id == patient.id))
        if appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
        if appointment.status != "confirmed":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only confirmed appointments can be changed.")
        if update.action == "cancel":
            appointment.status = "cancelled"
            appointment.slot.status = "available"
            for reminder in appointment.reminders:
                reminder.status = "cancelled"
            db.flush()
            return appointment
        if update.preferred_date is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="A preferred date is required to reschedule an appointment.")
        if update.preferred_date < date.today():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Appointments cannot be rescheduled to a past date.")
        self._ensure_slots(db, appointment.doctor, update.preferred_date)
        new_slot = self._available_slot(db, patient, appointment.doctor, update.preferred_date, update.preferred_time)
        appointment.slot.status = "available"
        new_slot.status = "booked"
        appointment.slot = new_slot
        reminder_time = max(datetime.utcnow() + timedelta(minutes=1), new_slot.start_time - timedelta(days=1))
        for reminder in appointment.reminders:
            if reminder.status == "scheduled":
                reminder.scheduled_at = reminder_time
        db.flush()
        return appointment

    def list_for_patient(self, db: Session, patient: PatientProfile) -> list[Appointment]:
        return list(db.scalars(select(Appointment).options(joinedload(Appointment.doctor).joinedload(Doctor.department), joinedload(Appointment.slot)).where(Appointment.patient_id == patient.id).order_by(Appointment.created_at.desc())))

    def as_response(self, appointment: Appointment) -> AppointmentResponse:
        return AppointmentResponse(id=appointment.id, department=appointment.doctor.department.name, doctor_name=appointment.doctor.name, start_time=appointment.slot.start_time, end_time=appointment.slot.end_time, status=appointment.status, reason=appointment.reason)


appointment_service = AppointmentService()
