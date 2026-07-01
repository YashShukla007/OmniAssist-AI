import { useState } from "react";
import { Copy, Check } from "lucide-react";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function CodeBlock({
  language,
  value,
}) {

  const [copied, setCopied] = useState(false);

  async function copyCode() {

    try {

      await navigator.clipboard.writeText(value);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);

    } catch (error) {

      console.error(error);

    }

  }

  return (

    <div className="rounded-xl overflow-hidden border border-slate-700 my-5">

      <div className="flex justify-between items-center bg-slate-800 px-4 py-2">

        <span className="text-xs uppercase tracking-wide text-slate-300">
          {language}
        </span>

        <button
          onClick={copyCode}
          className="flex items-center gap-2 text-sm hover:text-cyan-400 transition"
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

      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          padding: "18px",
          fontSize: "14px",
        }}
      >
        {value}
      </SyntaxHighlighter>

    </div>

  );

}

export default CodeBlock;