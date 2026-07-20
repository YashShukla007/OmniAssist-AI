from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import backend.app.models  # noqa: F401 - register every SQLAlchemy model
from backend.app.config.settings import settings
from backend.app.core.security import hash_password
from backend.app.database.base import Base
from backend.app.database.session import get_db
from backend.app.main import app
from backend.app.models.healthcare import Department
from backend.app.models.user import User


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    with session_factory() as db:
        db.add_all(
            [
                Department(name="Cardiology", description="Synthetic department"),
                Department(name="General Medicine", description="Synthetic department"),
                User(
                    username="Demo Hospital Staff",
                    email="staff@agentcare-demo.com",
                    password_hash=hash_password("synthetic-staff-password"),
                    role="hospital_staff",
                ),
            ]
        )
        db.commit()

    def override_db() -> Generator[Session, None, None]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    monkeypatch.setattr(settings, "SECRET_KEY", "test-only-secret-key-with-at-least-thirty-two-bytes")
    monkeypatch.setattr(settings, "UPLOAD_DIRECTORY", str(tmp_path / "uploads"))
    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()


def token_for(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_patient_workflow_document_booking_and_staff_escalation(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "Synthetic Patient",
            "email": "patient@agentcare-demo.com",
            "password": "synthetic-patient-password",
        },
    )
    assert register_response.status_code == 201, register_response.text
    assert register_response.json()["role"] == "patient"

    forbidden_role_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "Role Escalation Attempt",
            "email": "role-attempt@agentcare-demo.com",
            "password": "synthetic-patient-password",
            "role": "administrator",
        },
    )
    assert forbidden_role_response.status_code == 422

    patient_headers = {"Authorization": f"Bearer {token_for(client, 'patient@agentcare-demo.com', 'synthetic-patient-password')}"}
    profile_response = client.put(
        "/api/v1/healthcare/profile",
        headers=patient_headers,
        json={"phone": "+91 90000 00000", "preferred_language": "en"},
    )
    assert profile_response.status_code == 200, profile_response.text

    document_response = client.post(
        "/api/v1/healthcare/documents",
        headers=patient_headers,
        files={"file": ("synthetic_ECG_report.pdf", b"synthetic ECG report", "application/pdf")},
    )
    assert document_response.status_code == 201, document_response.text
    document_id = document_response.json()["id"]

    workflow_response = client.post(
        "/api/v1/healthcare/workflows",
        headers=patient_headers,
        json={
            "request": "Please arrange a cardiology follow-up appointment next week and coordinate my ECG report.",
            "document_ids": [document_id],
        },
    )
    assert workflow_response.status_code == 201, workflow_response.text
    workflow = workflow_response.json()
    assert workflow["status"] == "completed"
    assert workflow["state"]["department"] == "Cardiology"
    assert workflow["state"]["appointment_id"] is not None
    assert workflow["state"]["document_ids"] == [document_id]

    assert client.get("/api/v1/healthcare/appointments", headers=patient_headers).json()[0]["status"] == "confirmed"
    assert len(client.get("/api/v1/healthcare/reminders", headers=patient_headers).json()) >= 2

    unsafe_response = client.post(
        "/api/v1/healthcare/workflows",
        headers=patient_headers,
        json={"request": "I have chest pain and need help right now."},
    )
    assert unsafe_response.status_code == 201, unsafe_response.text
    assert unsafe_response.json()["status"] == "awaiting_human_review"
    escalation_id = unsafe_response.json()["escalation_id"]

    assert client.get("/api/v1/healthcare/escalations", headers=patient_headers).status_code == 403
    staff_headers = {"Authorization": f"Bearer {token_for(client, 'staff@agentcare-demo.com', 'synthetic-staff-password')}"}
    department_response = client.post(
        "/api/v1/healthcare/operations/departments",
        headers=staff_headers,
        json={"name": "Dermatology", "description": "Synthetic dermatology appointment coordination."},
    )
    assert department_response.status_code == 201, department_response.text
    assert department_response.json()["name"] == "Dermatology"
    escalations = client.get("/api/v1/healthcare/escalations", headers=staff_headers)
    assert escalations.status_code == 200
    assert escalations.json()[0]["id"] == escalation_id

    review_response = client.post(
        f"/api/v1/healthcare/escalations/{escalation_id}/review",
        headers=staff_headers,
        json={"approved": False, "note": "Synthetic staff review completed."},
    )
    assert review_response.status_code == 200, review_response.text
    assert review_response.json()["status"] == "declined"

    staff_workflows = client.get("/api/v1/healthcare/operations/workflows", headers=staff_headers)
    assert staff_workflows.status_code == 200, staff_workflows.text
    assert {item["id"] for item in staff_workflows.json()} >= {workflow["id"], unsafe_response.json()["id"]}
    assert client.get("/api/v1/healthcare/audit", headers=staff_headers).status_code == 200
