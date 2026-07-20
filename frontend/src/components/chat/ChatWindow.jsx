import Navbar from "../layout/Navbar";
import ChatArea from "./ChatArea";
import PromptInput from "./PromptInput";
import { useEffect } from "react";
import { useChat } from "../../context/ChatContext";

function ChatWindow({ showHeader = true, compact = false, onHealthcareUpdated }) {
  const { ensureConversation } = useChat();

  useEffect(() => {
    void ensureConversation();
    // The conversation bootstrap must run once; re-running on every chat state update can race uploads.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={`chat-window ${compact ? "chat-window-compact" : ""}`}>
      {showHeader && <Navbar />}

      <ChatArea compact={compact} />

      <PromptInput compact={compact} onHealthcareUpdated={onHealthcareUpdated} />
    </div>
  );
}

export default ChatWindow;
