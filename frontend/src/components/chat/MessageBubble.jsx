import { useState } from "react";
import { Bot, Cpu, Copy, Check } from "lucide-react";

import MarkdownRenderer from "./MarkdownRenderer";
import { useTheme } from "../../context/ThemeContext";

function MessageBubble({ message }) {

  const isUser = message.role === "user";
  const { theme } = useTheme();

  const [copied, setCopied] = useState(false);

  async function copyResponse() {

    try {

      await navigator.clipboard.writeText(
        message.content
      );

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);

    } catch (error) {

      console.error(error);

    }

  }

  return (

    <div
      className={`mb-8 flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`max-w-4xl rounded-2xl ${
          isUser
            ? "bg-cyan-500 text-white px-6 py-4"
            : theme === "dark"
              ? "bg-slate-800 border border-slate-700 text-slate-100"
              : "bg-white border border-slate-200 text-slate-800 shadow-sm"
        }`}
      >

        {isUser ? (

          <>
            <p className="text-sm opacity-80 mb-2">
              You
            </p>

            <p className="leading-7 whitespace-pre-wrap">
              {message.content}
            </p>
          </>

        ) : (

          <>

            {/* Header */}

            <div className={`flex items-center justify-between border-b px-6 py-4 ${theme === "dark" ? "border-slate-700" : "border-slate-100"}`}>

              <div className="flex items-center gap-3">

                <Bot
                  size={22}
                  className="text-cyan-500"
                />

                <div>

                  <h3 className="font-semibold">
                    OmniAssist AI
                  </h3>

                  <p className={`text-xs ${theme === "dark" ? "text-slate-400" : "text-slate-500"}`}>
                    Multi-Domain AI Assistant
                  </p>

                </div>

              </div>

              <button
                onClick={copyResponse}
                className={`flex items-center gap-2 text-sm transition ${theme === "dark" ? "text-slate-400 hover:text-cyan-400" : "text-slate-500 hover:text-cyan-600"}`}
              >

                {copied ? (
                  <>
                    <Check size={16} />
                    Copied
                  </>
                ) : (
                  <>
                    <Copy size={16} />
                    Copy
                  </>
                )}

              </button>

            </div>

            {/* Model & Confidence */}

            <div className={`flex flex-wrap gap-3 px-6 py-4 border-b ${theme === "dark" ? "border-slate-700" : "border-slate-100"}`}>

              <div className={`flex items-center gap-2 rounded-full px-3 py-1 text-sm ${theme === "dark" ? "bg-slate-700 text-slate-200" : "bg-slate-100 text-slate-600"}`}>

                <Cpu size={15} />

                {message.model ?? "Unknown"}

              </div>

            </div>

            {/* Markdown */}

            <div className="px-6 py-5">

              <MarkdownRenderer
                content={message.content}
              />

            </div>

          </>

        )}

      </div>

    </div>

  );

}

export default MessageBubble;