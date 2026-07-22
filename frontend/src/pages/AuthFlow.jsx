import { useState } from "react";
import { ArrowLeft, Building2, HeartPulse, LockKeyhole, ShieldCheck, UserRound, Moon, Sun } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { Brand } from "./LandingPage";
import { useTheme } from "../context/ThemeContext";

const roles = [{ name: "Patient", description: "Access your health information, book appointments and more", icon: UserRound }];

function Field({ label, type = "text", placeholder, name, value, onChange, required = true }) {
  return <label className="form-field"><span>{label}</span><input name={name} type={type} value={value} onChange={onChange} placeholder={placeholder} required={required} /></label>;
}

function FormMessage({ message, error }) {
  return message ? <p className={`form-message ${error ? "is-error" : ""}`} role="alert">{message}</p> : null;
}

function LoginForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage("");
    try {
      const response = await api.post("/auth/login", form);
      localStorage.setItem("omniassist_token", response.data.access_token);
      const userResponse = await api.get("/auth/me");
      sessionStorage.setItem("omniassist_role", userResponse.data.role);
      sessionStorage.setItem("omniassist_username", userResponse.data.username);
      navigate("/dashboard", { replace: true });
    } catch (error) {
      setMessage(error.response?.data?.detail ?? "We could not sign you in. Check your details and backend connection.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return <section className="auth-card"><h1>Welcome Back!</h1><p>Login to continue to OmniAssist AI</p><form onSubmit={handleSubmit}><Field label="Email address" name="email" value={form.email} onChange={update} type="email" placeholder="you@example.com" /><Field label="Password" name="password" value={form.password} onChange={update} type="password" placeholder="Enter your password" /><div className="form-options"><label><input type="checkbox" /> Remember me</label><button type="button" className="text-button" onClick={() => setMessage("Password reset will be enabled when email delivery is configured.")}>Forgot Password?</button></div><FormMessage message={message} error /><button className="button button-primary form-button" disabled={isSubmitting}>{isSubmitting ? "Signing in..." : "Login"}</button><div className="or-divider">or</div><button type="button" className="button button-secondary form-button google-button" onClick={() => setMessage("Google sign-in requires OAuth credentials and is not configured yet.")}><span className="google-mark" aria-hidden="true">G</span>Continue with Google</button></form><p className="auth-switch">Don&apos;t have an account? <Link to="/register">Register</Link></p></section>;
}

function RegisterForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [acceptedTerms, setAcceptedTerms] = useState(false);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  async function handleSubmit(event) {
    event.preventDefault();
    if (form.password !== form.confirmPassword) return setMessage("Password and confirmation must match.");
    if (!acceptedTerms) return setMessage("Please accept the Terms & Conditions and Privacy Policy.");
    setIsSubmitting(true);
    setMessage("");
    try {
      await api.post("/auth/register", { username: form.username, email: form.email, password: form.password });
      navigate("/login", { replace: true });
    } catch (error) {
      setMessage(error.response?.data?.detail ?? "We could not create your account. Check your backend connection.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return <section className="auth-card auth-card-wide"><h1>Create Your Patient Account</h1><p>Patient accounts are available through public registration. Hospital Staff and Administrator access is provisioned by the hospital.</p><form onSubmit={handleSubmit}><Field label="Full name" name="username" value={form.username} onChange={update} placeholder="Enter your full name" /><Field label="Email" name="email" value={form.email} onChange={update} type="email" placeholder="you@example.com" /><Field label="Password" name="password" value={form.password} onChange={update} type="password" placeholder="At least 8 characters" /><Field label="Confirm Password" name="confirmPassword" value={form.confirmPassword} onChange={update} type="password" placeholder="Repeat your password" /><label className="terms"><input type="checkbox" checked={acceptedTerms} onChange={(event) => setAcceptedTerms(event.target.checked)} /> I agree to the <button type="button" className="text-button" onClick={() => setMessage("Terms will be added before public release.")}>Terms & Conditions</button> and <button type="button" className="text-button" onClick={() => setMessage("Privacy policy will be added before public release.")}>Privacy Policy</button></label><FormMessage message={message} error /><button className="button button-primary form-button" disabled={isSubmitting}>{isSubmitting ? "Creating account..." : "Register as Patient"}</button></form><p className="auth-switch">Already have an account? <Link to="/login">Login</Link></p></section>;
}

function RoleSelection() {
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState(sessionStorage.getItem("omniassist_registration_role") ?? "Patient");
  return <section className="role-selection"><p className="auth-kicker">Continue as</p><h1>Patient account sign-in</h1><div className="role-list">{roles.map(({ name, description, icon: Icon }) => <button key={name} className={selectedRole === name ? "selected" : ""} onClick={() => setSelectedRole(name)}><span><Icon size={25} /></span><div><strong>{name}</strong><small>{description}</small></div>{selectedRole === name && <ShieldCheck size={18} />}</button>)}</div><button className="button button-primary role-continue" onClick={() => { sessionStorage.setItem("omniassist_role", selectedRole); navigate("/login"); }}>Continue to secure login</button></section>;
}

function AuthFlow({ mode }) {
  const { theme, toggleTheme } = useTheme();
  const form = mode === "login" ? <LoginForm /> : mode === "register" ? <RegisterForm /> : <RoleSelection />;
  return <main className="auth-page"><header><Brand /><div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}><button className="theme-toggle-btn" aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`} onClick={toggleTheme}>{theme === "light" ? <Moon size={16} /> : <Sun size={16} />}</button><Link className="back-link" to="/"><ArrowLeft size={16} /> Back to website</Link></div></header><div className="auth-layout"><aside className="auth-aside"><span className="aside-icon"><HeartPulse size={32} /></span><h2>Care, coordinated by intelligent workflows.</h2><p>Bring conversations, documents, appointments, and trusted AI assistance into one secure workspace.</p><div className="aside-points"><span><LockKeyhole size={16} /> Built for secure teams</span><span><Building2 size={16} /> Multi-domain by design</span></div></aside><div className="auth-content">{form}</div></div></main>;
}

export default AuthFlow;
