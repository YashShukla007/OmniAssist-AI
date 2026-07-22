import { createContext, useContext, useEffect, useState } from "react";

import { useDomain } from "./DomainContext";
import api from "../services/api";

const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [conversations, setConversations] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const { setSelectedDomain } = useDomain();

  const currentConversation =
    conversations.find((chat) => chat.id === conversationId) ?? null;

  function addMessage(message, targetConversationId = conversationId) {
    if (targetConversationId == null) return;
    setConversations((previous) =>
      previous.map((chat) => {
        if (chat.id !== targetConversationId) return chat;
        const title =
          chat.title === "New Chat" && message.role === "user"
            ? message.content.length > 30
              ? `${message.content.slice(0, 30)}...`
              : message.content
            : chat.title;
        return {
          ...chat,
          title,
          domain: message.domain ?? chat.domain,
          model: message.model ?? chat.model,
          provider: message.provider ?? chat.provider,
          responseTime: message.responseTime ?? chat.responseTime,
          updatedAt: new Date(),
          messages: [...(Array.isArray(chat.messages) ? chat.messages : []), message],
        };
      }),
    );
  }

  async function newConversation() {
    if (!localStorage.getItem("omniassist_token")) return undefined;
    try {
      const response = await api.post("/conversations/");
      const conversation = {
        id: response.data.conversation_id,
        title: "New Chat",
        domain: "Healthcare",
        model: null,
        provider: null,
        createdAt: new Date(),
        updatedAt: new Date(),
        messages: [],
      };
      setConversations((previous) => [conversation, ...previous]);
      setConversationId(conversation.id);
      setSelectedDomain("Healthcare");
      return conversation.id;
    } catch (error) {
      console.error(error);
      return undefined;
    }
  }

  async function loadConversations() {
    if (!localStorage.getItem("omniassist_token")) return undefined;
    try {
      const response = await api.get("/conversations/");
      const chats = response.data;
      if (chats.length === 0) return newConversation();
      const formatted = chats.map((chat) => ({
        id: chat.id,
        title: chat.title,
        domain: chat.domain ?? "Healthcare",
        model: chat.model,
        provider: chat.provider,
        responseTime: chat.response_time,
        createdAt: new Date(chat.created_at),
        updatedAt: new Date(chat.updated_at),
        messages: Array.isArray(chat.messages) ? chat.messages : [],
      }));
      setConversations(formatted);
      setConversationId(formatted[0].id);
      setSelectedDomain(formatted[0].domain);
      return formatted[0].id;
    } catch (error) {
      console.error(error);
      return undefined;
    }
  }

  async function fetchConversation(id) {
    try {
      const response = await api.get(`/conversations/${id}`);
      const conversation = response.data;
      setSelectedDomain(conversation.domain ?? "Healthcare");
      setConversations((previous) =>
        previous.map((chat) =>
          chat.id === id
            ? {
                ...chat,
                title: conversation.title,
                domain: conversation.domain ?? "Healthcare",
                model: conversation.model,
                provider: conversation.provider,
                responseTime: conversation.response_time,
                createdAt: new Date(conversation.created_at),
                updatedAt: new Date(conversation.updated_at),
                messages: Array.isArray(conversation.messages)
                  ? conversation.messages
                  : [],
              }
            : chat,
        ),
      );
    } catch (error) {
      console.error(error);
    }
  }

  async function selectConversation(id) {
    await fetchConversation(id);
    setConversationId(id);
  }

  async function ensureConversation() {
    if (!localStorage.getItem("omniassist_token")) return undefined;
    return conversationId ?? loadConversations();
  }

  useEffect(() => {
    const initialLoad = window.setTimeout(() => {
      void loadConversations();
    }, 0);
    return () => window.clearTimeout(initialLoad);
    // The initial conversation fetch intentionally runs once when the provider mounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ChatContext.Provider
      value={{
        conversations,
        currentConversation,
        conversationId,
        addMessage,
        newConversation,
        selectConversation,
        fetchConversation,
        ensureConversation,
        isTyping,
        setIsTyping,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useChat() {
  return useContext(ChatContext);
}
