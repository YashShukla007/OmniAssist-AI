import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {

  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const [conversationId, setConversationId] = useState(
    crypto.randomUUID()
  );

  function addMessage(message) {
    setMessages((prev) => [...prev, message]);
  }

  function clearChat() {
    setMessages([]);
  }

  function newConversation() {
    setMessages([]);
    setConversationId(
      crypto.randomUUID()
    );
  }

  return (
    <ChatContext.Provider
      value={{
        messages,
        addMessage,
        clearChat,
        isTyping,
        setIsTyping,
        conversationId,
        setConversationId,
        newConversation,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}