import { useEffect, useRef, useState } from "react";
import { AlertTriangle, BellRing, CalendarDays, Check, ChevronRight, ClipboardList, Download, Eye, FileText, HeartPulse, History, RefreshCw, Trash2, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";
import ChatWindow from "../components/chat/ChatWindow";
import MainLayout from "../components/layout/MainLayout";
import Navbar from "../components/layout/Navbar";
import RightPanel from "../components/layout/RightPanel";
import Sidebar from "../components/layout/Sidebar";
import api from "../services/api";
import { AppointmentCalendar, StaffOperationsWorkspace, WorkflowMap } from "../components/dashboard/HealthcareOperations";

function Notice({ message, onDismiss }) { return message ? <div className="app-notice" role="status"><span>{message}</span><button onClick={onDismiss} aria-label="Dismiss notification">×</button></div> : null; }
function statusClass(status) { return ["confirmed", "completed", "received"].includes(status?.toLowerCase()) ? "success" : "warning"; }
function displayStatus(status) { return status?.replaceAll("_", " ") ?? "Unknown"; }
function OverviewCard({ card, onClick }) { const Icon = card.icon; return <button className="overview-card" onClick={onClick}><div className="card-label"><Icon size={15} className={card.accent} />{card.label}</div><div className="overview-value"><strong>{card.value}</strong><span>{card.meta}</span></div><small>{card.detail}</small></button>; }

function DashboardOverview({ appointments, documents, reminders, username, onNavigate, onUpload, onToggleReminder }) {
  const nextAppointment = appointments[0];
  const cards = [
    { label: "Next Appointment", value: nextAppointment ? new Date(nextAppointment.start_time).getDate() : "–", meta: nextAppointment ? new Date(nextAppointment.start_time).toLocaleDateString(undefined, { month: "short", year: "numeric" }) : "No booking", icon: CalendarDays, accent: "blue", detail: nextAppointment?.department ?? "Book a visit", view: "Appointments" },
    { label: "Pending Tasks", value: String(reminders.filter((item) => item.status !== "completed").length), meta: "Tasks", icon: ClipboardList, accent: "green", detail: "View all →", view: "Reminders" },
    { label: "Documents", value: String(documents.length), meta: "Uploaded", icon: FileText, accent: "blue", detail: "View all →", view: "Documents" },
    { label: "Reminders", value: String(reminders.length), meta: "Scheduled", icon: BellRing, accent: "red", detail: "View all →", view: "Reminders" },
    { label: "Escalations", value: "–", meta: "Staff review", icon: AlertTriangle, accent: "red", detail: "Role restricted", view: "Escalations" },
  ];
  return <div className="dashboard-scroll"><section className="dashboard-heading"><div><p>Live information from your protected account</p><h1>Good morning, {username}</h1></div><button className="date-button" onClick={() => onNavigate("Appointments")}><CalendarDays size={14} />View appointments</button></section><section className="overview-grid">{cards.map((card) => <OverviewCard card={card} onClick={() => onNavigate(card.view)} key={card.label} />)}</section><section className="quick-actions"><h2>Quick Actions</h2><div><button className="quick-action blue" onClick={() => onNavigate("Appointments")}><CalendarDays /><span><strong>Book Appointment</strong><small>Schedule a new visit</small></span></button><button className="quick-action green" onClick={onUpload}><Upload /><span><strong>Upload Reports</strong><small>Upload medical documents</small></span></button><button className="quick-action purple" onClick={() => onNavigate("Chat Assistant")}><HeartPulse /><span><strong>Ask AI Assistant</strong><small>Start an administrative workflow</small></span></button><button className="quick-action orange" onClick={() => onNavigate("Audit Logs")}><History /><span><strong>View History</strong><small>Audit trail for staff users</small></span></button></div></section><section className="dashboard-panels"><AppointmentPanel appointments={appointments} onNavigate={onNavigate} /><DocumentsPanel documents={documents} onNavigate={onNavigate} /><ReminderPanel reminders={reminders} onNavigate={onNavigate} onToggle={onToggleReminder} /></section></div>;
}

function AppointmentPanel({ appointments, onNavigate }) { return <article className="dashboard-panel"><div className="section-heading"><h2>Upcoming Appointments</h2><button onClick={() => onNavigate("Appointments")}>View all</button></div>{appointments.slice(0, 2).map((item) => <button className="appointment" onClick={() => onNavigate("Appointments")} key={item.id}><time><strong>{new Date(item.start_time).getDate()}</strong><span>{new Date(item.start_time).toLocaleString(undefined, { month: "short" }).toUpperCase()}</span></time><div><strong>{item.department}</strong><small>{new Date(item.start_time).toLocaleString()}</small><small>{item.doctor_name}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span></button>)}{appointments.length === 0 && <p className="empty-panel">No appointments yet.</p>}</article>; }
function DocumentsPanel({ documents, onNavigate }) { return <article className="dashboard-panel"><div className="section-heading"><h2>Recent Documents</h2><button onClick={() => onNavigate("Documents")}>View all</button></div>{documents.slice(0, 3).map((item) => <button className="document-line" onClick={() => onNavigate("Documents")} key={item.id}><FileText size={18} /><div><strong>{item.original_filename}</strong><small>{item.document_type.replaceAll("_", " ")}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span></button>)}{documents.length === 0 && <p className="empty-panel">No documents uploaded.</p>}</article>; }
function ReminderPanel({ reminders, onNavigate, onToggle }) { return <article className="dashboard-panel"><div className="section-heading"><h2>Health Reminders</h2><button onClick={() => onNavigate("Reminders")}>View all</button></div>{reminders.slice(0, 3).map((item) => <button className="reminder-line" onClick={() => onToggle(item.id)} key={item.id}><span className={item.status === "completed" ? "reminder-check done" : "reminder-check"}>{item.status === "completed" && <Check size={12} />}</span><div><strong>{item.message}</strong><small>{new Date(item.scheduled_at).toLocaleString()}</small></div></button>)}{reminders.length === 0 && <p className="empty-panel">No reminders scheduled.</p>}</article>; }

function ProfileWorkspace({ profile, onSave, onNotice }) {
  const [form, setForm] = useState(profile ?? { phone: "", preferred_language: "en", emergency_contact: "", date_of_birth: "" });
  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  async function submit(event) { event.preventDefault(); const saved = await onSave(form); if (saved) onNotice("Your patient profile has been saved."); }
  return <div className="workspace-view"><div className="workspace-header"><div><h1>Patient Profile</h1><p>Keep your contact and communication preferences current.</p></div></div><form className="profile-form" onSubmit={submit}><label>Date of birth<input name="date_of_birth" type="date" value={form.date_of_birth} onChange={update} /></label><label>Phone<input name="phone" value={form.phone ?? ""} onChange={update} placeholder="+91 98765 43210" /></label><label>Preferred language<select name="preferred_language" value={form.preferred_language ?? "en"} onChange={update}><option value="en">English</option><option value="hi">Hindi</option></select></label><label>Emergency contact<input name="emergency_contact" value={form.emergency_contact ?? ""} onChange={update} placeholder="Name and phone number" /></label><button className="button button-primary">Save profile</button></form></div>;
}

function WorkflowWorkspace({ workflows }) { return <div className="workspace-view"><div className="workspace-header"><div><h1>Agent Workflows</h1><p>Persisted coordination runs created by the Healthcare AI Assistant.</p></div></div><div className="workspace-list">{workflows.map((workflow) => <div className="workspace-row" key={workflow.id}><ClipboardList size={18} /><div><strong>{workflow.request_text}</strong><small>{workflow.current_step.replaceAll("_", " ")} · {new Date(workflow.created_at).toLocaleString()}</small></div><span className={`status ${statusClass(workflow.status)}`}>{displayStatus(workflow.status)}</span></div>)}{workflows.length === 0 && <p className="empty-panel">Start an administrative request in Chat Assistant to create a workflow.</p>}</div></div>; }

function LegacyWorkspace({ title, appointments, documents, reminders, profile, workflows, onAddAppointment, onUpload, onToggleReminder, onSaveProfile, onNotice }) {
  const [formOpen, setFormOpen] = useState(false);
  const [form, setForm] = useState({ department: "Cardiology", preferred_date: "", preferred_time: "10:30 AM", reason: "Administrative appointment request" });
  async function submitAppointment(event) { event.preventDefault(); if (!form.preferred_date) return onNotice("Choose a preferred appointment date first."); const success = await onAddAppointment(form); if (success) setFormOpen(false); }
  if (title === "Appointments") return <div className="workspace-view"><div className="workspace-header"><div><h1>Appointments</h1><p>Review persisted visits or request an available slot.</p></div><button className="button button-primary" onClick={() => setFormOpen(true)}>Book appointment</button></div>{formOpen && <form className="inline-form" onSubmit={submitAppointment}><label>Department<select value={form.department} onChange={(event) => setForm((current) => ({ ...current, department: event.target.value }))}><option>Cardiology</option><option>General Medicine</option></select></label><label>Preferred date<input type="date" value={form.preferred_date} onChange={(event) => setForm((current) => ({ ...current, preferred_date: event.target.value }))} /></label><label>Reason<input value={form.reason} onChange={(event) => setForm((current) => ({ ...current, reason: event.target.value }))} /></label><button className="button button-primary">Request slot</button><button type="button" className="button button-secondary" onClick={() => setFormOpen(false)}>Cancel</button></form>}<div className="workspace-list">{appointments.map((item) => <div className="workspace-row" key={item.id}><CalendarDays size={18} /><div><strong>{item.department}</strong><small>{new Date(item.start_time).toLocaleString()} · {item.doctor_name}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span></div>)}</div></div>;
  if (title === "Documents") return <div className="workspace-view"><div className="workspace-header"><div><h1>Documents</h1><p>Upload, classify, and detect duplicate health documents.</p></div><button className="button button-primary" onClick={onUpload}><Upload size={16} />Upload report</button></div><div className="workspace-list">{documents.map((item) => <div className="workspace-row" key={item.id}><FileText size={18} /><div><strong>{item.original_filename}</strong><small>{item.document_type.replaceAll("_", " ")}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span></div>)}</div></div>;
  if (title === "Reminders") return <div className="workspace-view"><div className="workspace-header"><div><h1>Health Reminders</h1><p>Click a reminder to update its persisted completion status.</p></div></div><div className="workspace-list">{reminders.map((item) => <button className="workspace-row" onClick={() => onToggleReminder(item.id)} key={item.id}><span className={item.status === "completed" ? "reminder-check done" : "reminder-check"}>{item.status === "completed" && <Check size={12} />}</span><div><strong>{item.message}</strong><small>{new Date(item.scheduled_at).toLocaleString()}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span></button>)}</div></div>;
  if (title === "Patients") return <ProfileWorkspace key={profile?.id ?? "profile-loading"} profile={profile} onSave={onSaveProfile} onNotice={onNotice} />;
  if (title === "Workflows") return <WorkflowWorkspace workflows={workflows} />;
  return <div className="placeholder-view"><div className="placeholder-icon"><ClipboardList size={27} /></div><h1>{title}</h1><p>This screen is role-restricted or awaiting its dedicated backend module.</p><button className="button button-primary" onClick={() => onNotice(`${title} requires a permitted role or the next backend module.`)}>View access requirements <ChevronRight size={16} /></button></div>;
}

function EnhancedAppointmentWorkspace({ appointments, onAddAppointment, onNotice }) {
  const [formOpen, setFormOpen] = useState(false);
  const [form, setForm] = useState({ department: "Cardiology", preferred_date: "", preferred_time: "10:30 AM", reason: "Administrative appointment request" });
  const [overrides, setOverrides] = useState({});
  async function submit(event) { event.preventDefault(); if (!form.preferred_date) return onNotice("Choose a preferred appointment date first."); if (await onAddAppointment(form)) setFormOpen(false); }
  const visibleAppointments = appointments.map((item) => overrides[item.id] ?? item);
  async function updateAppointment(item, action) { const preferred_date = action === "reschedule" ? window.prompt("Enter a new date (YYYY-MM-DD):", new Date(item.start_time).toISOString().slice(0, 10)) : null; if (action === "reschedule" && !preferred_date) return; try { const response = await api.patch(`/healthcare/appointments/${item.id}`, { action, ...(preferred_date ? { preferred_date } : {}) }); setOverrides((current) => ({ ...current, [item.id]: response.data })); onNotice(`Appointment ${action === "cancel" ? "cancelled" : "rescheduled"}.`); } catch (error) { onNotice(error.response?.data?.detail ?? "Appointment update failed."); } }
  return <div className="workspace-view"><div className="workspace-header"><div><h1>Appointments</h1><p>Review persisted visits or request an available conflict-free slot.</p></div><button className="button button-primary" onClick={() => setFormOpen(true)}>Book appointment</button></div>{formOpen && <form className="inline-form" onSubmit={submit}><label>Department<select value={form.department} onChange={(event) => setForm((current) => ({ ...current, department: event.target.value }))}><option>Cardiology</option><option>General Medicine</option></select></label><label>Preferred date<input type="date" min={new Date().toISOString().slice(0, 10)} value={form.preferred_date} onChange={(event) => setForm((current) => ({ ...current, preferred_date: event.target.value }))} /></label><label>Preferred time<input value={form.preferred_time} onChange={(event) => setForm((current) => ({ ...current, preferred_time: event.target.value }))} placeholder="10:30 AM" /></label><label>Reason<input value={form.reason} onChange={(event) => setForm((current) => ({ ...current, reason: event.target.value }))} /></label><button className="button button-primary">Request slot</button><button type="button" className="button button-secondary" onClick={() => setFormOpen(false)}>Cancel</button></form>}<AppointmentCalendar appointments={visibleAppointments} /><div className="workspace-list">{visibleAppointments.map((item) => <div className="workspace-row" key={item.id}><CalendarDays size={18} /><div><strong>{item.department}</strong><small>{new Date(item.start_time).toLocaleString()} / {item.doctor_name}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span>{item.status === "confirmed" && <div className="operations-actions"><button className="button button-secondary" onClick={() => updateAppointment(item, "reschedule")}>Reschedule</button><button className="button button-secondary" onClick={() => updateAppointment(item, "cancel")}>Cancel</button></div>}</div>)}{visibleAppointments.length === 0 && <p className="empty-panel">No appointments yet.</p>}</div></div>;
}

function EnhancedWorkflowWorkspace({ workflows }) {
  return <div className="workspace-view"><div className="workspace-header"><div><h1>Agent Workflows</h1><p>Persisted coordination runs, agent hand-offs, and workflow state.</p></div></div><div className="workflow-list">{workflows.map((workflow) => <WorkflowMap workflow={workflow} key={workflow.id} />)}{workflows.length === 0 && <p className="empty-panel">Start an administrative request in Chat Assistant to create a workflow.</p>}</div></div>;
}

// Retained temporarily while the document workspace evolves without changing saved document behavior.
// eslint-disable-next-line no-unused-vars
function LegacyEnhancedDocumentsWorkspace({ documents, onNotice }) {
  const inputRef = useRef(null);
  const [displayDocuments, setDisplayDocuments] = useState(documents);
  const [replacementId, setReplacementId] = useState(null);
  const chooseFile = (documentId = null) => { setReplacementId(documentId); inputRef.current?.click(); };
  const upload = async (event) => { const file = event.target.files?.[0]; if (!file) return; const data = new FormData(); data.append("file", file); try { const response = replacementId ? await api.put(`/healthcare/documents/${replacementId}`, data) : await api.post("/healthcare/documents", data); setDisplayDocuments((current) => replacementId ? current.map((item) => item.id === replacementId ? response.data : item) : [response.data, ...current]); onNotice(replacementId ? `${file.name} replaced the previous document.` : `${file.name} was uploaded and classified.`); } catch (error) { onNotice(error.response?.data?.detail ?? "Document upload failed."); } finally { event.target.value = ""; setReplacementId(null); } };
  const remove = async (document) => { if (!window.confirm(`Delete ${document.original_filename}? This cannot be undone.`)) return; try { await api.delete(`/healthcare/documents/${document.id}`); setDisplayDocuments((current) => current.filter((item) => item.id !== document.id)); onNotice(`${document.original_filename} was deleted.`); } catch (error) { onNotice(error.response?.data?.detail ?? "Document deletion failed."); } };
  return <div className="workspace-view"><div className="workspace-header"><div><h1>Documents</h1><p>Upload, replace, or delete your own persisted healthcare documents.</p></div><button className="button button-primary" onClick={() => chooseFile()}><Upload size={16} />Upload report</button></div><input ref={inputRef} className="visually-hidden" type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={upload} /><div className="workspace-list">{displayDocuments.map((item) => <article className="workspace-row document-workspace-row" key={item.id}><FileText size={18} /><div><strong>{item.original_filename}</strong><small>{item.document_type.replaceAll("_", " ")} · uploaded {new Date(item.created_at).toLocaleDateString()}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span><div className="document-actions"><button type="button" onClick={() => chooseFile(item.id)} aria-label={`Replace ${item.original_filename}`} title="Replace document"><RefreshCw size={15} /></button><button type="button" className="danger-action" onClick={() => remove(item)} aria-label={`Delete ${item.original_filename}`} title="Delete document"><Trash2 size={15} /></button></div></article>)}{displayDocuments.length === 0 && <p className="empty-panel">No documents uploaded.</p>}</div></div>;
}

function EnhancedDocumentsWorkspace({ documents, onNotice }) {
  const inputRef = useRef(null);
  const [displayDocuments, setDisplayDocuments] = useState(documents);
  const [replacementId, setReplacementId] = useState(null);

  const chooseFile = (documentId = null) => {
    setReplacementId(documentId);
    inputRef.current?.click();
  };

  const accessFile = async (document, action) => {
    const previewWindow = action === "view" ? window.open("", "_blank", "noopener") : null;
    try {
      const response = await api.get(`/healthcare/documents/${document.id}/content`, {
        params: { download: action === "download" },
        responseType: "blob",
      });
      const objectUrl = URL.createObjectURL(response.data);
      if (action === "download") {
        const link = window.document.createElement("a");
        link.href = objectUrl;
        link.download = document.original_filename;
        window.document.body.appendChild(link);
        link.click();
        link.remove();
      } else if (previewWindow) {
        previewWindow.location.href = objectUrl;
      } else {
        onNotice("Your browser blocked the preview window. Please allow pop-ups and try again.");
      }
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60_000);
    } catch (error) {
      previewWindow?.close();
      onNotice(error.response?.data?.detail ?? `Document ${action} failed.`);
    }
  };

  const upload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const data = new FormData();
    data.append("file", file);
    try {
      const response = replacementId
        ? await api.put(`/healthcare/documents/${replacementId}`, data)
        : await api.post("/healthcare/documents", data);
      setDisplayDocuments((current) => replacementId
        ? current.map((item) => item.id === replacementId ? response.data : item)
        : [response.data, ...current]);
      onNotice(replacementId ? `${file.name} replaced the previous document.` : `${file.name} was uploaded and classified.`);
    } catch (error) {
      onNotice(error.response?.data?.detail ?? "Document upload failed.");
    } finally {
      event.target.value = "";
      setReplacementId(null);
    }
  };

  const remove = async (document) => {
    if (!window.confirm(`Delete ${document.original_filename}? This cannot be undone.`)) return;
    try {
      await api.delete(`/healthcare/documents/${document.id}`);
      setDisplayDocuments((current) => current.filter((item) => item.id !== document.id));
      onNotice(`${document.original_filename} was deleted.`);
    } catch (error) {
      onNotice(error.response?.data?.detail ?? "Document deletion failed.");
    }
  };

  return <div className="workspace-view"><div className="workspace-header"><div><h1>Documents</h1><p>Upload, view, download, replace, or delete your own persisted healthcare documents.</p></div><button className="button button-primary" onClick={() => chooseFile()}><Upload size={16} />Upload report</button></div><input ref={inputRef} className="visually-hidden" type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={upload} /><div className="workspace-list">{displayDocuments.map((item) => <article className="workspace-row document-workspace-row" key={item.id}><FileText size={18} /><div><strong>{item.original_filename}</strong><small>{item.document_type.replaceAll("_", " ")} · uploaded {new Date(item.created_at).toLocaleDateString()}</small></div><span className={`status ${statusClass(item.status)}`}>{displayStatus(item.status)}</span><div className="document-actions"><button type="button" onClick={() => accessFile(item, "view")} aria-label={`View ${item.original_filename}`} title="View document"><Eye size={15} /></button><button type="button" onClick={() => accessFile(item, "download")} aria-label={`Download ${item.original_filename}`} title="Download document"><Download size={15} /></button><button type="button" onClick={() => chooseFile(item.id)} aria-label={`Replace ${item.original_filename}`} title="Replace document"><RefreshCw size={15} /></button><button type="button" className="danger-action" onClick={() => remove(item)} aria-label={`Delete ${item.original_filename}`} title="Delete document"><Trash2 size={15} /></button></div></article>)}{displayDocuments.length === 0 && <p className="empty-panel">No documents uploaded.</p>}</div></div>;
}

