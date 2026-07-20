import { useChat } from "../../context/ChatContext";

import WelcomeDashboard from "./WelcomeDashboard";
import MessageBubble from "./MessageBubble";

function ChatArea({ compact = false }) {

  const {
    currentConversation,
    isTyping,
  } = useChat();

  const messages = currentConversation?.messages ?? [];

  // Show Welcome Dashboard when there are no messages
  if (messages.length === 0) {
    return (
      <div className="flex-1 overflow-y-auto">
        {compact ? <AssistantEmptyState /> : <WelcomeDashboard />}
      </div>
    );
  }

  return (
    <div className={`chat-area ${compact ? "chat-area-compact" : ""}`}>

      {messages.map((message, index) => (
        <MessageBubble
          key={index}
          message={message}
        />
      ))}

      {isTyping && (
        <div className="mt-4 text-slate-400 italic">
          OmniAssist AI is typing...
        </div>
      )}

    </div>
  );
}

function AssistantEmptyState() {
  return <div className="assistant-empty"><div className="assistant-request">I need a cardiology appointment next week.<br />Also I want to upload my ECG report.</div><div className="assistant-progress"><span>♡</span><div><strong>AI Assistant is ready to help</strong><small>Ask a question or start a workflow below.</small></div></div><div className="agent-workflow"><div className="section-heading"><strong>Agent Workflow</strong><button>View Details →</button></div>{["Coordinator Agent", "Routing Agent", "Appointment Agent", "Document Agent", "Reminder Agent", "Safety Agent"].map((agent, index) => <div className="workflow-line" key={agent}><i /> <div><strong>{agent}</strong><small>{index === 0 ? "Goal received and workflow created" : "Ready when your request is sent"}</small></div><time>10:30:{11 + index}</time></div>)}</div></div>;
}

export default ChatArea;
