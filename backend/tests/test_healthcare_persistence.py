from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import backend.app.models  # noqa: F401 - imports every mapped table before metadata creation
from backend.app.database.base import Base
from backend.app.models.healthcare import Department, PatientProfile
from backend.app.models.user import User
from backend.app.schemas.healthcare import AppointmentCreate, AppointmentSlotCreate, AppointmentUpdate, DepartmentCreate, DoctorCreate
from backend.app.services.appointment_service import appointment_service
from backend.app.services.healthcare_analytics_service import healthcare_analytics_service
from backend.app.services.hospital_operations_service import hospital_operations_service


def database_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_booking_prefers_requested_time_and_releases_slot_on_cancel() -> None:
    db = database_session()
    try:
        user = User(username="synthetic-patient", email="synthetic@example.test", password_hash="not-a-real-password")
        department = Department(name="Cardiology", description="Synthetic department")
        db.add_all([user, department])
        db.commit()
        patient = PatientProfile(user_id=user.id)
        db.add(patient)
        db.commit()

        appointment = appointment_service.create_for_patient(
            db,
            patient,
            AppointmentCreate(department="Cardiology", preferred_date=date.today() + timedelta(days=2), preferred_time="3:55 PM", reason="Synthetic administrative booking"),
        )
        assert appointment.slot.start_time.hour == 16
        original_slot_id = appointment.slot_id

        rescheduled = appointment_service.update_for_patient(
            db,
            patient,
            appointment.id,
            AppointmentUpdate(action="reschedule", preferred_date=date.today() + timedelta(days=3), preferred_time="2:10 PM"),
        )
        assert rescheduled.slot.start_time.hour == 14
        assert rescheduled.slot_id != original_slot_id

        cancelled = appointment_service.update_for_patient(db, patient, appointment.id, AppointmentUpdate(action="cancel"))
        assert cancelled.status == "cancelled"
        assert cancelled.slot.status == "available"
    finally:
        db.close()


def test_analytics_reads_persisted_records() -> None:
    db = database_session()
    try:
        user = User(username="analytics-patient", email="analytics@example.test", password_hash="not-a-real-password")
        department = Department(name="General Medicine", description="Synthetic department")
        db.add_all([user, department])
        db.commit()
        patient = PatientProfile(user_id=user.id)
        db.add(patient)
        db.commit()
        appointment_service.create_for_patient(
            db,
            patient,
            AppointmentCreate(department="General Medicine", preferred_date=date.today() + timedelta(days=1), reason="Synthetic analytics booking"),
        )
        db.commit()

        analytics = healthcare_analytics_service.overview(db)
        assert analytics.patients == 1
        assert analytics.appointments == 1
        assert any(bucket.label == "confirmed" and bucket.value == 1 for bucket in analytics.appointment_statuses)
    finally:
        db.close()


def test_past_appointment_date_is_rejected() -> None:
    db = database_session()
    try:
        user = User(username="date-patient", email="date@example.test", password_hash="not-a-real-password")
        department = Department(name="Cardiology", description="Synthetic department")
        db.add_all([user, department])
        db.commit()
        patient = PatientProfile(user_id=user.id)
        db.add(patient)
        db.commit()

        try:
            appointment_service.create_for_patient(
                db,
                patient,
                AppointmentCreate(department="Cardiology", preferred_date=date.today() - timedelta(days=1), reason="Synthetic invalid booking"),
            )
        except HTTPException as error:
            assert error.status_code == 422
        else:
            raise AssertionError("Past appointment request unexpectedly succeeded")
    finally:
        db.close()


def test_invalid_preferred_time_is_rejected() -> None:
    db = database_session()
    try:
        user = User(username="time-patient", email="time@example.test", password_hash="not-a-real-password")
        department = Department(name="Cardiology", description="Synthetic department")
        db.add_all([user, department])
        db.commit()
        patient = PatientProfile(user_id=user.id)
        db.add(patient)
        db.commit()

        try:
            appointment_service.create_for_patient(
                db,
                patient,
                AppointmentCreate(
                    department="Cardiology",
                    preferred_date=date.today() + timedelta(days=2),
                    preferred_time="late afternoon",
                    reason="Synthetic invalid booking",
                ),
            )
        except HTTPException as error:
            assert error.status_code == 422
        else:
            raise AssertionError("Invalid appointment time unexpectedly succeeded")
    finally:
        db.close()


def test_staff_catalogue_creates_doctor_and_future_slot() -> None:
    db = database_session()
    try:
        department = Department(name="Cardiology", description="Synthetic department")
        db.add(department)
        db.commit()

        doctor = hospital_operations_service.create_doctor(db, DoctorCreate(department_id=department.id, name="Dr. Synthetic"))
        slot = hospital_operations_service.create_slot(
            db,
            AppointmentSlotCreate(
                doctor_id=doctor.id,
                start_time=datetime.now() + timedelta(days=2),
                end_time=datetime.now() + timedelta(days=2, minutes=30),
            ),
        )
        assert doctor.department_id == department.id
        assert slot.doctor_id == doctor.id
        assert slot.status == "available"
    finally:
        db.close()


def test_staff_catalogue_creates_department() -> None:
    db = database_session()
    try:
        department = hospital_operations_service.create_department(
            db,
            DepartmentCreate(name="Dermatology", description="Synthetic skin-care appointment coordination"),
        )

        assert department.name == "Dermatology"
        assert department.active is True
    finally:
        db.close()
