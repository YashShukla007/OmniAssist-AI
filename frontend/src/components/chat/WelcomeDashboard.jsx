import { domains } from "../../constants/domains";
import { useDomain } from "../../context/DomainContext";

function WelcomeDashboard() {
  const { setSelectedDomain } = useDomain();

  return (
    <div className="max-w-5xl mx-auto p-10">
      <h1 className="text-5xl font-bold">
        Welcome to OmniAssist AI
      </h1>

      <p className="mt-4 text-slate-400 text-lg">
        Choose a domain to begin your conversation.
      </p>

      <div className="grid grid-cols-2 gap-6 mt-12">
        {domains.map((domain) => {
          const Icon = domain.icon;

          return (
            <button
              key={domain.id}
              onClick={() => setSelectedDomain(domain.name)}
              className="rounded-2xl border border-slate-700 bg-slate-900 hover:border-cyan-400 hover:scale-[1.02] transition-all duration-300 p-6 text-left"
            >
              <Icon
                size={36}
                className="text-cyan-400 mb-5"
              />

              <h2 className="text-2xl font-semibold">
                {domain.name}
              </h2>

              <p className="text-slate-400 mt-3">
                {domain.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default WelcomeDashboard;