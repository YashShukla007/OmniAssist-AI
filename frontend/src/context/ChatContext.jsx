import {
  createContext,
  useContext,
  useState,
  useEffect,
} from "react";

import { useDomain } from "./DomainContext";

import api from "../services/api";

const ChatContext = createContext();

export function ChatProvider({ children }) {

  const [conversations, setConversations] = useState([]);

  const [conversationId, setConversationId] = useState(null);

  const [isTyping, setIsTyping] = useState(false);

  const { setSelectedDomain } = useDomain();

  const currentConversation =
    conversations.find(
      (chat) => chat.id === conversationId
    ) ?? null;

  useEffect(() => {
    loadConversations();
  }, []);

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
          provider: message.provider ?? chat.provider,
          responseTime: message.responseTime ?? chat.responseTime,
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

      return active
        ? [active, ...others]
        : updated;

    });

  }

  async function newConversation() {

    try {

      const response = await api.post("/conversations/");

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

      setSelectedDomain("IT Helpdesk");

    } catch (error) {

      console.error(error);

    }

  }

  async function loadConversations() {

    try {

      const response = await api.get("/conversations/");

      const chats = response.data;

      if (chats.length === 0) {

        await newConversation();
        return;

      }

      const formatted = chats.map((chat) => ({
        id: chat.id,
        title: chat.title,
        domain: chat.domain,
        model: chat.model,
        provider: chat.provider,
        responseTime: chat.response_time,
        createdAt: new Date(chat.created_at),
        updatedAt: new Date(chat.updated_at),
        messages: chat.messages,
      }));

      setConversations(formatted);

      setConversationId(formatted[0].id);

      setSelectedDomain(formatted[0].domain);

    } catch (error) {

      console.error(error);

    }

  }

  async function fetchConversation(id) {

    try {

      const response = await api.get(
        `/conversations/${id}`
      );

      const conversation = response.data;

      setSelectedDomain(conversation.domain);

      setConversations((prev) =>
        prev.map((chat) => {

          if (chat.id !== id) return chat;

          return {
            ...chat,
            title: conversation.title,
            domain: conversation.domain,
            model: conversation.model,
            provider: conversation.provider,
            responseTime: conversation.response_time,
            createdAt: new Date(conversation.created_at),
            updatedAt: new Date(conversation.updated_at),
            messages: conversation.messages,
          };

        })
      );

    } catch (error) {

      console.error(error);

    }

  }

  async function selectConversation(id) {

    await fetchConversation(id);

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
        fetchConversation,
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