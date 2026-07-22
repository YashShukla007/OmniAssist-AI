import {
  ArrowRight,
  BadgeCheck,
  BrainCircuit,
  Building2,
  HeartPulse,
  Landmark,
  Laptop,
  Scale,
  ShieldCheck,
  UsersRound,
  Moon,
  Sun,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";

const domains = [
  { title: "Healthcare", text: "Patient care, appointments, records & more", icon: HeartPulse, accent: "teal" },
  { title: "IT Helpdesk", text: "Tickets, incidents, assets & more", icon: Laptop, accent: "blue" },
  { title: "HR", text: "Employee, leave, payroll & more", icon: UsersRound, accent: "orange" },
  { title: "Finance", text: "Accounts, reports, transactions & more", icon: Landmark, accent: "green" },
  { title: "Legal", text: "Cases, documents, compliance & more", icon: Scale, accent: "violet" },
];

function Brand({ dark = false }) {
  return (
    <Link className={`brand ${dark ? "brand-dark" : ""}`} to="/">
      <span className="brand-mark"><HeartPulse size={19} /></span>
      <span>OmniAssist AI</span>
    </Link>
  );
}

function LandingPage() {
  const { theme, toggleTheme } = useTheme();
  return (
    <main className="marketing-page">
      <nav className="marketing-nav">
        <Brand />
        <div className="marketing-links">
          <a href="#platform">Platform</a>
          <a href="#solutions">Solutions</a>
          <a href="#security">Resources</a>
          <a href="#about">About us</a>
        </div>
        <div className="nav-actions" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button className="theme-toggle-btn" aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`} onClick={toggleTheme}>
            {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
          </button>
          <Link className="button button-secondary" to="/login">Login</Link>
          <Link className="button button-primary" to="/register">Register</Link>
        </div>
      </nav>

      <section className="hero" id="platform">
        <div className="hero-copy">
          <p className="eyebrow"><span /> Enterprise AI orchestration</p>
          <h1>One Platform.<br />Every Domain.<br /><em>Infinite Possibilities.</em></h1>
          <p className="hero-description">OmniAssist AI is an enterprise AI platform that helps organisations automate workflows, make better decisions, and deliver exceptional experiences across their critical domains.</p>
          <ul className="benefit-list">
            <li><BadgeCheck /> AI-powered workflows</li>
            <li><BadgeCheck /> Multi-domain support</li>
            <li><BadgeCheck /> Secure &amp; compliant</li>
            <li><BadgeCheck /> Real-time intelligence</li>
          </ul>
          <div className="hero-actions">
            <Link className="button button-primary button-large" to="/register">Get Started <ArrowRight size={17} /></Link>
            <a className="button button-secondary button-large" href="#solutions">Explore domains</a>
          </div>
        </div>

        <div className="domain-orbit" aria-label="OmniAssist supported domains">
          <div className="orbit-ring ring-one" />
          <div className="orbit-ring ring-two" />
          <div className="orbit-core"><BrainCircuit size={54} /></div>
          {domains.map(({ title, text, icon: Icon, accent }, index) => (
            <article className={`domain-orbit-card card-${index + 1} accent-${accent}`} key={title}>
              <span><Icon size={23} /></span>
              <strong>{title}</strong>
              <small>{text}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="trust-strip" id="security">
        <div><UsersRound /><strong>10K+</strong><small>Active users</small></div>
        <div><Building2 /><strong>50+</strong><small>Enterprises</small></div>
        <div><BrainCircuit /><strong>5+</strong><small>Domains</small></div>
        <div><ShieldCheck /><strong>99.9%</strong><small>Uptime</small></div>
      </section>

      <section className="customer-strip" id="solutions">
        <p>Trusted by forward-thinking organisations</p>
        <div><span>◌ CityCare Hospital</span><span>◈ TechSolutions</span><span>◉ HealthFirst</span><span>◒ InnovaCorp</span><span>◍ LegalEase</span></div>
      </section>

      <section className="marketing-footer" id="about">
        <Brand />
        <p>One platform for responsible, practical enterprise AI.</p>
        <Link to="/dashboard">View product dashboard <ArrowRight size={15} /></Link>
      </section>
    </main>
  );
}

export { Brand };
export default LandingPage;
