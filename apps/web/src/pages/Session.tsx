import { useEffect, useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { getDeliberationStatus, getDeliberationReport } from "../lib/api";
import type { DeliberationStatus, FullReport } from "../types/api";
import { Badge } from "../components/ui/badge";
import { CouncilChamber } from "../components/council/CouncilChamber";
import { DeliberationTimeline } from "../components/deliberation/DeliberationTimeline";
import { VerdictDashboard } from "../components/verdict/VerdictDashboard";
import { AlertCircle, Loader2, Clock } from "lucide-react";
import type { CouncilPhase } from "../components/council/types";
import { cn } from "../lib/utils";

const STEP_LABELS: Record<string, string> = {
  analyze_context: "Context Analysis",
  generate_perspectives: "Perspective Generation",
  collect_arguments: "Argument Collection",
  resolve_conflicts: "Conflict Detection",
  evaluate_principles: "Ethical Review",
  explore_scenarios: "Scenario Exploration",
  reflect: "Reflection",
  score_wisdom: "Consensus Building",
  generate_verdict: "Final Verdict",
};

function clamp(v: number, min = 0, max = 100) { return Math.max(min, Math.min(max, v)); }

function LoadingSkeleton() {
  return (
    <div className="flex items-center justify-center py-32">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="mx-auto max-w-lg py-20">
      <div className="bg-card card-ref rounded-2xl p-8 text-center">
        <AlertCircle className="mx-auto mb-4 h-12 w-12 text-danger" />
        <h2 className="mb-2 text-lg font-semibold">Deliberation Error</h2>
        <p className="text-sm text-muted">{message}</p>
      </div>
    </div>
  );
}

export default function Session() {
  const { id } = useParams<{ id: string }>();
  const [status, setStatus] = useState<DeliberationStatus | null>(null);
  const [report, setReport] = useState<FullReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isRunning = status && status.status !== "completed" && status.status !== "failed";
  const isComplete = status?.status === "completed";

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    let pollTimer: ReturnType<typeof setTimeout>;

    async function poll() {
      try {
        const s = await getDeliberationStatus(id!);
        if (cancelled) return;
        setStatus(s);
        if (s.status === "completed" || s.status === "failed") {
          if (s.status === "completed") {
            const r = await getDeliberationReport(id!);
            if (!cancelled) setReport(r);
          }
          return;
        }
        pollTimer = setTimeout(poll, 2000);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Unknown error");
      }
    }

    poll();
    return () => { cancelled = true; clearTimeout(pollTimer); };
  }, [id]);

  const councilPhase: CouncilPhase = useMemo(() => {
    if (isComplete) return "verdict";
    if (!status) return "idle";
    if (status.status === "failed") return "idle";
    const activeStep = status.progress.steps.find((s) => s.status === "in_progress");
    if (!activeStep) return "deliberating";
    if (["resolve_conflicts"].includes(activeStep.name)) return "conflict";
    if (["reflect"].includes(activeStep.name)) return "reflecting";
    if (["score_wisdom", "generate_verdict"].includes(activeStep.name)) return "consensus";
    return "deliberating";
  }, [status, isComplete]);

  const consensusLevel = useMemo(() => {
    if (isComplete) return 100;
    if (!status) return 0;
    return clamp(Math.round((status.progress.steps_completed / status.progress.steps_total) * 100));
  }, [status, isComplete]);

  const timelineSteps = useMemo(() => {
    if (!status) return [];
    return status.progress.steps.map((s) => ({
      name: s.name,
      label: STEP_LABELS[s.name] || s.name.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
      status: s.status as "pending" | "in_progress" | "completed" | "failed",
    }));
  }, [status]);

  if (error) return <ErrorState message={error} />;
  if (!status && !error) return <LoadingSkeleton />;

  const cardStyle = "bg-card card-ref";

  return (
    <div className="flex flex-col gap-6 overflow-auto">
      {status && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="mb-6">
            <div className="flex items-center gap-2 text-xs text-muted mb-1">
              <Clock className="h-3 w-3" />
              Session
            </div>
            <h1 className="text-xl font-bold leading-tight">{status.question}</h1>
            <p className="mt-1 text-[10px] text-muted font-mono">{id}</p>
          </div>

          <div className="grid gap-6" style={{ gridTemplateColumns: "1fr 380px" }}>
            <div className="space-y-6">
              {isRunning && (
                <div className={`${cardStyle} rounded-2xl p-4`}>
                  <DeliberationTimeline steps={timelineSteps} />
                </div>
              )}

              {isComplete && report && status.verdict && (
                <VerdictDashboard verdict={status.verdict} report={report} />
              )}

              {status.status === "failed" && (
                <ErrorState message={status.error || "Deliberation failed"} />
              )}
            </div>

            <div className="space-y-6">
              <div className={`${cardStyle} rounded-2xl p-4`}>
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-xs font-medium text-muted uppercase tracking-wider">
                    Council
                  </span>
                  {isRunning && (
                    <Badge variant="default" className="text-[10px] px-2 py-0">
                      <span className="relative mr-1 flex h-1.5 w-1.5">
                        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
                        <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-primary" />
                      </span>
                      Live
                    </Badge>
                  )}
                  {isComplete && (
                    <Badge variant="success" className="text-[10px] px-2 py-0">
                      Verdict
                    </Badge>
                  )}
                </div>
                <CouncilChamber
                  compact
                  phase={councilPhase}
                  consensusLevel={consensusLevel}
                  stepsComplete={status.progress.steps_completed}
                  stepsTotal={status.progress.steps_total}
                  confidence={status.verdict?.confidence}
                  wisdomScore={status.verdict?.wisdom_score ?? undefined}
                  advisorStatuses={status.advisor_statuses}
                />
              </div>

              {isRunning && (
                <div className={`${cardStyle} rounded-2xl p-4`}>
                  <h3 className="mb-3 text-xs font-medium text-muted uppercase tracking-wider">
                    Deliberation Status
                  </h3>
                  <div className="flex items-center gap-3">
                    <Loader2 className="h-5 w-5 animate-spin text-primary shrink-0" />
                    <div>
                      <p className="text-sm font-medium">Council deliberating...</p>
                      <p className="text-xs text-muted">
                        Step {status.progress.steps_completed + 1} of {status.progress.steps_total}
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-progress-track">
                    <motion.div
                      className="h-full rounded-full bg-grad-primary-btn"
                      initial={{ width: 0 }}
                      animate={{ width: `${consensusLevel}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>
              )}

              {isComplete && status.advisor_statuses.length > 0 && (
                <div className={`${cardStyle} rounded-2xl p-4`}>
                  <h3 className="mb-3 text-xs font-medium text-muted uppercase tracking-wider">
                    Council Summary
                  </h3>
                  <div className="space-y-2">
                    {status.advisor_statuses.map((a) => (
                      <div key={a.persona} className="flex items-center justify-between text-xs">
                        <span className="capitalize text-muted">
                          {a.persona.replace(/_/g, " ")}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className="capitalize">{a.stance.replace(/_/g, " ")}</span>
                          <span className="tabular-nums font-medium">
                            {Math.round(a.confidence * 100)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
