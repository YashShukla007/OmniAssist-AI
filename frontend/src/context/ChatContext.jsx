import { createContext, useContext, useState } from "react";
import api from "../services/api";

const ChatContext = createContext();

export function ChatProvider({ children }) {

  const createConversation = () => ({
    id: crypto.randomUUID(),
    title: "New Chat",
    domain: null,
    model: null,
    createdAt: new Date(),
    updatedAt: new Date(),
    messages: [],
  });

  const [conversations, setConversations] = useState([
    createConversation(),
  ]);

  const [conversationId, setConversationId] = useState(
    conversations[0].id
  );

  const [isTyping, setIsTyping] = useState(false);

  const currentConversation =
    conversations.find(
      (chat) => chat.id === conversationId
    ) || conversations[0];

  function addMessage(message) {

    setConversations((prev) => {

      const updated = prev.map((chat) => {

        if (chat.id !== conversationId) return chat;

        const updatedMessages = [
          ...chat.messages,
          message,
        ];

        const title =
          chat.title === "New Chat" &&
          message.role === "user"
            ? message.content.length > 30
              ? message.content.slice(0, 30) + "..."
              : message.content
            : chat.title;

        return {
          ...chat,
          title,
          domain: message.domain ?? chat.domain,
          model: message.model ?? chat.model,
          updatedAt: new Date(),
          messages: updatedMessages,
        };

      });

      const active = updated.find(
        (chat) => chat.id === conversationId
      );

      const others = updated.filter(
        (chat) => chat.id !== conversationId
      );

      return [
        active,
        ...others,
      ];

    });

  }

  async function newConversation() {

    try {

      const response = await api.post("/conversations");

      const conversation = {
        id: response.data.conversation_id,
        title: "New Chat",
        domain: null,
        model: null,
        createdAt: new Date(),
        updatedAt: new Date(),
        messages: [],
      };

      setConversations((prev) => [
        conversation,
        ...prev,
      ]);

      setConversationId(conversation.id);

    } catch (error) {

      console.error(error);

    }

  }

  function selectConversation(id) {
    setConversationId(id);
  }

  return (
    <ChatContext.Provider
      value={{
        conversations,
        currentConversation,
        conversationId,
        addMessage,
        newConversation,
        selectConversation,
        isTyping,
        setIsTyping,
      }}
    >
      {children}
    </ChatContext.Provider>
  );

}

export function useChat() {
  return useContext(ChatContext);
}