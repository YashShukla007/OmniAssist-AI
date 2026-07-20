from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.agents.routing_agent import routing_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.core.authorization import require_roles
from backend.app.database.base import Base
from backend.app.models.healthcare import Department
from backend.app.models.user import User
from backend.app.services.document_service import document_service


def test_routing_agent_routes_ecg_request_to_cardiology() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    db.add_all([
        Department(name="Cardiology", description="Synthetic department"),
        Department(name="General Medicine", description="Synthetic department"),
        Department(name="Dermatology", description="Synthetic department"),
    ])
    db.commit()
    decision = routing_agent.route(db, "Please arrange a cardiology follow-up and attach my ECG.")

    assert decision.department == "Cardiology"
    assert decision.confidence > 0.8
    dynamic_decision = routing_agent.route(db, "Please arrange a Dermatology appointment.")
    assert dynamic_decision.department == "Dermatology"
    db.close()


def test_safety_agent_escalates_sensitive_medical_language() -> None:
    decision = safety_agent.assess("I have chest pain and need help right now.")

    assert decision.should_escalate is True
    assert decision.reason is not None


def test_safety_agent_escalates_medication_requests() -> None:
    decision = safety_agent.assess("Which medication should I take for this?")

    assert decision.should_escalate is True


def test_document_classifier_uses_filename_metadata() -> None:
    assert document_service.classify_filename("old_ECG_report.pdf") == "ecg_report"
    assert document_service.classify_filename("blood_lab_results.pdf") == "blood_report"


def test_staff_permission_is_enforced_in_backend_code() -> None:
    patient = User(username="synthetic", email="synthetic@example.test", password_hash="not-a-real-password", role="patient")
    permission_check = require_roles("hospital_staff", "administrator")

    try:
        permission_check(current_user=patient)
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("Patient role unexpectedly received staff access")


def test_document_only_request_does_not_require_appointment_booking() -> None:
    from backend.app.agents.appointment_agent import appointment_agent

    assert appointment_agent.requires_appointment("Please classify my attached ECG report.") is False
    assert appointment_agent.requires_appointment("Please book a cardiology appointment.") is True
