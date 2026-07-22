import { useChat } from "../../context/ChatContext";
import { WorkflowMap } from "../dashboard/HealthcareOperations";
import WelcomeDashboard from "./WelcomeDashboard";
import MessageBubble from "./MessageBubble";

function ChatArea({ compact = false }) {
  const { currentConversation, isTyping } = useChat();
  const messages = currentConversation?.messages ?? [];
  const latestWorkflow = [...messages].reverse().find((message) => message.workflow)?.workflow;

  if (messages.length === 0) {
    return <div className="flex-1 overflow-y-auto">{compact ? <AssistantEmptyState /> : <WelcomeDashboard />}</div>;
  }

  return <div className={`chat-area ${compact ? "chat-area-compact" : ""} overflow-y-auto`}>
    {messages.map((message, index) => <MessageBubble key={index} message={message} />)}
    {isTyping && <div className="mt-4 text-slate-400 italic">AgentCare is processing your request...</div>}
    {compact && latestWorkflow && <section className="chat-workflow-live"><h2>Live Agent Workflow</h2><WorkflowMap workflow={latestWorkflow} /></section>}
  </div>;
}

function AssistantEmptyState() {
  return <div className="assistant-empty"><div className="assistant-request">Send an administrative request, such as a Cardiology appointment with an attached ECG report.</div><div className="assistant-progress"><span>♡</span><div><strong>AgentCare is ready</strong><small>Your real persisted workflow will appear here after the request is processed.</small></div></div></div>;
}

export default ChatArea;
