import { Cpu, Activity, Clock, FolderOpen } from "lucide-react";
import { useDomain } from "../../context/DomainContext";

function RightPanel() {
  const { selectedDomain } = useDomain();

  return (
    <div className="h-full bg-slate-900 p-6">
      <h2 className="text-2xl font-bold mb-8">
        AI Insights
      </h2>

      <div className="space-y-5">

        {/* Domain */}
        <div className="rounded-2xl bg-slate-800 p-5">
          <div className="flex items-center gap-3 mb-2">
            <FolderOpen className="text-cyan-400" size={20} />
            <h3 className="font-semibold">Selected Domain</h3>
          </div>

          <p className="text-slate-300">
            {selectedDomain}
          </p>
        </div>

        {/* Model */}
        <div className="rounded-2xl bg-slate-800 p-5">
          <div className="flex items-center gap-3 mb-2">
            <Cpu className="text-cyan-400" size={20} />
            <h3 className="font-semibold">Active Model</h3>
          </div>

          <p className="text-slate-300">
            Qwen2.5-1.5B (Coming Soon)
          </p>
        </div>

        {/* Confidence */}
        <div className="rounded-2xl bg-slate-800 p-5">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="text-green-400" size={20} />
            <h3 className="font-semibold">Confidence</h3>
          </div>

          <p className="text-slate-300">
            Waiting for first response...
          </p>
        </div>

        {/* Response Time */}
        <div className="rounded-2xl bg-slate-800 p-5">
          <div className="flex items-center gap-3 mb-2">
            <Clock className="text-yellow-400" size={20} />
            <h3 className="font-semibold">Response Time</h3>
          </div>

          <p className="text-slate-300">
            --
          </p>
        </div>

      </div>
    </div>
  );
}

export default RightPanel;