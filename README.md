# AgentCare — Agentic Patient Administration and Care Coordination

AgentCare is the healthcare workflow in OmniAssist AI. It coordinates administrative patient journeys: registration, department routing, appointment booking, document collection, reminders, follow-ups, audit history, and human escalation.

> Safety boundary: AgentCare is not a diagnosis, treatment, prescription, dosage, or emergency-response system. Requests that indicate an emergency, medication, treatment, dosage, diagnosis, or other sensitive medical decision are persisted as a human-review escalation instead of being handled autonomously.

## Challenge requirements covered

| Requirement | Implementation |
| --- | --- |
| Python backend and SQL persistence | FastAPI, SQLAlchemy, Alembic, SQLite by default or PostgreSQL through `DATABASE_URL` |
| Distinct agents | Coordinator, Safety & Escalation, Department Routing, Appointment, Document, and Follow-up agents |
| LLM integration | Coordinator calls the configured OpenRouter client to produce a bounded administrative plan; provider/model fallback handles transient model failures |
| Functional tools | SQL-backed patient profile, department catalogue, slot lookup and booking, document storage/classification, reminder creation, escalation review, and audit logging |
| Patient UI | React dashboard for profile, documents, workflows, appointments, reminders, and the chat workflow |
| Staff UI | Protected request view, escalations/approval, audit log, analytics, doctor creation, and slot creation |
| Backend RBAC | FastAPI `require_roles` dependency protects staff-only workflow, escalation, audit, analytics, and catalogue endpoints |
| Human oversight | Safety agent creates `Escalation` records that staff must review; the patient cannot self-approve |

## Architecture

```text
React patient/staff UI
        │
        ▼
FastAPI /api/v1/healthcare routes + JWT/RBAC
        │
        ▼
Coordinator Agent ── optional OpenRouter LLM administrative plan
        │
        ├── Safety & Escalation Agent ──► Escalation + AuditEvent
        ├── Department Routing Agent ───► active Department catalogue tool
        ├── Appointment Agent ──────────► doctor/slot/conflict/booking tools
        ├── Document Agent ─────────────► upload/checksum/classification tools
        └── Follow-up Agent ────────────► persisted Reminder tools
        │
        ▼
SQLAlchemy → SQLite/PostgreSQL
  User, PatientProfile, Department, Doctor, AppointmentSlot, Appointment,
  PatientDocument, WorkflowRun, Reminder, Escalation, AuditEvent
```

The workflow response is derived from persisted appointment and document records. It does not present an LLM diagnosis as a result.

## Local setup (Windows PowerShell)

Prerequisites: Python 3.11+, [uv](https://docs.astral.sh/uv/), Node.js 20+, and npm.

1. Create your local configuration. Do not commit `backend/.env`.

   ```powershell
   Copy-Item backend\.env.example backend\.env
   ```

   Open `backend/.env` and set a unique `SECRET_KEY` of at least 32 characters. SQLite already works locally with the supplied `DATABASE_URL`. To enable the Coordinator’s LLM plan, also set `OPENROUTER_API_KEY` and a comma-separated `OPENROUTER_MODELS` value.

2. Install Python dependencies and create the local environment.

   ```powershell
   uv sync
   ```

3. Apply the persistent database schema.

   ```powershell
   uv run alembic upgrade head
   uv run alembic current
   ```

4. Provision a synthetic Hospital Staff account for the protected demo views. Public registration creates patient accounts only; the command securely prompts for a local demo password.

   ```powershell
   uv run python -m backend.scripts.seed_demo --role hospital_staff --username "Demo Hospital Staff" --email staff@agentcare-demo.com
   ```

   To make a local administrator instead, use `--role administrator` and a different email.

5. Start the API in one terminal.

   ```powershell
   uv run uvicorn backend.app.main:app --reload
   ```

6. Start the React app in another terminal.

   ```powershell
   Set-Location frontend
   npm.cmd install
   npm.cmd run dev
   ```

   Open the Vite URL shown in the terminal (normally `http://localhost:5173`).

## Complete demo script

1. Register a synthetic **Patient** in the UI and sign in.
2. In **Patients**, save a synthetic profile. Do not use real patient information.
3. In **Chat Assistant**, attach a synthetic PDF named `ECG_Report.pdf` and submit:

   ```text
   I need a cardiology follow-up appointment next week and want to attach my old ECG report.
   ```

   This creates a `WorkflowRun`, validates the department against the SQL catalogue, creates/chooses an appointment slot, persists the document checksum/classification, creates appointment and follow-up reminders, and writes audit events.
4. Check **Workflows**, **Appointments**, **Documents**, and **Reminders**. Try appointment reschedule and cancel to verify slot release and reminder updates.
5. Submit `I have chest pain and need help right now.` The Safety Agent will not book it; it creates an escalation for human review.
6. Sign out, then log in as `staff@agentcare-demo.com` with the password chosen in step 4. In **Workflows**, review all persisted patient requests. In **Escalations**, approve or decline the case with a note. Review **Audit Logs** and **Analytics**; create a department, doctor, and future slot in **Analytics**.

## Verification commands

Run these from the repository root before a submission:

```powershell
uv run pytest backend/tests -q
uv run python -m compileall backend
uv run alembic upgrade head
```

Run these from `frontend`:

```powershell
npm.cmd run lint
npm.cmd run build
```

The test suite includes an end-to-end API test covering patient registration, profile update, document upload, multi-agent workflow, appointment/reminder persistence, safety escalation, staff review, staff request visibility, RBAC denial, and audit access.

## Configuration and data handling

`backend/.env.example` contains only safe placeholders. Keep real API keys, the GitHub `SUBMISSION_TOKEN`, and all real patient data out of Git. Uploads are stored under `backend/uploads/`, which is ignored. The repository uses only synthetic data in tests and demos.

For PostgreSQL, set `DATABASE_URL` to a SQLAlchemy PostgreSQL connection string in `backend/.env`, then rerun `uv run alembic upgrade head`. Do not use the public registration route to provision staff privileges; use the local operator command above or an equivalent deployment-controlled provisioning process.

## CI / challenge submission

The included `.github/workflows/agentcare-checks.yml` runs the challenge checker after you add `SUBMISSION_TOKEN` to the repository’s GitHub Actions secrets. Before pushing, make sure the repository is public, your default branch contains the application source, `backend/.env` is not tracked, and the verification commands above pass.
