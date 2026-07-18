import { useEffect, useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { getDeliberationStatus, getDeliberationReport } from "../lib/api";
import type { DeliberationStatus, FullReport } from "../types/api";
import { cn } from "../lib/utils";
import { Badge } from "../components/ui/badge";
import { CouncilChamber } from "../components/council/CouncilChamber";
import { CouncilCore } from "../components/council/CouncilCore";
import { DeliberationTimeline } from "../components/deliberation/DeliberationTimeline";
import { VerdictDashboard } from "../components/verdict/VerdictDashboard";
import { ADVISORS, THINKING_PHRASES, IDLE_STATUSES } from "../components/council/CouncilChamber";
import { AlertCircle, Loader2, Clock } from "lucide-react";
import type { CouncilPhase, AdvisorState, NeuralConnection, ConnectionState } from "../components/council/types";

function randomItem<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

const CONFLICT_TYPES = ["conflict", "disagree", "disagree", "consensus"];

function simulateConnections(
  step: number,
  totalSteps: number,
  hasConflict: boolean
): NeuralConnection[] {
  const baseConnections: NeuralConnection[] = [
    { from: "sage", to: "guardian", state: "idle" },
    { from: "sage", to: "strategist", state: "idle" },
    { from: "guardian", to: "strategist", state: "idle" },
    { from: "guardian", to: "analyst", state: "idle" },
    { from: "strategist", to: "ethicist", state: "idle" },
    { from: "analyst", to: "ethicist", state: "idle" },
    { from: "analyst", to: "visionary", state: "idle" },
    { from: "ethicist", to: "visionary", state: "idle" },
    { from: "sage", to: "core", state: "idle" },
    { from: "guardian", to: "core", state: "idle" },
    { from: "strategist", to: "core", state: "idle" },
    { from: "analyst", to: "core", state: "idle" },
    { from: "ethicist", to: "core", state: "idle" },
    { from: "visionary", to: "core", state: "idle" },
    { from: "guardian", to: "ethicist", state: "idle" },
    { from: "strategist", to: "analyst", state: "idle" },
  ];

  if (step <= 1) return baseConnections;

  const ratio = step / totalSteps;

  return baseConnections.map((c) => {
    if (ratio < 0.3) {
      if (Math.random() > 0.6) return { ...c, state: "active" as ConnectionState };
    } else if (ratio < 0.5 && hasConflict) {
      if (c.from === "guardian" && c.to === "ethicist") return { ...c, state: "conflict" as ConnectionState };
      if (c.from === "strategist" && c.to === "analyst") return { ...c, state: "disagree" as ConnectionState };
      if (Math.random() > 0.7) return { ...c, state: "active" as ConnectionState };
    } else if (ratio < 0.8) {
      if (c.from === "guardian" && c.to === "ethicist") return { ...c, state: "disagree" as ConnectionState };
      if (c.from === "strategist" && c.to === "analyst") return { ...c, state: "disagree" as ConnectionState };
      if (Math.random() > 0.5) return { ...c, state: "active" as ConnectionState };
    } else {
      return { ...c, state: "consensus" as ConnectionState };
    }
    return c;
  });
}

function LoadingSkeleton() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="mx-auto max-w-lg px-4 py-20">
      <div className="glass-card p-8 text-center">
        <AlertCircle className="mx-auto mb-4 h-12 w-12 text-destructive" />
        <h2 className="mb-2 text-lg font-semibold">Deliberation Error</h2>
        <p className="text-sm text-muted-foreground">{message}</p>
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
    return () => {
      cancelled = true;
      clearTimeout(pollTimer);
    };
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

  const advisorStates: AdvisorState[] = useMemo(() => {
    const states: AdvisorState[] = ADVISORS.map((a) => ({
      id: a.id,
      status: "idle",
      statusLabel: randomItem(IDLE_STATUSES),
      progress: 0,
    }));

    if (isComplete && status && status.advisor_statuses.length > 0) {
      return ADVISORS.map((a) => {
        const apiState = status.advisor_statuses.find(
          (as) => as.persona.replace(/\s+/g, "_").toLowerCase() === a.id
        );
        return {
          id: a.id,
          status: "done",
          statusLabel: "Completed",
          progress: 100,
          stance: apiState?.stance,
          confidence: apiState?.confidence,
        };
      });
    }

    if (isRunning && status) {
      const activeStepIdx = status.progress.steps.findIndex(
        (s) => s.status === "in_progress"
      );
      const ratio = activeStepIdx >= 0 ? activeStepIdx / status.progress.steps_total : 0.3;

      return ADVISORS.map((a, i) => {
        const baseProgress = Math.min(100, Math.round(ratio * 100 + (i * 5)));
        const phrases = THINKING_PHRASES[a.id] || ["Analyzing..."];

        let advisorStatus: string;
        let advisorLabel: string;
        let advisorProgress: number;

        if (baseProgress >= 95) {
          advisorStatus = "done";
          advisorLabel = "Completed";
          advisorProgress = 100;
        } else if (baseProgress >= 70) {
          advisorStatus = "thinking";
          advisorLabel = phrases[3] || "Synthesizing...";
          advisorProgress = baseProgress;
        } else if (baseProgress >= 40) {
          advisorStatus = "thinking";
          advisorLabel = phrases[2] || "Evaluating...";
          advisorProgress = baseProgress;
        } else if (baseProgress >= 15) {
          advisorStatus = "thinking";
          advisorLabel = phrases[1] || "Analyzing...";
          advisorProgress = baseProgress;
        } else {
          advisorStatus = "thinking";
          advisorLabel = phrases[0] || "Thinking...";
          advisorProgress = baseProgress;
        }

        return {
          id: a.id,
          status: advisorStatus,
          statusLabel: advisorLabel,
          progress: advisorProgress,
        };
      });
    }

    return states;
  }, [status, isRunning, isComplete]);

  const connections = useMemo(() => {
    if (!status) return [];
    const activeStepIdx = status.progress.steps.findIndex(
      (s) => s.status === "in_progress"
    );
    const hasConflict = councilPhase === "conflict";
    return simulateConnections(
      Math.max(0, activeStepIdx),
      status.progress.steps_total,
      hasConflict
    );
  }, [status, councilPhase]);

  const consensusLevel = useMemo(() => {
    if (isComplete) return 100;
    if (!status) return 0;
    const completed = status.progress.steps_completed;
    const total = status.progress.steps_total;
    return Math.round((completed / total) * 100);
  }, [status, isComplete]);

  if (error) return <ErrorState message={error} />;
  if (!status && !error) return <LoadingSkeleton />;

  return (
    <div className="aurora-bg relative min-h-screen">
      <div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {status && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <div className="mb-6">
              <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
                <Clock className="h-3 w-3" />
                Session
              </div>
              <h1 className="text-xl font-bold leading-tight sm:text-2xl">{status.question}</h1>
              <p className="mt-1 text-[10px] text-muted-foreground font-mono">{id}</p>
            </div>

            <div className="grid gap-6 lg:grid-cols-5">
              <div className="space-y-6 lg:col-span-3">
                {isRunning && (
                  <DeliberationTimeline steps={status.progress.steps} />
                )}

                {isComplete && report && (
                  <VerdictDashboard
                    verdict={status.verdict!}
                    report={report}
                  />
                )}

                {status.status === "failed" && (
                  <ErrorState message={status.error || "Deliberation failed"} />
                )}
              </div>

              <div className="space-y-6 lg:col-span-2">
                <div className="glass-card overflow-hidden p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
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
                    advisorStates={advisorStates}
                    consensusLevel={consensusLevel}
                    verdict={status.verdict?.decision}
                  />
                </div>

                {isRunning && (
                  <div className="glass-card p-4">
                    <h3 className="mb-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Deliberation Status
                    </h3>
                    <div className="flex items-center gap-3">
                      <Loader2 className="h-5 w-5 animate-spin text-primary shrink-0" />
                      <div>
                        <p className="text-sm font-medium">Council deliberating...</p>
                        <p className="text-xs text-muted-foreground">
                          Step {status.progress.steps_completed + 1} of{" "}
                          {status.progress.steps_total}
                        </p>
                      </div>
                    </div>
                    <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-border">
                      <motion.div
                        className="h-full rounded-full bg-gradient-to-r from-primary to-primary-400"
                        initial={{ width: 0 }}
                        animate={{
                          width: `${(status.progress.steps_completed / status.progress.steps_total) * 100}%`,
                        }}
                        transition={{ duration: 0.5 }}
                      />
                    </div>
                  </div>
                )}

                {isComplete && status.advisor_statuses.length > 0 && (
                  <div className="glass-card p-4">
                    <h3 className="mb-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Council Summary
                    </h3>
                    <div className="space-y-2">
                      {status.advisor_statuses.map((a) => (
                        <div
                          key={a.persona}
                          className="flex items-center justify-between text-xs"
                        >
                          <span className="capitalize text-muted-foreground">
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
    </div>
  );
}
