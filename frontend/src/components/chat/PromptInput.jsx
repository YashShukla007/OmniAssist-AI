import { useState } from "react";
import { SendHorizontal } from "lucide-react";

import api from "../../services/api";

import { useChat } from "../../context/ChatContext";
import { useDomain } from "../../context/DomainContext";

function PromptInput() {

  const [prompt, setPrompt] = useState("");

  const {
    addMessage,
    setIsTyping,
    conversationId,
  } = useChat();

  const { selectedDomain } = useDomain();

  async function handleSend() {

    if (!prompt.trim()) return;

    const userMessage = prompt;

    addMessage({
      role: "user",
      domain: selectedDomain,
      content: userMessage,
    });

    setPrompt("");

    setIsTyping(true);

    try {

      const response = await api.post("/chat", {
        conversation_id: conversationId,
        message: userMessage,
        domain: selectedDomain,
      });

      setIsTyping(false);

      addMessage({
        role: "assistant",
        domain: selectedDomain,
        content: response.data.answer,
        confidence: response.data.confidence,
        model: response.data.model,
      });

    } catch (error) {

      console.error(error);

      setIsTyping(false);

      addMessage({
        role: "assistant",
        domain: selectedDomain,
        content:
          "❌ Unable to connect to the backend.",
      });

    }

  }

  function handleKeyDown(e) {

    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }

  }

  return (

    <div className="border-t border-slate-800 bg-slate-900 p-6">

      <div className="flex items-center gap-4">

        <textarea
          rows={2}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Ask ${selectedDomain} anything...`}
          className="flex-1 rounded-xl bg-slate-800 p-4 resize-none outline-none"
        />

        <button
          onClick={handleSend}
          className="rounded-xl bg-cyan-500 hover:bg-cyan-600 transition p-4"
        >
          <SendHorizontal />
        </button>

      </div>

    </div>

  );

}

export default PromptInput;