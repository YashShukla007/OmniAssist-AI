from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.healthcare import Department


class DepartmentService:
    """Database-backed department lookup tool used by the routing agent."""

    default_departments = (
        ("Cardiology", "Administrative coordination for heart-care appointments."),
        ("General Medicine", "Administrative coordination for general outpatient visits."),
    )

    def ensure_default_catalogue(self, db: Session) -> None:
        existing_names = {
            name.casefold()
            for name in db.scalars(select(Department.name))
        }
        for name, description in self.default_departments:
            if name.casefold() not in existing_names:
                db.add(Department(name=name, description=description, active=True))
        db.flush()

    def active_departments(self, db: Session) -> list[Department]:
        self.ensure_default_catalogue(db)
        departments = list(
            db.scalars(
                select(Department)
                .where(Department.active.is_(True))
                .order_by(Department.name)
            )
        )
        if not departments:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No active departments are available for administrative routing.",
            )
        return departments


department_service = DepartmentService()
