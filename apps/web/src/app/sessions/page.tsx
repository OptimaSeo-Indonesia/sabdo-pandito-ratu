"use client";

import { useEffect, useState } from "react";
import { listSessions, getSessionStats } from "@/lib/api";
import type { SessionListItem, SessionStats } from "@/types/api";

export default function SessionsPage() {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [stats, setStats] = useState<SessionStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, st] = await Promise.all([
          listSessions(),
          getSessionStats(),
        ]);
        setSessions(s.items);
        setStats(st);
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      <header className="mb-8">
        <h1 className="text-2xl font-bold">Session History</h1>
      </header>

      {stats && (
        <div className="mb-8 grid grid-cols-3 gap-4">
          <div className="rounded-lg border bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-bold text-blue-600">{stats.total_cases}</div>
            <div className="text-sm text-gray-500">Total Sessions</div>
          </div>
          <div className="rounded-lg border bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-bold text-green-600">{stats.cases_with_outcomes}</div>
            <div className="text-sm text-gray-500">With Outcomes</div>
          </div>
          <div className="rounded-lg border bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-bold text-purple-600">{stats.avg_confidence}%</div>
            <div className="text-sm text-gray-500">Avg Confidence</div>
          </div>
        </div>
      )}

      {loading && <p className="text-gray-500">Loading...</p>}

      {!loading && sessions.length === 0 && (
        <p className="rounded-lg border bg-white p-6 text-center text-gray-500 shadow-sm">
          No sessions yet. Submit a question on the home page.
        </p>
      )}

      {sessions.length > 0 && (
        <div className="space-y-3">
          {sessions.map((s) => (
            <a
              key={s.session_id}
              href={`/session/${s.session_id}`}
              className="block rounded-lg border bg-white p-4 shadow-sm transition hover:shadow-md"
            >
              <div className="flex items-center justify-between">
                <p className="font-medium text-gray-900">{s.question}</p>
                <span className="rounded bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800">
                  {s.status}
                </span>
              </div>
              <p className="mt-1 text-xs text-gray-400">{s.session_id}</p>
            </a>
          ))}
        </div>
      )}
    </main>
  );
}
