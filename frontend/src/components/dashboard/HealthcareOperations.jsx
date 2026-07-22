import { useCallback, useEffect, useState } from "react";
import { Activity, AlertTriangle, CheckCircle2, ClipboardList, FileText, ShieldCheck } from "lucide-react";
import api from "../../services/api";

function labelize(value) {
  return value?.replaceAll("_", " ") ?? "Unknown";
}

export function AppointmentCalendar({ appointments }) {
  const days = Array.from({ length: 7 }, (_, offset) => {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() + offset);
    return date;
  });
  return <section className="calendar-card" aria-label="Upcoming appointment calendar"><div className="section-heading"><h2>Appointment calendar</h2><span>Next 7 days</span></div><div className="calendar-week">{days.map((day) => { const entries = appointments.filter((appointment) => new Date(appointment.start_time).toDateString() === day.toDateString()); return <div className="calendar-day" key={day.toISOString()}><strong>{day.toLocaleDateString(undefined, { weekday: "short" })}</strong><time>{day.getDate()}</time>{entries.map((entry) => <span key={entry.id} title={`${entry.department}: ${new Date(entry.start_time).toLocaleTimeString()}`}>{entry.department}</span>)}</div>; })}</div></section>;
}

export function WorkflowMap({ workflow }) {
  const steps = [
    ["Coordinator", "plan"],
    ["Safety", "safety"],
    ["Routing", "department"],
    ["Appointment", "appointment_id"],
    ["Documents", "document_ids"],
    ["Follow-up", "completed"],
  ];
  const state = workflow.state ?? {};

  const getStatusDescription = () => {
    if (workflow.status === "completed") {
      return "All steps successfully executed: The request has been routed, appointments booked, documents processed, and follow-ups scheduled.";
    }
    if (workflow.status === "failed") {
      return "The workflow execution failed or was aborted due to an error.";
    }
    const currentLower = workflow.current_step.toLowerCase();
    if (currentLower.includes("coordinator")) {
      return "Coordinator Agent: Analyzing the administrative request, matching the patient record, and planning next steps.";
    }
    if (currentLower.includes("safety")) {
      return "Safety Agent: Verifying compliance with safety boundaries and checking for any sensitive/emergency keywords requiring human review.";
    }
    if (currentLower.includes("routing")) {
      return "Department Routing Agent: Mapping the request to the correct medical department (e.g. Cardiology).";
    }
    if (currentLower.includes("appointment")) {
      return "Appointment Agent: Checking calendar availability and reserving the requested appointment slot.";
    }
    if (currentLower.includes("document")) {
      return "Document Agent: Parsing attached documents, checking for duplicate files, and identifying missing records.";
    }
    if (currentLower.includes("follow_up") || currentLower.includes("follow-up")) {
      return "Follow-up Agent: Scheduling reminders, follow-up notifications, and closing the active workflow.";
    }
    return `Currently executing: ${labelize(workflow.current_step)}. Orchestrating sub-agents to complete the administration.`;
  };

  return <article className="workflow-map"><header><ClipboardList size={16} /><div><strong>Workflow #{workflow.id}</strong><small>{labelize(workflow.current_step)}</small></div><span className={`status ${workflow.status === "completed" ? "success" : "warning"}`}>{labelize(workflow.status)}</span></header><div className="workflow-steps">{steps.map(([name, stateKey], index) => { const complete = workflow.status === "completed" || Boolean(state[stateKey]) || (name === "Safety" && state.safety === "escalated"); const current = workflow.current_step.includes(name.toLowerCase().replace("-", "_")); return <div className={complete ? "complete" : current ? "current" : "pending"} key={name}><i>{complete ? <CheckCircle2 size={13} /> : index + 1}</i><span>{name}</span></div>; })}</div><p className="workflow-status-desc">{getStatusDescription()}</p>{state.department && <p className="workflow-detail">Routed to <strong>{state.department}</strong>{state.appointment_id ? ` · Appointment #${state.appointment_id}` : ""}</p>}{state.missing_document_types?.length > 0 && <p className="workflow-detail warning-text">Document follow-up: {state.missing_document_types.join(", ")}</p>}</article>;
}

