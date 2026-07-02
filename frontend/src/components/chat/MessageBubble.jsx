import { useState } from "react";
import { Bot, Cpu, Copy, Check } from "lucide-react";

import MarkdownRenderer from "./MarkdownRenderer";

function MessageBubble({ message }) {

  const isUser = message.role === "user";

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
            : "bg-slate-800 border border-slate-700"
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

            <div className="flex items-center justify-between border-b border-slate-700 px-6 py-4">

              <div className="flex items-center gap-3">

                <Bot
                  size={22}
                  className="text-cyan-400"
                />

                <div>

                  <h3 className="font-semibold">
                    OmniAssist AI
                  </h3>

                  <p className="text-xs text-slate-400">
                    Multi-Domain AI Assistant
                  </p>

                </div>

              </div>

              <button
                onClick={copyResponse}
                className="flex items-center gap-2 text-sm text-slate-400 hover:text-cyan-400 transition"
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

            <div className="flex flex-wrap gap-3 px-6 py-4 border-b border-slate-700">

              <div className="flex items-center gap-2 rounded-full bg-slate-700 px-3 py-1 text-sm">

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