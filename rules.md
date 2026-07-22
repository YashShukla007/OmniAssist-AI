About
Welcome to the AgentCare Build Challenge 2026.

Hospitals and clinics drown in repetitive administrative work — registering patients, routing requests to the right department, checking doctor availability, booking and rescheduling appointments, collecting documents, sending reminders, coordinating follow-ups. These workflows are scattered across forms, phone calls, spreadsheets, and disconnected systems.

Your challenge is to build AgentCare: an agentic AI application that understands an administrative patient request, plans the steps, invokes the right tools, persists workflow state, and completes the task safely — with multiple genuinely distinct agents coordinating the work.

This is not a diagnosis or treatment system. The application must never independently diagnose conditions, prescribe medicine, recommend dosages, or claim to replace a clinician. Medical decisions stay under human supervision; the agents handle administration and coordination only.

What is judged is genuine, end-to-end implementation — route → service → agent → tool → database → persisted result. Depth of real wiring beats breadth of stubs.


1 problem statement

Pick one and start building

Rules
These rules are checked before scoring. Breaking any one results in a score of zero.

Accessible source repository. A public GitHub repository containing your real application source. An empty, inaccessible, or documentation-only repo is disqualified.
Python backend. The primary backend must be implemented in Python. No meaningful Python backend → disqualified.
Agentic AI, not CRUD. The app must use an LLM and implement a multi-step, tool-using agent workflow. A CRUD-only hospital app with no agent workflow, or a chat box that only forwards prompts to an LLM and takes no actions, is disqualified.
Persistent SQL database. Core patient, appointment, document, and workflow data must live in a persistent SQL database (SQLite, PostgreSQL, MySQL, …). In-memory dicts or session variables that vanish on restart → disqualified.
Healthcare safety boundary. The system must not autonomously diagnose, prescribe, change dosages, or claim to replace a clinician. Administrative department routing is fine (routing a heart follow-up to Cardiology); asserting a diagnosis is not.
Data & secret safety. No real patient data, private credentials, API secrets, or production tokens in the repo. Keep secrets in a local, gitignored .env and ship a .env.example without real values. Committed PII or usable secrets → disqualified and flagged for review.
The repository must be your own work. Disclose third-party code, templates, or generated components where appropriate.