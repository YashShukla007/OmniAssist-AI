from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models.healthcare import AppointmentSlot, Department, Doctor
from backend.app.schemas.healthcare import AppointmentSlotCreate, DepartmentCreate, DoctorCreate


class HospitalOperationsService:
    """Staff-facing management of the persisted department, doctor, and slot catalogue."""

    def list_departments(self, db: Session) -> list[Department]:
        return list(db.scalars(select(Department).order_by(Department.name)))

    def create_department(self, db: Session, request: DepartmentCreate) -> Department:
        existing = db.scalar(select(Department).where(Department.name.ilike(request.name.strip())))
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A department with that name already exists.")
        department = Department(name=request.name.strip(), description=request.description.strip())
        db.add(department)
        db.flush()
        return department

    def list_doctors(self, db: Session) -> list[Doctor]:
        return list(db.scalars(select(Doctor).order_by(Doctor.name)))

    def create_doctor(self, db: Session, request: DoctorCreate) -> Doctor:
        department = db.get(Department, request.department_id)
        if department is None or not department.active:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="The selected department is not active.")
        duplicate = db.scalar(select(Doctor).where(Doctor.department_id == request.department_id, Doctor.name.ilike(request.name)))
        if duplicate is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A doctor with that name already exists in the selected department.")
        doctor = Doctor(department_id=request.department_id, name=request.name.strip())
        db.add(doctor)
        db.flush()
        return doctor

    def create_slot(self, db: Session, request: AppointmentSlotCreate) -> AppointmentSlot:
        if request.start_time <= datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Appointment slots must start in the future.")
        doctor = db.get(Doctor, request.doctor_id)
        if doctor is None or not doctor.active:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="The selected doctor is not active.")
        slot = AppointmentSlot(doctor_id=request.doctor_id, start_time=request.start_time, end_time=request.end_time)
        db.add(slot)
        try:
            db.flush()
        except IntegrityError as error:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That doctor already has a slot at this start time.") from error
        return slot


hospital_operations_service = HospitalOperationsService()
