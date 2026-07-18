import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { startDeliberation, startDryRun } from "../lib/api";

export default function Home() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [useDryRun, setUseDryRun] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const fn = useDryRun ? startDryRun : startDeliberation;
      const result = await fn(question);
      navigate(`/session/${result.session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      <header className="mb-12 text-center">
        <h1 className="mb-2 text-4xl font-bold">Sabdo Pandito Ratu</h1>
        <p className="text-lg text-gray-600">
          Multi-AI Deliberation Engine — Ask a question, get a reasoned verdict
        </p>
      </header>

      <section className="mb-8 rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">Submit a Question</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={4}
            className="mb-4 w-full rounded border p-3 text-sm"
            placeholder="Ask a question for the council of AI advisors..."
          />
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm text-gray-600">
              <input
                type="checkbox"
                checked={useDryRun}
                onChange={(e) => setUseDryRun(e.target.checked)}
                className="rounded"
              />
              Dry run (no LLM calls)
            </label>
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Submitting..." : "Deliberate"}
            </button>
          </div>
          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
        </form>
      </section>

      <section className="rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-3 text-lg font-semibold">How It Works</h2>
        <ol className="list-inside list-decimal space-y-2 text-sm text-gray-600">
          <li><strong>Submit</strong> your question to the council of 6 AI advisors</li>
          <li>The system <strong>analyzes</strong> context, generates perspectives, and detects conflicts</li>
          <li>Advisors <strong>debate</strong> across 5 ethical principles and 12 scenarios</li>
          <li>The system <strong>reflects</strong> on blind spots and scores wisdom</li>
          <li>You receive a <strong>reasoned verdict</strong> with full transparency</li>
        </ol>
      </section>
    </main>
  );
}
