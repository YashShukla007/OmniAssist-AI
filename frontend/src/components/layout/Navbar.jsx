import { Moon, GitCompareArrows, Cpu } from "lucide-react";
import { useDomain } from "../../context/DomainContext";

function Navbar() {
  const { selectedDomain } = useDomain();

  return (
    <header className="h-20 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-8">
      {/* Left */}
      <div className="flex items-center gap-4">
        <Cpu className="text-cyan-400" size={28} />

        <div>
          <h2 className="text-xl font-semibold">
            {selectedDomain} Assistant
          </h2>

          <p className="text-sm text-slate-400">
            Multi-Domain Enterprise AI
          </p>
        </div>
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        <button className="border border-slate-700 rounded-xl px-5 py-3 hover:bg-slate-800 transition">
          <GitCompareArrows
            size={18}
            className="inline mr-2"
          />
          Comparison Mode
        </button>

        <button className="rounded-full bg-slate-800 p-3 hover:bg-slate-700 transition">
          <Moon size={18} />
        </button>
      </div>
    </header>
  );
}

export default Navbar;