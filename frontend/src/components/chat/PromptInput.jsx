import { useRef, useState } from "react";
import { Paperclip, SendHorizontal, X } from "lucide-react";

import api from "../../services/api";
import { useChat } from "../../context/ChatContext";
import { useDomain } from "../../context/DomainContext";

// 60 second timeout for heavy LLM models
const WORKFLOW_TIMEOUT_MS = 60_000;

function PromptInput({ compact = false, onHealthcareUpdated }) {
  const [prompt, setPrompt] = useState("");
  const [attachment, setAttachment] = useState(null);
  const fileInputRef = useRef(null);
  const { addMessage, ensureConversation, setIsTyping, conversationId, isTyping } = useChat();
  const { selectedDomain } = useDomain();

  async function handleSend() {
    if ((!prompt.trim() && !attachment) || isTyping) return;
    const userMessage = prompt.trim() || "Please coordinate the attached document.";
    let activeConversationId = null;
    const abortController = new AbortController();
    const timeoutId = window.setTimeout(() => abortController.abort(), WORKFLOW_TIMEOUT_MS);

    try {
      activeConversationId = await ensureConversation();
      if (!activeConversationId) throw new Error("A chat session could not be created. Please sign in again.");

      addMessage({ role: "user", domain: selectedDomain, content: userMessage }, activeConversationId);
      setPrompt("");
      setAttachment(null);
      setIsTyping(true);

      let documentIds = [];
      let uploadedDocument = null;
      if (selectedDomain === "Healthcare" && attachment) {
        const formData = new FormData();
        formData.append("file", attachment);
        const uploadResponse = await api.post("/healthcare/documents", formData, { signal: abortController.signal });
        documentIds = [uploadResponse.data.id];
        uploadedDocument = uploadResponse.data;
      }

      const response = selectedDomain === "Healthcare"
        ? await api.post("/healthcare/workflows", { request: userMessage, document_ids: documentIds }, { signal: abortController.signal })
        : await api.post("/chat", { conversation_id: activeConversationId, message: userMessage, domain: selectedDomain }, { signal: abortController.signal });

      addMessage({
        role: "assistant",
        content: selectedDomain === "Healthcare" ? response.data.summary : response.data.answer,
        domain: selectedDomain,
        model: selectedDomain === "Healthcare" ? "AgentCare workflow" : response.data.model,
        provider: selectedDomain === "Healthcare" ? "Multi-agent orchestration" : response.data.provider,
        responseTime: selectedDomain === "Healthcare" ? null : response.data.response_time,
        workflow: selectedDomain === "Healthcare" ? response.data : undefined,
      }, activeConversationId);

      if (selectedDomain === "Healthcare") void onHealthcareUpdated?.({ document: uploadedDocument, workflow: response.data });
    } catch (error) {
      const isAborted = error.name === "AbortError" || error.code === "ERR_CANCELED";
      const message = isAborted
        ? "The request timed out. The AI model is taking longer than usual — please try again."
        : (error.response?.data?.detail ?? error.message ?? "Unable to complete this request.");
      console.error("[PromptInput] send error:", error);
      const targetId = activeConversationId ?? conversationId;
      if (targetId) {
        addMessage({ role: "assistant", domain: selectedDomain, content: message }, targetId);
      }
    } finally {
      window.clearTimeout(timeoutId);
      setIsTyping(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSend();
    }
  }

  return <div className={`prompt-input ${compact ? "prompt-input-compact" : ""}`}>
    {attachment && <div className="prompt-attachment"><Paperclip size={13} /><span>{attachment.name}</span><button type="button" onClick={() => setAttachment(null)} aria-label="Remove attached file"><X size={13} /></button></div>}
    <div className="prompt-input-row">
      {selectedDomain === "Healthcare" && <><input ref={fileInputRef} className="visually-hidden" type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={(event) => setAttachment(event.target.files?.[0] ?? null)} /><button type="button" className="prompt-attach" onClick={() => fileInputRef.current?.click()} aria-label="Attach healthcare document"><Paperclip size={16} /></button></>}
      <textarea rows={2} value={prompt} onChange={(event) => setPrompt(event.target.value)} onKeyDown={handleKeyDown} placeholder={`Ask ${selectedDomain} anything...`} className="prompt-textarea" />
      <button onClick={() => void handleSend()} className="prompt-send" disabled={isTyping} aria-label="Send request"><SendHorizontal /></button>
    </div>
  </div>;
}

export default PromptInput;
