export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-12 text-slate-100">
      <div className="mx-auto w-full max-w-3xl rounded-3xl border border-slate-700/60 bg-slate-950/70 p-10 shadow-2xl shadow-cyan-950/20 backdrop-blur">
        <p className="text-sm font-medium uppercase tracking-[0.35em] text-cyan-300">
          ResearchMind AI
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight text-white md:text-6xl">
          A clean foundation for a research-focused RAG product.
        </h1>
        <p className="mt-6 max-w-2xl text-base leading-7 text-slate-300 md:text-lg">
          This frontend is wired for the production scaffold only: Next.js,
          TypeScript, Tailwind CSS, and App Router are ready for the next phase.
        </p>
        <div className="mt-8 inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-200">
          Frontend service is running
        </div>
      </div>
    </main>
  );
}