export function StaffOperationsWorkspace({ title, role }) {
  const normalizedRole = role?.toLowerCase()?.replace(/\s+/g, "_");
  const allowed = ["hospital_staff", "administrator", "staff", "admin"].includes(normalizedRole);
  const [escalations, setEscalations] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [auditEvents, setAuditEvents] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [message, setMessage] = useState("");
  const load = useCallback(async () => {
    if (!allowed) return;
    try {
      if (title === "Escalations") setEscalations((await api.get("/healthcare/escalations")).data);
      if (title === "Workflows") setWorkflows((await api.get("/healthcare/operations/workflows")).data);
      if (title === "Audit Logs") setAuditEvents((await api.get("/healthcare/audit")).data);
      if (title === "Analytics") {
        const [analyticsResponse, departmentResponse, doctorResponse] = await Promise.all([api.get("/healthcare/analytics"), api.get("/healthcare/operations/departments"), api.get("/healthcare/operations/doctors")]);
        setAnalytics(analyticsResponse.data);
        setDepartments(departmentResponse.data);
        setDoctors(doctorResponse.data);
      }
    } catch (error) {
      setMessage(error.response?.data?.detail ?? "Could not load healthcare operations data.");
    }
  }, [allowed, title]);
  useEffect(() => {
    const deferredLoad = window.setTimeout(() => { void load(); }, 0);
    return () => window.clearTimeout(deferredLoad);
  }, [load]);
  const review = async (id, approved) => {
    const note = window.prompt(approved ? "Add an approval note for the audit log:" : "Add a decline note for the audit log:");
    if (!note?.trim()) return;
    try {
      await api.post(`/healthcare/escalations/${id}/review`, { approved, note: note.trim() });
      setMessage(`Escalation #${id} ${approved ? "approved" : "declined"}.`);
      await load();
    } catch (error) {
      setMessage(error.response?.data?.detail ?? "Escalation review could not be saved.");
    }
  };
  const createDoctor = async () => {
    const departmentId = window.prompt(`Department ID (${departments.map((item) => `${item.id}: ${item.name}`).join(", ")}):`);
    const name = departmentId ? window.prompt("Doctor name:") : null;
    if (!departmentId || !name?.trim()) return;
    try { await api.post("/healthcare/operations/doctors", { department_id: Number(departmentId), name: name.trim() }); setMessage("Doctor created."); await load(); } catch (error) { setMessage(error.response?.data?.detail ?? "Doctor creation failed."); }
  };
  const createDepartment = async () => {
    const name = window.prompt("Department name:");
    const description = name ? window.prompt("Department description:") : null;
    if (!name?.trim() || !description?.trim()) return;
    try { await api.post("/healthcare/operations/departments", { name: name.trim(), description: description.trim() }); setMessage("Department created."); await load(); } catch (error) { setMessage(error.response?.data?.detail ?? "Department creation failed."); }
  };
  const createSlot = async () => {
    const doctorId = window.prompt(`Doctor ID (${doctors.map((item) => `${item.id}: ${item.name}`).join(", ")}):`);
    const startTime = doctorId ? window.prompt("Slot start in local ISO format (for example 2026-07-25T10:00:00):") : null;
    const endTime = startTime ? window.prompt("Slot end in local ISO format (for example 2026-07-25T10:30:00):") : null;
    if (!doctorId || !startTime || !endTime) return;
    try { await api.post("/healthcare/operations/slots", { doctor_id: Number(doctorId), start_time: startTime, end_time: endTime }); setMessage("Appointment slot created."); await load(); } catch (error) { setMessage(error.response?.data?.detail ?? "Slot creation failed."); }
  };
  if (!allowed) return <div className="placeholder-view"><div className="placeholder-icon"><ShieldCheck size={27} /></div><h1>{title}</h1><p>This protected healthcare operations screen is available to Hospital Staff and Administrators only.</p></div>;
  if (title === "Workflows") return <div className="workspace-view"><div className="workspace-header"><div><h1>Patient requests</h1><p>All persisted AgentCare workflows, available to authorized hospital staff.</p></div></div>{message && <p className="form-message">{message}</p>}<div className="workspace-list">{workflows.map((item) => <article className="operations-row" key={item.id}><ClipboardList size={18} /><div><strong>{item.patient_name} · Workflow #{item.id}</strong><small>{item.request_text}</small><small>{new Date(item.created_at).toLocaleString()}</small></div><span className={`status ${item.status === "completed" ? "success" : "warning"}`}>{labelize(item.status)}</span></article>)}{workflows.length === 0 && <p className="empty-panel">No patient workflows have been created yet.</p>}</div></div>;
  if (title === "Escalations") return <div className="workspace-view"><div className="workspace-header"><div><h1>Escalations & approvals</h1><p>Safety-sensitive requests require documented human review before completion.</p></div></div>{message && <p className="form-message">{message}</p>}<div className="workspace-list">{escalations.map((item) => <article className="operations-row" key={item.id}><AlertTriangle size={19} /><div><strong>Workflow #{item.workflow_run_id}</strong><small>{item.reason}</small><small>{new Date(item.created_at).toLocaleString()}</small></div><span className={`status ${item.status === "approved" ? "success" : "warning"}`}>{labelize(item.status)}</span>{item.status === "open" && <div className="operations-actions"><button className="button button-primary" onClick={() => review(item.id, true)}>Approve</button><button className="button button-secondary" onClick={() => review(item.id, false)}>Decline</button></div>}</article>)}{escalations.length === 0 && <p className="empty-panel">No escalations need review.</p>}</div></div>;
  if (title === "Audit Logs") return <div className="workspace-view"><div className="workspace-header"><div><h1>Audit log</h1><p>Persisted actions from patients, agents, and staff reviewers.</p></div></div><div className="workspace-list">{auditEvents.map((item) => <article className="operations-row" key={item.id}><FileText size={18} /><div><strong>{labelize(item.action)}</strong><small>{item.entity_type}{item.entity_id ? ` #${item.entity_id}` : ""}</small><small>{new Date(item.created_at).toLocaleString()}</small></div><span className="audit-details">{Object.keys(item.details ?? {}).length ? JSON.stringify(item.details) : "Recorded"}</span></article>)}{auditEvents.length === 0 && <p className="empty-panel">No audit events yet.</p>}</div></div>;
  return <AnalyticsWorkspace analytics={analytics} departments={departments} doctors={doctors} message={message} onCreateDepartment={createDepartment} onCreateDoctor={createDoctor} onCreateSlot={createSlot} />;
}

function Metric({ label, value, icon: Icon, tone }) {
  return <article className="metric-card"><span className={tone}><Icon size={17} /></span><div><small>{label}</small><strong>{value ?? 0}</strong></div></article>;
}

function BarChart({ buckets, title }) {
  const max = Math.max(1, ...buckets.map((item) => item.value));
  return <article className="chart-card"><h2>{title}</h2><div className="bar-chart" role="img" aria-label={title}>{buckets.map((item) => <div className="bar-column" key={item.label}><span style={{ height: `${Math.max(6, (item.value / max) * 100)}%` }} title={`${item.label}: ${item.value}`} /><strong>{item.value}</strong><small>{item.label}</small></div>)}</div></article>;
}

function AnalyticsWorkspace({ analytics, departments, doctors, message, onCreateDepartment, onCreateDoctor, onCreateSlot }) {
  const data = analytics ?? { patients: 0, appointments: 0, documents: 0, open_escalations: 0, workflows_completed: 0, appointment_statuses: [], workflow_statuses: [], appointments_by_day: [] };
  return <div className="workspace-view"><div className="workspace-header"><div><h1>Healthcare analytics</h1><p>Live operational metrics calculated from the persistent SQL database.</p></div></div>{message && <p className="form-message">{message}</p>}<section className="metrics-grid"><Metric label="Patient profiles" value={data.patients} icon={ClipboardList} tone="blue" /><Metric label="Appointments" value={data.appointments} icon={Activity} tone="green" /><Metric label="Documents" value={data.documents} icon={FileText} tone="violet" /><Metric label="Open escalations" value={data.open_escalations} icon={AlertTriangle} tone="orange" /></section><section className="chart-grid"><BarChart title="Appointments by day" buckets={data.appointments_by_day} /><BarChart title="Appointment status" buckets={data.appointment_statuses} /><BarChart title="Workflow status" buckets={data.workflow_statuses} /></section><section className="catalogue-card"><div><h2>Hospital catalogue</h2><p>Manage the persisted departments, doctors, and appointment availability.</p></div><div className="catalogue-actions"><button className="button button-primary" onClick={onCreateDepartment}>Add department</button><button className="button button-primary" onClick={onCreateDoctor}>Add doctor</button><button className="button button-secondary" onClick={onCreateSlot}>Add slot</button></div><p><strong>Departments:</strong> {departments.map((item) => item.name).join(", ") || "None"}</p><p><strong>Doctors:</strong> {doctors.map((item) => item.name).join(", ") || "None"}</p></section><p className="analytics-footnote"><Activity size={14} /> {data.workflows_completed} completed workflow{data.workflows_completed === 1 ? "" : "s"} recorded.</p></div>;
}
