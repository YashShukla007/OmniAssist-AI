import { useChat } from "../../context/ChatContext";

function Sidebar() {

  const { newConversation } = useChat();

  return (
    <aside className="w-72 bg-slate-900 border-r border-slate-800 h-screen flex flex-col">

      {/* Logo */}
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-cyan-400">
          OmniAssist AI
        </h1>

        <p className="text-sm text-slate-400 mt-2">
          One AI. Multiple Expert Domains.
        </p>
      </div>

      {/* New Chat */}
      <div className="p-4">
        <button
          onClick={newConversation}
          className="w-full rounded-xl bg-cyan-500 hover:bg-cyan-600 transition-all p-3 font-medium"
        >
          + New Chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 px-4">

        <p className="text-xs uppercase text-slate-500 mb-4">
          Recent Chats
        </p>

        <div className="space-y-2">

          <button className="w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">
            Password Reset
          </button>

          <button className="w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">
            Leave Policy
          </button>

          <button className="w-full rounded-lg bg-slate-800 p-3 text-left hover:bg-slate-700">
            Medical Insurance
          </button>

        </div>

      </div>

      {/* Footer */}
      <div className="border-t border-slate-800 p-4">

        <button className="w-full rounded-lg bg-slate-800 p-3 hover:bg-slate-700">
          ⚙ Settings
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;