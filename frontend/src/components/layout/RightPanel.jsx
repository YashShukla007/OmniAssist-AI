import { Activity, BrainCircuit, Database, Gauge, Sparkles } from "lucide-react";
import { useChat } from "../../context/ChatContext";

function Insight({ icon: Icon, label, value, accent = "blue", children }) { return <article className="insight"><span className={`insight-icon ${accent}`}><Icon size={15} /></span><div><small>{label}</small><strong>{value}</strong>{children}</div></article>; }

function RightPanel({ onNavigate, onNotice }) {
  const { currentConversation } = useChat();
  const activeModel = currentConversation?.model ?? "Qwen2.5-72B-Instruct";
  return <aside className="insights-panel"><h2>AI Insights</h2><Insight icon={BrainCircuit} label="Model" value={activeModel} accent="violet" /><Insight icon={Gauge} label="Response Time" value={currentConversation?.responseTime ? `${currentConversation.responseTime}s` : "1.23 sec"} accent="green" /><Insight icon={Activity} label="Confidence Score" value="96%" accent="green"><span className="confidence"><i /></span></Insight><Insight icon={Database} label="Tokens Used" value="1,265" accent="purple" /><Insight icon={Sparkles} label="Workflow Status" value="Completed" accent="green" /><Insight icon={Database} label="Data Source" value="Hospital DB" accent="blue" /><article className="quick-explain"><h3>Quick Explain</h3><p>The system routed your request to Cardiology and booked the earliest available slot based on your preference.</p><button onClick={() => { onNavigate("Chat Assistant"); onNotice("The assistant can now explain the active workflow in detail."); }}>Explain More →</button></article></aside>;
}

export default RightPanel;
