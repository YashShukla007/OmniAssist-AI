from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.agents.appointment_agent import appointment_agent
from backend.app.agents.coordinator_agent import coordinator_agent
from backend.app.agents.document_agent import document_agent
from backend.app.agents.follow_up_agent import follow_up_agent
from backend.app.agents.routing_agent import routing_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.models.healthcare import Escalation, PatientProfile, WorkflowRun
from backend.app.models.user import User
from backend.app.schemas.healthcare import EscalationReview, WorkflowRequest, WorkflowResponse
from backend.app.services.audit_service import audit_service
from backend.app.services.appointment_service import appointment_service
from backend.app.services.patient_service import patient_service


class WorkflowService:
    async def run(self, db: Session, user: User, request: WorkflowRequest) -> WorkflowResponse:
        patient = patient_service.get_or_create_profile(db, user)
        workflow = WorkflowRun(patient_id=patient.id, request_text=request.request, current_step="coordinator", state={})
        db.add(workflow)
        db.flush()
        audit_service.record(db, actor_id=user.id, action="workflow.created", entity_type="workflow_run", entity_id=workflow.id)

        safety = safety_agent.assess(request.request)
        if safety.should_escalate:
            escalation = Escalation(workflow_run_id=workflow.id, reason=safety.reason or "Human review required.")
            workflow.current_step = "human_review"
            workflow.status = "awaiting_human_review"
            workflow.state = {"safety": "escalated"}
            db.add(escalation)
            audit_service.record(db, actor_id=user.id, action="workflow.escalated", entity_type="workflow_run", entity_id=workflow.id, details={"reason": escalation.reason})
            db.commit()
            db.refresh(escalation)
            return WorkflowResponse(id=workflow.id, status=workflow.status, current_step=workflow.current_step, summary="Your request has been sent to hospital staff for safe human review. OmniAssist does not provide medical advice.", state=workflow.state, escalation_id=escalation.id)

        plan = await coordinator_agent.plan(request.request)
        route = routing_agent.route(db, request.request)
        workflow.current_step = "appointment_booking"
        workflow.state = {"plan": plan.administrative_summary, "department": route.department, "routing_confidence": route.confidence}
        audit_service.record(db, actor_id=user.id, action="workflow.routed", entity_type="workflow_run", entity_id=workflow.id, details={"department": route.department})

        document_decision = document_agent.coordinate(db, patient, request.request, request.document_ids)
        appointment = None
        if appointment_agent.requires_appointment(request.request):
            appointment_decision = appointment_agent.book(db, patient, route.department, request.request)
            appointment = appointment_decision.appointment
            follow_up_agent.schedule(db, patient, appointment)

        workflow.current_step = "completed"
        workflow.status = "completed"
        workflow.state = {**workflow.state, "appointment_id": appointment.id if appointment else None, "document_ids": document_decision.document_ids, "missing_document_types": document_decision.missing_document_types}
        audit_service.record(db, actor_id=user.id, action="workflow.completed", entity_type="workflow_run", entity_id=workflow.id, details={"appointment_id": appointment.id if appointment else None, "documents": document_decision.document_ids})
        db.commit()
        db.refresh(workflow)
        missing_text = f" Please upload: {', '.join(document_decision.missing_document_types)}." if document_decision.missing_document_types else ""
        if appointment is None:
            document_text = "Attached documents were coordinated." if document_decision.document_ids else "Your administrative request was recorded."
            return WorkflowResponse(id=workflow.id, status=workflow.status, current_step=workflow.current_step, summary=f"{document_text}{missing_text}", state=workflow.state)
        appointment = db.scalar(select(type(appointment)).where(type(appointment).id == appointment.id))
        appointment_response = appointment_service.as_response(appointment)
        return WorkflowResponse(id=workflow.id, status=workflow.status, current_step=workflow.current_step, summary=f"{appointment_response.department} appointment booked with {appointment_response.doctor_name} for {appointment_response.start_time:%d %b %Y %I:%M %p}.{missing_text}", state=workflow.state)

    def list_for_patient(self, db: Session, patient: PatientProfile) -> list[WorkflowRun]:
        return list(db.scalars(select(WorkflowRun).where(WorkflowRun.patient_id == patient.id).order_by(WorkflowRun.created_at.desc())))

    def list_all(self, db: Session) -> list[WorkflowRun]:
        return list(
            db.scalars(
                select(WorkflowRun)
                .join(PatientProfile)
                .order_by(WorkflowRun.created_at.desc())
            )
        )

    def list_escalations(self, db: Session) -> list[Escalation]:
        return list(db.scalars(select(Escalation).order_by(Escalation.created_at.desc())))

    def review_escalation(self, db: Session, reviewer: User, escalation_id: int, review: EscalationReview) -> Escalation:
        escalation = db.get(Escalation, escalation_id)
        if escalation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escalation not found.")
        escalation.status = "approved" if review.approved else "declined"
        escalation.reviewed_by = reviewer.id
        escalation.reviewed_at = datetime.utcnow()
        escalation.workflow.status = "completed" if review.approved else "closed"
        escalation.workflow.current_step = "staff_reviewed"
        audit_service.record(db, actor_id=reviewer.id, action="escalation.reviewed", entity_type="escalation", entity_id=escalation.id, details={"approved": review.approved, "note": review.note})
        db.commit()
        db.refresh(escalation)
        return escalation


workflow_service = WorkflowService()
