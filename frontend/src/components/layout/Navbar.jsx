import { useRef, useState } from "react";
import { Bell, ChevronDown, HeartPulse, Moon, Search, Sun } from "lucide-react";
import { useDomain } from "../../context/DomainContext";
import { useTheme } from "../../context/ThemeContext";

const domains = ["Healthcare", "IT Helpdesk", "HR", "Finance", "Legal"];

function Navbar({ onNotice, onDomainUnavailable }) {
  const { selectedDomain, setSelectedDomain } = useDomain();
  const { theme, toggleTheme } = useTheme();
  const [domainOpen, setDomainOpen] = useState(false);
  const inputRef = useRef(null);

  function handleSearch(event) {
    if (event.key === "Enter" && event.currentTarget.value.trim()) onNotice(`Search for “${event.currentTarget.value.trim()}” is ready to connect to the global search API.`);
  }

  const chooseDomain = (domain) => {
    setDomainOpen(false);

    if (domain !== "Healthcare") {
      onDomainUnavailable(domain);
      return;
    }

    setSelectedDomain(domain);
    onNotice("Healthcare is your active integrated workspace.");
  };

  return <header className="topbar"><div className="domain-select-wrap"><button className="domain-selector" onClick={() => setDomainOpen((open) => !open)}><span className="domain-selector-icon"><HeartPulse size={12} /></span><div><small>Domain</small><strong>{selectedDomain || "Healthcare"}</strong></div><ChevronDown size={15} /></button>{domainOpen && <div className="domain-menu">{domains.map((domain) => <button key={domain} onClick={() => chooseDomain(domain)}>{domain}</button>)}</div>}</div><div className="search"><Search size={16} /><input ref={inputRef} onKeyDown={handleSearch} placeholder="Search anything..." /><button type="button" onClick={() => inputRef.current?.focus()} aria-label="Focus search"><kbd>Ctrl K</kbd></button></div><div className="topbar-actions"><button aria-label="Notifications" onClick={() => onNotice("You have 3 upcoming health reminders and 1 open escalation.")}><Bell size={18} /><i /></button><button className="theme-toggle" aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`} onClick={toggleTheme}>{theme === "light" ? <Moon size={18} /> : <Sun size={18} />}</button><span className="topbar-divider" /><div className="topbar-profile"><span className="avatar">YS</span><div><strong>Yash Shukla</strong><small>{sessionStorage.getItem("omniassist_role") ?? "Patient"}</small></div></div></div></header>;
}

export default Navbar;
