import { useChat } from "../../context/ChatContext";

import WelcomeDashboard from "./WelcomeDashboard";
import MessageBubble from "./MessageBubble";

function ChatArea() {

  const {
    currentConversation,
    isTyping,
  } = useChat();

  const messages = currentConversation?.messages ?? [];

  // Show Welcome Dashboard when there are no messages
  if (messages.length === 0) {
    return (
      <div className="flex-1 overflow-y-auto">
        <WelcomeDashboard />
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-10 py-8">

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

export default ChatArea;