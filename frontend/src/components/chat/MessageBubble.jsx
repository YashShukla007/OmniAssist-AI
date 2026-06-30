function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`mb-6 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-3xl rounded-2xl px-6 py-4 ${
          isUser
            ? "bg-cyan-500 text-white"
            : "bg-slate-800 text-white border border-slate-700"
        }`}
      >
        <p className="text-sm opacity-70 mb-2">
          {isUser ? "You" : "OmniAssist AI"}
        </p>

        <p className="leading-7 whitespace-pre-wrap">
          {message.content}
        </p>
      </div>
    </div>
  );
}

export default MessageBubble;