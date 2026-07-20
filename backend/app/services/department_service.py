from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.healthcare import Department


class DepartmentService:
    """Database-backed department lookup tool used by the routing agent."""

    def active_departments(self, db: Session) -> list[Department]:
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
