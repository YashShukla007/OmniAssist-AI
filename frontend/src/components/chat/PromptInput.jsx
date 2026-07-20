import { useRef, useState } from "react";
import { Paperclip, SendHorizontal, X } from "lucide-react";

import api from "../../services/api";

import { useChat } from "../../context/ChatContext";
import { useDomain } from "../../context/DomainContext";

function PromptInput({ compact = false, onHealthcareUpdated }) {

  const [prompt, setPrompt] = useState("");
  const [attachment, setAttachment] = useState(null);
  const fileInputRef = useRef(null);

  const {
    addMessage,
    setIsTyping,
    conversationId,
    isTyping,
  } = useChat();

  const { selectedDomain } = useDomain();

  async function handleSend() {

    if ((!prompt.trim() && !attachment) || isTyping) return;

    const userMessage = prompt.trim() || "Please coordinate the attached document.";

    addMessage({
      role: "user",
      domain: selectedDomain,
      content: userMessage,
    });

    setPrompt("");

    setIsTyping(true);

    try {

      let documentIds = [];
      let uploadedDocument = null;
      if (selectedDomain === "Healthcare" && attachment) {
        const formData = new FormData();
        formData.append("file", attachment);
        const uploadResponse = await api.post("/healthcare/documents", formData);
        documentIds = [uploadResponse.data.id];
        uploadedDocument = uploadResponse.data;
      }

      const response = selectedDomain === "Healthcare"
        ? await api.post("/healthcare/workflows", { request: userMessage, document_ids: documentIds })
        : await api.post("/chat", {
          conversation_id: conversationId,
          message: userMessage,
          domain: selectedDomain,
        });

      setIsTyping(false);

      addMessage({
        role: "assistant",
        content: selectedDomain === "Healthcare" ? response.data.summary : response.data.answer,
        domain: selectedDomain,
        model: selectedDomain === "Healthcare" ? "AgentCare workflow" : response.data.model,
        provider: selectedDomain === "Healthcare" ? "Multi-agent orchestration" : response.data.provider,
        responseTime: selectedDomain === "Healthcare" ? null : response.data.response_time,
      });

      if (selectedDomain === "Healthcare") {
        void onHealthcareUpdated?.({ document: uploadedDocument, workflow: response.data });
      }
      setAttachment(null);

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

    <div className={`prompt-input ${compact ? "prompt-input-compact" : ""}`}>

      {attachment && <div className="prompt-attachment"><Paperclip size={13} /><span>{attachment.name}</span><button type="button" onClick={() => setAttachment(null)} aria-label="Remove attached file"><X size={13} /></button></div>}
      <div className="prompt-input-row">

        {selectedDomain === "Healthcare" && <><input ref={fileInputRef} className="visually-hidden" type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={(event) => setAttachment(event.target.files?.[0] ?? null)} /><button type="button" className="prompt-attach" onClick={() => fileInputRef.current?.click()} aria-label="Attach healthcare document"><Paperclip size={16} /></button></>}

        <textarea
          rows={2}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Ask ${selectedDomain} anything...`}
          className="prompt-textarea"
        />

        <button
          onClick={handleSend}
          className="prompt-send"
          disabled={isTyping}
          aria-label="Send request"
        >
          <SendHorizontal />
        </button>

      </div>

    </div>

  );

}

export default PromptInput;
