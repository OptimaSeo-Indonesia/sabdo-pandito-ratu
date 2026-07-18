import type {
  StartResponse,
  DryRunResponse,
  DeliberationStatus,
  FullReport,
  AdvisorProfile,
  SessionListItem,
  SessionStats,
} from "@/types/api";

const BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${res.status}: ${body}`);
  }
  return res.json();
}

export function startDeliberation(
  question: string,
  context?: Record<string, unknown>
): Promise<StartResponse> {
  return request("/api/v1/deliberate", {
    method: "POST",
    body: JSON.stringify({ question, context: context || {} }),
  });
}

export function startDryRun(
  question: string,
  context?: Record<string, unknown>
): Promise<DryRunResponse> {
  return request("/api/v1/deliberate/dry-run", {
    method: "POST",
    body: JSON.stringify({ question, context: context || {} }),
  });
}

export function getDeliberationStatus(
  sessionId: string
): Promise<DeliberationStatus> {
  return request(`/api/v1/deliberate/${sessionId}`);
}

export function getDeliberationReport(
  sessionId: string
): Promise<FullReport> {
  return request(`/api/v1/deliberate/${sessionId}/report`);
}

export function listAdvisors(): Promise<AdvisorProfile[]> {
  return request("/api/v1/advisors");
}

export function listSessions(
  status?: string,
  limit = 20,
  offset = 0
): Promise<{ items: SessionListItem[]; total: number; limit: number; offset: number }> {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (status) params.set("status", status);
  return request(`/api/v1/sessions?${params}`);
}

export function getSessionStats(): Promise<SessionStats> {
  return request("/api/v1/sessions/stats");
}
