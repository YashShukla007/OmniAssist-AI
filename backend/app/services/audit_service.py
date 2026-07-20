from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.healthcare import AuditEvent


class AuditService:
    def record(
        self,
        db: Session,
        *,
        actor_id: int | None,
        action: str,
        entity_type: str,
        entity_id: int | None,
        details: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
        )
        db.add(event)
        return event


audit_service = AuditService()
