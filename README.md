# AgentCare — Agentic AI for Patient Administration & Care Coordination

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![React](https://img.shields.io/badge/React-18+-cyan.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**AgentCare** (powered by **OmniAssist AI**) is an agentic healthcare administration platform that coordinates a patient's non-clinical journey — from registration and department routing to appointment booking, document collection, reminders, follow-ups, and staff escalations.

> ⚠️ **Safety & Clinical Boundary Notice:** AgentCare is strictly an administrative coordination system. It does **not** provide autonomous medical diagnosis, prescriptions, treatment advice, or dosage changes. Any request involving acute emergencies, medical advice, or prescriptions is automatically blocked by the Safety Agent and escalated for human staff review.

---

## 🌟 Key Features & Problem Statement Coverage

| Feature Category | Implementation Details |
| :--- | :--- |
| **Agent Architecture** | 6 distinct agent roles: Coordinator, Safety & Escalation, Department Routing, Appointment, Document, and Follow-up agents. |
| **Flexible LLM Provider Support** | Supports **Local LLMs (Ollama)** for 100% offline local execution, as well as **Cloud LLM APIs** (OpenRouter, OpenAI, Groq, Anthropic) via environment config. |
| **Functional Tools** | SQL-backed patient profile, department catalogue, slot lookup & booking, document storage/classification, reminder creation, escalation review, and audit logging. |
| **Patient Experience** | Interactive React UI for profiles, document management, appointment booking/rescheduling/cancellation, reminders, and AI chat assistant. |
| **Staff & Admin Portal** | Protected operations dashboard for request review, escalation approvals, audit log inspection, real-time analytics, and schedule management. |
| **Backend RBAC** | Strict role-based access control enforced via FastAPI dependencies (`require_roles`). Patients cannot access staff views or approve escalations. |
| **Audit & Governance** | Immutable `AuditEvent` logging for all actions taken by users and agents, maintaining a complete compliance trail. |
| **Data Persistence** | Full relational database schema with SQLite (local default) or PostgreSQL support via SQLAlchemy & Alembic migrations. |

---

## 🤖 LLM Provider Configuration: Local LLM vs Cloud API

AgentCare is designed to work with **any LLM provider**. You can run it completely **offline with a Local LLM** (e.g. via Ollama) or connect it to a **Cloud LLM API** (OpenRouter, Groq, OpenAI).

### Option A: Local LLM (Ollama - 100% Offline & Private)

1. **Install Ollama** from [ollama.com](https://ollama.com).
2. **Pull your preferred model** in terminal:
   ```bash
   # Download Llama 3 (or mistral / qwen / phi3)
   ollama pull llama3
   ```
3. **Configure `backend/.env`**:
   ```ini
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   OLLAMA_TIMEOUT_SECONDS=120
   ```

---

### Option B: Cloud LLM API (OpenRouter / Groq / OpenAI)

To use high-speed cloud LLMs (Gemini, Llama-3-70b, GPT-4o, Claude):

1. **Get an API Key** from [OpenRouter.ai](https://openrouter.ai) or your cloud provider.
2. **Configure `backend/.env`**:
   ```ini
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODELS=google/gemini-2.5-flash,meta-llama/llama-3.3-70b-instruct:free
   ```

*(Note: If no LLM key is configured, AgentCare seamlessly falls back to structured rule-based coordinator planning so all system functionality remains fully operational).*

---

## 🏗️ Agentic System Architecture

```text
               ┌──────────────────────────────────────────────┐
               │    React Web Application (Patient / Staff)   │
               └──────────────────────┬───────────────────────┘
                                      │ REST API / JWT
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  FastAPI Backend (RBAC Enforced Endpoints)   │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │              Coordinator Agent               │
               │   (Manages WorkflowRun state & LLM Plan)     │
               └──┬───────┬──────────┬───────────┬──────────┬─┘
                  │       │          │           │          │
    ┌─────────────┘       │          │           │          └──────────────┐
    ▼                     ▼          ▼           ▼                         ▼
┌──────────────┐ ┌─────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────────────┐
│ Safety &     │ │ Department  │ │ Appointment│ │ Document   │ │ Follow-up & Reminder │
│ Escalation   │ │ Routing     │ │ Agent      │ │ Agent      │ │ Agent                │
│ Agent        │ │ Agent       │ │            │ │            │ │                      │
└──────┬───────┘ └──────┬──────┘ └─────┬──────┘ └─────┬──────┘ └──────────┬───────────┘
       │                │              │              │                   │
       ▼                ▼              ▼              ▼                   ▼
 ┌──────────┐     ┌───────────┐  ┌───────────┐  ┌───────────┐       ┌───────────┐
 │Escalation│     │Department │  │Doctor /   │  │Patient    │       │  Reminder │
 │& Audit   │     │Catalogue  │  │Slot Tool  │  │Doc Tool   │       │  Service  │
 └────┬─────┘     └─────┬─────┘  └─────┬─────┘  └─────┬─────┘       └─────┬─────┘
      │                 │              │              │                   │
      └─────────────────┴──────────────┼──────────────┴───────────────────┘
                                       ▼
                       ┌──────────────────────────────┐
                       │ SQLAlchemy ORM & Relational  │
                       │ Database (SQLite/PostgreSQL) │
                       └──────────────────────────────┘
```

### The 6 Agent Roles

1. **Coordinator Agent** (`backend/app/agents/coordinator_agent.py`): Tracks the execution plan, invokes specialized agents step-by-step, manages state transitions in `WorkflowRun`, and generates structural responses.
2. **Department Routing Agent** (`backend/app/agents/routing_agent.py`): Parses user intent, maps requests to active clinical departments (e.g., Cardiology, Orthopedics, Neurology), and handles unknown department requests gracefully.
3. **Appointment Agent** (`backend/app/agents/appointment_agent.py`): Searches available doctor slots, verifies schedule conflicts, books new appointments, and processes rescheduling or cancellations.
4. **Document Agent** (`backend/app/agents/document_agent.py`): Ingests uploaded files (ECG reports, blood tests, insurance IDs), computes MD5 checksums for duplicate detection, classifies document types, and links files to patient profiles.
5. **Follow-up Agent** (`backend/app/agents/follow_up_agent.py`): Schedules automated reminders and follow-up tasks tied to appointments and care milestones.
6. **Safety & Escalation Agent** (`backend/app/agents/safety_agent.py`): Evaluates input safety against clinical boundary rules. If emergency symptoms (e.g., severe chest pain) or diagnostic inquiries are detected, it halts autonomous processing and creates a human `Escalation` ticket.

---

## 🗄️ Database Schema Overview

The database uses SQLAlchemy with 11 primary persistent entities:

* `User`: Authentication record, password hash, and assigned role (`patient`, `hospital_staff`, `administrator`).
* `PatientProfile`: Demographic details, emergency contact info, and medical preferences.
* `Department`: Clinical specialty catalog (Cardiology, Orthopedics, General Medicine, etc.).
* `Doctor`: Medical practitioner details linked to a department.
* `AppointmentSlot`: Time windows for doctor availability (`scheduled`, `booked`).
* `Appointment`: Patient booking records linked to doctor, slot, and status.
* `PatientDocument`: Uploaded medical documents with file path, checksum, and document type.
* `WorkflowRun`: State tracking for active patient requests and agent execution steps.
* `Reminder`: Automated notification tasks scheduled for patients.
* `Escalation`: Flagged requests awaiting human staff review and approval notes.
* `AuditEvent`: Immutable log of every system operation, actor ID, and metadata.

---

## 🚀 Quick Start Guide (First-Time Users)

### Prerequisites

Ensure you have the following installed on your machine:
* **Python**: 3.11 or higher
* **uv**: Fast Python package installer (`pip install uv` or follow [uv docs](https://docs.astral.sh/uv/))
* **Node.js**: v20 or higher
* **npm**: v10 or higher

---

### Step 1: Clone & Configure Environment

```bash
# Clone the repository
git clone https://github.com/YashShukla007/OmniAssist-AI.git
cd OmniAssist-AI

# Create backend environment configuration file
# On Windows PowerShell:
Copy-Item backend\.env.example backend\.env

# On Linux / macOS:
cp backend/.env.example backend/.env
```

Open `backend/.env` and update configuration parameters:
```ini
SECRET_KEY=generate_a_secure_random_key_with_at_least_32_characters
DATABASE_URL=sqlite:///./omniassist.db

# Choose your LLM Provider: "openrouter" or "ollama"
LLM_PROVIDER=openrouter

# OpenRouter (Cloud) settings
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODELS=google/gemini-2.5-flash

# Ollama (Local) settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

### Step 2: Backend Setup & Database Migration

```bash
# Install Python dependencies and build virtual environment
uv sync

# Run database migrations to create all tables
uv run alembic upgrade head
```

---

### Step 3: Seed Synthetic Demo Data & Accounts

Run the seed script to create initial clinical departments, sample doctors, available slots, and a **Hospital Staff** account for testing human review features:

```bash
# Create a synthetic Hospital Staff account (will prompt for a password)
uv run python -m backend.scripts.seed_demo --role hospital_staff --username "Demo Staff" --email staff@agentcare-demo.com
```

*(Note: Public registration in the UI creates `patient` accounts by default. Staff accounts are provisioned via this CLI tool for security).*

---

### Step 4: Run the Backend API Server

In your first terminal, launch the FastAPI application:

```bash
uv run uvicorn backend.app.main:app --reload --port 8000
```
* **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Step 5: Run the Frontend Web Application

Open a **second terminal** and start the React dev server:

```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

Open your browser and navigate to: **`http://localhost:5173`**

---

## 🧪 Verification & Testing Commands

To verify code quality, linting, syntax, and run the test suite before submitting:

### Backend Tests (pytest & compile check)

```bash
# Run pytest test suite (13+ backend unit/integration tests)
uv run pytest backend/tests -q

# Verify syntax compilation across all backend files
uv run python -m compileall backend

# Verify Alembic migration status
uv run alembic current
```

### Frontend Build & Linting

```bash
cd frontend

# Run ESLint check
npm run lint

# Build production bundle to verify no build errors
npm run build
```

---

## 🎬 Step-by-Step Demo Walkthrough

1. **Patient Registration & Login**:
   * Navigate to `http://localhost:5173` and click **Register**.
   * Create a new patient account (e.g., `patient@example.com`).
   * Complete the initial profile form under the **Patients / Profile** section.

2. **Submitting an Administrative Request**:
   * Open the **Chat Assistant** tab.
   * Attach a sample document (e.g. `ECG_Report.pdf`) and type:
     > *"I need a cardiology follow-up appointment next week and want to attach my old ECG report."*
   * Observe the **Coordinator Agent** dynamically executing the workflow map:
     `Intent Detection -> Department Routing (Cardiology) -> Slot Booking -> Document Classification -> Reminder Creation`.

3. **Managing Appointments & Documents**:
   * Visit the **Appointments** view to check your scheduled booking, or test rescheduling / cancelling slots.
   * Visit **Documents** to view the classified document metadata and MD5 checksum.
   * Visit **Reminders** to view auto-generated follow-up tasks.

4. **Testing Clinical Safety & Human Escalation**:
   * Go back to the **Chat Assistant** and type:
     > *"I have severe chest pain and short breath right now, what medication should I take?"*
   * The **Safety Agent** will intercept the message, block autonomous advice, and trigger a human review escalation ticket.

5. **Staff Portal & Escalation Approval**:
   * Sign out and log in as the staff user: `staff@agentcare-demo.com`.
   * Navigate to **Escalations** to review the flagged emergency ticket and submit a resolution note.
   * View **Audit Logs** to inspect the complete, immutable action history.
   * View **Analytics** to manage departments, doctors, and appointment slots.

---

## 🔒 Security & Safety Boundaries

* **No Autonomous Medical Advice**: The system rejects requests for medical diagnoses, treatment options, prescriptions, and dosage advice.
* **Strict Role Enforcement**: FastAPI middleware verifies authorization tokens and user roles for every staff endpoint.
* **PII & Data Safety**: All sample data in seed scripts and unit tests are strictly synthetic. Uploaded documents are stored locally in `backend/uploads/` (gitignored).

---

## 📁 Repository Structure

```text
OmniAssist-AI/
├── backend/
│   ├── app/
│   │   ├── agents/          # 6 Distinct Agent implementations
│   │   ├── api/v1/          # REST Endpoints (Auth, Healthcare, Audit)
│   │   ├── config/          # Environment & LLM provider settings
│   │   ├── core/            # Security, Auth Dependencies
│   │   ├── models/          # SQLAlchemy Database Models
│   │   ├── providers/       # LLM Providers (OpenRouter, Ollama)
│   │   └── services/        # Business Logic Services
│   ├── alembic/             # Database Migration Scripts
│   ├── scripts/             # Seed scripts (seed_demo.py)
│   ├── tests/               # Pytest Unit & Integration Tests
│   └── .env.example         # Template for environment variables
├── frontend/
│   ├── src/
│   │   ├── components/      # Chat, Navigation, Operations Workspace
│   │   ├── pages/           # Dashboard, AuthFlow, Landing Pages
│   │   └── index.css        # Responsive styling & Design tokens
│   ├── package.json
│   └── vite.config.js
├── .github/workflows/       # CI / Automated checks
├── pyproject.toml           # Python dependencies (uv)
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
