import { useEffect, useRef, useState } from "react";
import { Activity, BellRing, BotMessageSquare, CalendarDays, ChevronDown, CircleHelp, FileText, HeartPulse, LayoutDashboard, LogOut, Scale, Settings, ShieldAlert, UserRound, UsersRound, Workflow } from "lucide-react";
import { useDomain } from "../../context/DomainContext";

const navigation = [["Dashboard", LayoutDashboard], ["Chat Assistant", BotMessageSquare], ["Appointments", CalendarDays], ["Patients", UsersRound], ["Documents", FileText], ["Workflows", Workflow], ["Analytics", Activity], ["Reminders", BellRing], ["Escalations", ShieldAlert], ["Audit Logs", CircleHelp]];
const domains = [["Healthcare", HeartPulse], ["IT Helpdesk", BotMessageSquare], ["HR", UsersRound], ["Finance", Activity], ["Legal", Scale]];

function Sidebar({ activeView, onNavigate, onLogout, onDomainUnavailable }) {
  const { selectedDomain, setSelectedDomain } = useDomain();
  const [profileOpen, setProfileOpen] = useState(false);
  const userRef = useRef(null);
  const username = sessionStorage.getItem("omniassist_username") ?? "Patient";
  const initials = username.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase() || "P";

  useEffect(() => {
    function handleClickOutside(event) {
      if (userRef.current && !userRef.current.contains(event.target)) {
        setProfileOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const chooseDomain = (domain) => {
    if (domain !== "Healthcare") {
      onDomainUnavailable(domain);
      return;
    }

    setSelectedDomain(domain);
    onNavigate("Dashboard");
  };
  return <aside className="sidebar"><button className="sidebar-brand" onClick={() => onNavigate("Dashboard")}><span className="brand-mark"><HeartPulse size={18} /></span><strong>OmniAssist AI</strong></button><nav className="sidebar-nav">{navigation.map(([label, Icon]) => <button key={label} className={activeView === label ? "active" : ""} onClick={() => onNavigate(label)}><Icon size={16} />{label}</button>)}</nav><div className="sidebar-domains"><p>Domains</p>{domains.map(([domain, Icon]) => <button key={domain} className={selectedDomain === domain ? "domain-active" : ""} onClick={() => chooseDomain(domain)}><Icon size={15} />{domain}</button>)}</div><div className="sidebar-user" ref={userRef}><span className="avatar">{initials}</span><div><strong>{username}</strong><small>{sessionStorage.getItem("omniassist_role") ?? "Patient"}</small></div><button aria-label="Open account menu" onClick={() => setProfileOpen((open) => !open)}><ChevronDown size={16} /></button>{profileOpen && <div className="profile-menu"><button onClick={() => { onNavigate("Patients"); setProfileOpen(false); }}><UserRound size={14} />My Profile</button><button onClick={() => { onNavigate("Settings"); setProfileOpen(false); }}><Settings size={14} />Settings</button><button className="logout" onClick={onLogout}><LogOut size={14} />Logout</button></div>}</div></aside>;
}

export default Sidebar;
