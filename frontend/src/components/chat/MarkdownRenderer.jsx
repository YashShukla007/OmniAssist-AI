import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import CodeBlock from "./CodeBlock";

function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code(props) {
          const {
            inline,
            className,
            children,
            ...rest
          } = props;

          const match = /language-(\w+)/.exec(
            className || ""
          );

          if (!inline && match) {
            return (
              <CodeBlock
                language={match[1]}
                value={String(children).replace(/\n$/, "")}
              />
            );
          }

          return (
            <code
              className="bg-slate-800 px-1 py-0.5 rounded"
              {...rest}
            >
              {children}
            </code>
          );
        },

        h1: ({ children }) => (
          <h1 className="text-3xl font-bold mb-4">
            {children}
          </h1>
        ),

        h2: ({ children }) => (
          <h2 className="text-2xl font-semibold mt-6 mb-3">
            {children}
          </h2>
        ),

        h3: ({ children }) => (
          <h3 className="text-xl font-semibold mt-4 mb-2">
            {children}
          </h3>
        ),

        p: ({ children }) => (
          <p className="leading-7 mb-4">
            {children}
          </p>
        ),

        ul: ({ children }) => (
          <ul className="list-disc ml-6 mb-4">
            {children}
          </ul>
        ),

        ol: ({ children }) => (
          <ol className="list-decimal ml-6 mb-4">
            {children}
          </ol>
        ),

        blockquote: ({ children }) => (
          <blockquote className="border-l-4 border-cyan-500 pl-4 italic my-4">
            {children}
          </blockquote>
        ),

        table: ({ children }) => (
          <table className="table-auto border border-slate-700 my-4">
            {children}
          </table>
        ),

        th: ({ children }) => (
          <th className="border border-slate-700 px-4 py-2 bg-slate-800">
            {children}
          </th>
        ),

        td: ({ children }) => (
          <td className="border border-slate-700 px-4 py-2">
            {children}
          </td>
        ),

        a: ({ children, href }) => (
          <a
            href={href}
            target="_blank"
            rel="noreferrer"
            className="text-cyan-400 underline"
          >
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}

export default MarkdownRenderer;