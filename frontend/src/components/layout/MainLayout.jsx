function MainLayout({ sidebar, chat, insights }) {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <div className="flex h-screen">

        {/* Sidebar */}
        <div>
          {sidebar}
        </div>

        {/* Chat */}
        <div className="flex-1">
          {chat}
        </div>

        {/* Right Panel */}
        <div className="w-80 border-l border-slate-800">
          {insights}
        </div>

      </div>

    </div>
  );
}

export default MainLayout;