function EnhancedWorkspace(props) {
  if (props.title === "Appointments") return <EnhancedAppointmentWorkspace appointments={props.appointments} onAddAppointment={props.onAddAppointment} onNotice={props.onNotice} />;
  if (props.title === "Documents") return <EnhancedDocumentsWorkspace documents={props.documents} onNotice={props.onNotice} />;
  if (props.title === "Workflows" && ["hospital_staff", "administrator"].includes(sessionStorage.getItem("omniassist_role"))) return <StaffOperationsWorkspace title="Workflows" role={sessionStorage.getItem("omniassist_role")} />;
  if (props.title === "Workflows") return <EnhancedWorkflowWorkspace workflows={props.workflows} />;
  if (["Escalations", "Audit Logs", "Analytics"].includes(props.title)) return <StaffOperationsWorkspace title={props.title} role={sessionStorage.getItem("omniassist_role")} />;
  return <LegacyWorkspace {...props} />;
}

function Workspace(props) { return <EnhancedWorkspace {...props} />; }

function Dashboard() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [activeView, setActiveView] = useState("Dashboard");
  const [notice, setNotice] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [profile, setProfile] = useState(null);
  const [workflows, setWorkflows] = useState([]);
  const username = sessionStorage.getItem("omniassist_username") ?? "Patient";
  const showNotice = (message) => { if (message === "Invalid or expired token") return; setNotice(message); window.setTimeout(() => setNotice(""), 5000); };
  const loadHealthcareData = async () => { try { const [appointmentResponse, documentResponse, reminderResponse, profileResponse, workflowResponse] = await Promise.all([api.get("/healthcare/appointments"), api.get("/healthcare/documents"), api.get("/healthcare/reminders"), api.get("/healthcare/profile"), api.get("/healthcare/workflows")]); setAppointments(appointmentResponse.data); setDocuments(documentResponse.data); setReminders(reminderResponse.data); setProfile(profileResponse.data); setWorkflows(workflowResponse.data); } catch (error) { showNotice(error.response?.data?.detail ?? "Could not load your healthcare data."); } };
  const refreshAfterHealthcareWorkflow = async ({ document, workflow } = {}) => {
    if (document) setDocuments((current) => [document, ...current.filter((item) => item.id !== document.id)]);
    if (workflow) setWorkflows((current) => [{ id: workflow.id, request_text: workflow.summary, status: workflow.status, current_step: workflow.current_step, state: workflow.state, created_at: new Date().toISOString() }, ...current.filter((item) => item.id !== workflow.id)]);
    await loadHealthcareData();
  };
  useEffect(() => {
    if (!localStorage.getItem("omniassist_token")) {
      navigate("/login");
      return undefined;
    }

    const initialLoad = window.setTimeout(() => {
      void loadHealthcareData();
    }, 0);

    return () => window.clearTimeout(initialLoad);
    // The protected dashboard loads once after it mounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [navigate]);
  const chooseFile = () => fileInputRef.current?.click();
  const uploadFile = async (event) => { const file = event.target.files?.[0]; if (!file) return; const formData = new FormData(); formData.append("file", file); try { const response = await api.post("/healthcare/documents", formData); showNotice(response.data.duplicate ? `${file.name} is already stored; the duplicate was detected.` : `${file.name} was uploaded and classified.`); await loadHealthcareData(); } catch (error) { showNotice(error.response?.data?.detail ?? "Document upload failed."); } finally { event.target.value = ""; } };
  const addAppointment = async (form) => { try { const response = await api.post("/healthcare/appointments", form); showNotice(`${response.data.department} appointment booked with ${response.data.doctor_name}.`); await loadHealthcareData(); return true; } catch (error) { showNotice(error.response?.data?.detail ?? "Appointment booking failed."); return false; } };
  const toggleReminder = async (reminderId) => { try { await api.post(`/healthcare/reminders/${reminderId}/toggle`); await loadHealthcareData(); } catch (error) { showNotice(error.response?.data?.detail ?? "Reminder update failed."); } };
  const saveProfile = async (update) => { try { const response = await api.put("/healthcare/profile", update); setProfile(response.data); return true; } catch (error) { showNotice(error.response?.data?.detail ?? "Profile update failed."); return false; } };
  const showDomainUnavailable = (domain) => showNotice(`${domain} is work in progress. Healthcare is the only integrated domain right now; ${domain} will be connected in a future release.`);
  const logout = () => { localStorage.removeItem("omniassist_token"); sessionStorage.removeItem("omniassist_role"); sessionStorage.removeItem("omniassist_username"); navigate("/"); };
  return <MainLayout sidebar={<Sidebar activeView={activeView} onNavigate={setActiveView} onLogout={logout} onDomainUnavailable={showDomainUnavailable} />} insights={<RightPanel onNavigate={setActiveView} onNotice={showNotice} />}><Navbar onNavigate={setActiveView} onNotice={showNotice} onDomainUnavailable={showDomainUnavailable} /><div className={`dashboard-content ${activeView === "Chat Assistant" ? "assistant-view" : ""}`}>{activeView === "Dashboard" ? <DashboardOverview appointments={appointments} documents={documents} reminders={reminders} username={username} onNavigate={setActiveView} onUpload={chooseFile} onToggleReminder={toggleReminder} /> : activeView === "Chat Assistant" ? <ChatWindow showHeader={false} compact onHealthcareUpdated={refreshAfterHealthcareWorkflow} /> : <Workspace title={activeView} appointments={appointments} documents={documents} reminders={reminders} profile={profile} workflows={workflows} onAddAppointment={addAppointment} onUpload={chooseFile} onToggleReminder={toggleReminder} onSaveProfile={saveProfile} onNotice={showNotice} />}</div><input className="visually-hidden" ref={fileInputRef} type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={uploadFile} /><Notice message={notice} onDismiss={() => setNotice("")} /></MainLayout>;
}

export default Dashboard;
