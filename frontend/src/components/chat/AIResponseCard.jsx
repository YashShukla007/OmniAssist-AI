function AIResponseCard() {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900 p-6">

      <h2 className="text-xl font-bold text-cyan-400">
        OmniAssist AI
      </h2>

      <div className="mt-6">

        <h3 className="font-semibold text-lg">
          📌 Summary
        </h3>

        <p className="mt-2 text-slate-300">
          Summary will appear here.
        </p>

      </div>

      <div className="mt-8">

        <h3 className="font-semibold text-lg">
          ✅ Steps
        </h3>

        <ul className="mt-3 space-y-2">

          <li>Step 1</li>
          <li>Step 2</li>
          <li>Step 3</li>

        </ul>

      </div>

      <div className="mt-8">

        <h3 className="font-semibold text-lg">
          ⚠ Important Notes
        </h3>

      </div>

      <div className="mt-8">

        <h3 className="font-semibold text-lg">
          💡 Tips
        </h3>

      </div>

    </div>
  );
}

export default AIResponseCard;