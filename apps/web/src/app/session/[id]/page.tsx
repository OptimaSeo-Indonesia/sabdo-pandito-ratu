"use client";

import { useParams } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import {
  getDeliberationStatus,
  getDeliberationReport,
} from "@/lib/api";
import type { DeliberationStatus, FullReport } from "@/types/api";

const STEP_LABELS: Record<string, string> = {
  analyze_context: "Analyze Context",
  generate_perspectives: "Generate Perspectives",
  collect_arguments: "Collect Arguments",
  resolve_conflicts: "Resolve Conflicts",
  evaluate_principles: "Evaluate Principles",
  explore_scenarios: "Explore Scenarios",
  reflect: "Reflect",
  score_wisdom: "Score Wisdom",
  generate_verdict: "Generate Verdict",
};

function Spinner() {
  return (
    <div className="flex items-center gap-2 text-gray-500">
      <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      <span>Processing...</span>
    </div>
  );
}

function ProgressSteps({ steps }: { steps: Array<{ name: string; status: string }> }) {
  return (
    <div className="mb-6">
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">Progress</h3>
      <div className="space-y-2">
        {steps.map((s) => {
          const isActive = s.status === "in_progress" || s.status === "completed";
          const isDone = s.status === "completed";
          return (
            <div key={s.name} className="flex items-center gap-3">
              <div
                className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                  isDone
                    ? "bg-green-500 text-white"
                    : isActive
                      ? "border-2 border-blue-500 text-blue-500"
                      : "border-2 border-gray-300 text-gray-400"
                }`}
              >
                {isDone ? "✓" : isActive ? "●" : "○"}
              </div>
              <span className={isDone ? "text-gray-900" : isActive ? "text-blue-700" : "text-gray-400"}>
                {STEP_LABELS[s.name] || s.name}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function AdvisorTable({ advisors }: { advisors: DeliberationStatus["advisor_statuses"] }) {
  return (
    <div className="mb-6">
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">Advisor Perspectives</h3>
      <div className="overflow-x-auto rounded border">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 font-medium">Persona</th>
              <th className="px-4 py-2 font-medium">Stance</th>
              <th className="px-4 py-2 font-medium">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {advisors.map((a) => (
              <tr key={a.persona} className="border-t">
                <td className="px-4 py-2 font-medium capitalize">{a.persona.replace(/_/g, " ")}</td>
                <td className="px-4 py-2 capitalize">{a.stance.replace(/_/g, " ")}</td>
                <td className="px-4 py-2">{Math.round(a.confidence * 100)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function WisdomBadge({ score }: { score: number | null | undefined }) {
  if (score == null) return null;
  const color = score >= 70 ? "bg-green-100 text-green-800" : score >= 50 ? "bg-yellow-100 text-yellow-800" : "bg-red-100 text-red-800";
  return (
    <span className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ${color}`}>
      Wisdom Score: {score}/100
    </span>
  );
}

function VerdictCard({ status }: { status: DeliberationStatus }) {
  if (!status.verdict) return null;
  const v = status.verdict;
  return (
    <div className="mb-6 rounded-lg border bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-bold">Verdict</h2>
        <WisdomBadge score={v.wisdom_score} />
      </div>
      <div className="mb-3 flex items-center gap-3">
        <span className="rounded bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-800">
          {v.decision}
        </span>
        <span className="text-sm text-gray-500">Confidence: {Math.round(v.confidence * 100)}%</span>
      </div>
      <p className="text-gray-700">{v.summary}</p>
    </div>
  );
}

function ReportSection({ report }: { report: FullReport }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="mb-6 rounded-lg border bg-white shadow-sm">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between px-6 py-4 text-left font-semibold hover:bg-gray-50"
      >
        <span>Full Deliberation Report</span>
        <span className="text-gray-400">{open ? "▲" : "▼"}</span>
      </button>
      {open && (
        <div className="border-t px-6 py-4">
          {report.verdict.wisdom_score && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Wisdom Score Breakdown</h4>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {Object.entries(report.verdict.wisdom_score).filter(([k]) => k !== "overall").map(([k, v]) => (
                  <div key={k} className="flex justify-between rounded bg-gray-50 px-3 py-2">
                    <span className="capitalize text-gray-600">{k.replace(/_/g, " ")}</span>
                    <span className="font-medium">{String(v)}/100</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {report.principle_evaluations.length > 0 && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Principle Evaluations</h4>
              <div className="space-y-2">
                {report.principle_evaluations.map((p) => (
                  <div key={p.principle} className="rounded border p-3 text-sm">
                    <div className="mb-1 flex items-center justify-between">
                      <span className="font-medium capitalize">{p.principle.replace(/_/g, " ")}</span>
                      <span className="text-gray-500">{p.score}/10</span>
                    </div>
                    <p className="text-gray-600">{p.rationale}</p>
                    {p.concerns.length > 0 && (
                      <ul className="mt-1 list-disc pl-4 text-gray-500">
                        {p.concerns.map((c) => <li key={c}>{c}</li>)}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {report.scenario_explorations.length > 0 && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Scenario Exploration</h4>
              <div className="space-y-2">
                {report.scenario_explorations.map((s) => (
                  <div key={s.name} className="rounded border p-3 text-sm">
                    <div className="mb-1 flex items-center gap-2">
                      <span className="font-medium">{s.name}</span>
                      <span className="text-gray-500">({s.horizon})</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {report.conflicts.length > 0 && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Conflicts</h4>
              <div className="space-y-2">
                {report.conflicts.map((c) => (
                  <div key={c.description} className="rounded border p-3 text-sm">
                    <div className="mb-1 flex items-center gap-2">
                      <span className="font-medium capitalize">{c.type.replace(/_/g, " ")}</span>
                      <span className="text-gray-500">between {c.between.join(", ")}</span>
                    </div>
                    <p className="text-gray-600">{c.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {report.recommendations.length > 0 && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Recommendations</h4>
              <ul className="list-disc pl-5 text-sm text-gray-700">
                {report.recommendations.map((r) => <li key={r}>{r}</li>)}
              </ul>
            </div>
          )}

          {report.reasoning.key_factors.length > 0 && (
            <div className="mb-6">
              <h4 className="mb-2 font-semibold text-gray-700">Key Factors</h4>
              <ul className="list-disc pl-5 text-sm text-gray-700">
                {report.reasoning.key_factors.map((f) => <li key={f}>{f}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
      <h2 className="mb-2 text-lg font-bold">Error</h2>
      <p>{message}</p>
    </div>
  );
}

export default function SessionPage() {
  const params = useParams();
  const sessionId = params.id as string;
  const [status, setStatus] = useState<DeliberationStatus | null>(null);
  const [report, setReport] = useState<FullReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;

    let cancelled = false;
    let pollTimer: ReturnType<typeof setTimeout>;

    async function poll() {
      try {
        const s = await getDeliberationStatus(sessionId);
        if (cancelled) return;
        setStatus(s);
        if (s.status === "completed" || s.status === "failed") {
          if (s.status === "completed") {
            const r = await getDeliberationReport(sessionId);
            if (!cancelled) setReport(r);
          }
          return;
        }
        pollTimer = setTimeout(poll, 2000);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unknown error");
        }
      }
    }

    poll();
    return () => {
      cancelled = true;
      clearTimeout(pollTimer);
    };
  }, [sessionId]);

  if (error) return <ErrorState message={error} />;
  if (!status) return <div className="py-12 text-center"><Spinner /></div>;

  const isRunning = status.status !== "completed" && status.status !== "failed";

  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      <header className="mb-8">
        <h1 className="mb-1 text-2xl font-bold">Deliberation Session</h1>
        <p className="text-gray-600">{status.question}</p>
        <p className="mt-1 text-xs text-gray-400">Session: {sessionId}</p>
      </header>

      {isRunning && <ProgressSteps steps={status.progress.steps} />}
      {isRunning && <Spinner />}

      {status.status === "failed" && (
        <ErrorState message={status.error || "Deliberation failed"} />
      )}

      {status.status === "completed" && (
        <>
          <ProgressSteps steps={status.progress.steps} />
          <VerdictCard status={status} />
          <AdvisorTable advisors={status.advisor_statuses} />
          {report && <ReportSection report={report} />}
        </>
      )}
    </main>
  );
}
