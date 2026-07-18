import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { getDeliberationStatus, getDeliberationReport } from "../lib/api";
import type { DeliberationStatus, FullReport } from "../types/api";
import { cn } from "../lib/utils";
import { Badge } from "../components/ui/badge";
import {
  Brain,
  Eye,
  Scale,
  Shield,
  Lightbulb,
  Sparkles,
  CheckCircle2,
  Loader2,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Clock,
  Users,
  BarChart3,
  FileText,
} from "lucide-react";

const STEP_LABELS: Record<string, string> = {
  analyze_context: "Context Analysis",
  generate_perspectives: "Perspective Generation",
  collect_arguments: "Argument Collection",
  resolve_conflicts: "Conflict Resolution",
  evaluate_principles: "Ethical Review",
  explore_scenarios: "Scenario Exploration",
  reflect: "Reflection",
  score_wisdom: "Wisdom Scoring",
  generate_verdict: "Verdict Generation",
};

const STEP_ICONS: Record<string, typeof Brain> = {
  analyze_context: Eye,
  generate_perspectives: Lightbulb,
  collect_arguments: Scale,
  resolve_conflicts: Shield,
  evaluate_principles: Sparkles,
  explore_scenarios: Eye,
  reflect: Brain,
  score_wisdom: BarChart3,
  generate_verdict: FileText,
};

const ADVISOR_CONFIG: Record<string, { icon: typeof Brain; color: string }> = {
  rational_analyst: { icon: Scale, color: "from-emerald-500 to-teal-600" },
  humanitarian: { icon: Sparkles, color: "from-rose-500 to-pink-600" },
  economic_analyst: { icon: BarChart3, color: "from-blue-500 to-indigo-600" },
  legal_expert: { icon: Shield, color: "from-amber-500 to-orange-600" },
  devils_advocate: { icon: Eye, color: "from-violet-500 to-purple-600" },
  long_term_strategist: { icon: Brain, color: "from-cyan-500 to-blue-600" },
};

function getAdvisorConfig(persona: string) {
  const key = persona.toLowerCase().replace(/\s+/g, "_");
  return ADVISOR_CONFIG[key] || { icon: Brain, color: "from-primary to-primary-600" };
}

function ProgressTimeline({ steps }: { steps: Array<{ name: string; status: string }> }) {
  const currentIdx = steps.findIndex((s) => s.status === "in_progress");
  const completed = steps.filter((s) => s.status === "completed").length;
  const total = steps.length;

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-medium text-muted-foreground">Deliberation Progress</h3>
        <span className="text-xs tabular-nums text-muted-foreground">
          {completed}/{total} steps
        </span>
      </div>
      <div className="relative space-y-1">
        <div className="absolute bottom-0 left-[11px] top-0 w-0.5 bg-border" />
        <div
          className="absolute bottom-0 left-[11px] w-0.5 bg-primary transition-all duration-500"
          style={{ top: 0, height: `${(completed / total) * 100}%` }}
        />
        {steps.map((s, i) => {
          const Icon = STEP_ICONS[s.name] || Clock;
          const isDone = s.status === "completed";
          const isActive = s.status === "in_progress";
          const isPending = s.status === "pending";

          return (
            <motion.div
              key={s.name}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className={cn(
                "relative flex items-center gap-3 rounded-lg px-3 py-2.5 transition-all duration-300",
                isActive && "bg-primary/5",
                isDone && "opacity-90"
              )}
            >
              <div
                className={cn(
                  "relative z-10 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-300",
                  isDone && "border-success bg-success text-white",
                  isActive && "border-primary bg-primary/10 text-primary",
                  isPending && "border-border bg-transparent text-muted-foreground"
                )}
              >
                {isDone ? (
                  <CheckCircle2 className="h-3.5 w-3.5" />
                ) : isActive ? (
                  <Loader2 className="h-3 w-3 animate-spin" />
                ) : (
                  <div className="h-1.5 w-1.5 rounded-full bg-current" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p
                  className={cn(
                    "text-sm font-medium leading-tight",
                    isDone && "text-foreground",
                    isActive && "text-primary",
                    isPending && "text-muted-foreground"
                  )}
                >
                  {STEP_LABELS[s.name] || s.name}
                </p>
              </div>
              {isActive && (
                <span className="shrink-0 text-xs text-primary">In progress...</span>
              )}
              {isDone && (
                <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-success" />
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

function CouncilPanel({ advisors }: { advisors: DeliberationStatus["advisor_statuses"] }) {
  if (!advisors || advisors.length === 0) return null;

  return (
    <div>
      <h3 className="mb-4 text-sm font-medium text-muted-foreground">AI Council</h3>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {advisors.map((a, i) => {
          const cfg = getAdvisorConfig(a.persona);
          const Icon = cfg.icon;
          return (
            <motion.div
              key={a.persona}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card flex items-center gap-3 p-4"
            >
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${cfg.color} shadow-lg`}
              >
                <Icon className="h-4.5 w-4.5 text-white" style={{ width: 18, height: 18 }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium capitalize leading-tight">
                  {a.persona.replace(/_/g, " ")}
                </p>
                <p className="text-xs capitalize text-muted-foreground">{a.stance.replace(/_/g, " ")}</p>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-sm font-semibold tabular-nums">
                  {Math.round(a.confidence * 100)}%
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

function VerdictDisplay({ status }: { status: DeliberationStatus }) {
  if (!status.verdict) return null;
  const v = status.verdict;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card overflow-hidden p-1"
    >
      <div className="rounded-xl bg-gradient-to-br from-primary/[0.03] to-transparent p-6 sm:p-8">
        <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
          <div>
            <Badge variant="default" className="mb-2 px-3 py-1">
              Final Verdict
            </Badge>
            <h2 className="text-2xl font-bold sm:text-3xl">{v.decision}</h2>
          </div>
          <div className="flex items-center gap-4">
            {v.wisdom_score != null && (
              <div className="text-center">
                <p className="text-2xl font-bold text-primary tabular-nums">{v.wisdom_score}</p>
                <p className="text-xs text-muted-foreground">Wisdom Score</p>
              </div>
            )}
            <div className="text-center">
              <p className="text-2xl font-bold tabular-nums">
                {Math.round(v.confidence * 100)}%
              </p>
              <p className="text-xs text-muted-foreground">Confidence</p>
            </div>
          </div>
        </div>
        {v.summary && (
          <p className="text-muted-foreground leading-relaxed">{v.summary}</p>
        )}
      </div>
    </motion.div>
  );
}

function WisdomScoreSection({ report }: { report: FullReport }) {
  if (!report.verdict.wisdom_score) return null;
  const ws = report.verdict.wisdom_score;

  const dimensions = Object.entries(ws)
    .filter(([k]) => k !== "overall")
    .map(([k, v]) => ({
      label: k.replace(/_/g, " "),
      score: v as number,
    }));

  return (
    <div className="glass-card p-6">
      <h3 className="mb-4 text-sm font-medium text-muted-foreground">Wisdom Score Breakdown</h3>
      <div className="space-y-3">
        {dimensions.map((d) => (
          <div key={d.label}>
            <div className="mb-1 flex items-center justify-between text-sm">
              <span className="capitalize text-muted-foreground">{d.label}</span>
              <span className="font-medium tabular-nums">{d.score}/100</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-border">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${d.score}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="h-full rounded-full bg-gradient-to-r from-primary to-primary-400"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ReportAccordion({ report }: { report: FullReport }) {
  const [open, setOpen] = useState(false);

  const sections = [
    {
      key: "principle_evaluations",
      label: "Principle Evaluations",
      count: report.principle_evaluations.length,
      content: report.principle_evaluations.length > 0 && (
        <div className="space-y-3">
          {report.principle_evaluations.map((p) => (
            <div key={p.principle} className="rounded-xl border border-border/50 p-4">
              <div className="mb-1 flex items-center justify-between">
                <span className="font-medium capitalize">{p.principle.replace(/_/g, " ")}</span>
                <span className="text-sm text-muted-foreground tabular-nums">{p.score}/10</span>
              </div>
              <p className="text-sm text-muted-foreground">{p.rationale}</p>
              {p.concerns.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {p.concerns.map((c) => (
                    <li key={c} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-muted-foreground/40" />
                      {c}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      ),
    },
    {
      key: "conflicts",
      label: "Conflicts Detected",
      count: report.conflicts.length,
      content: report.conflicts.length > 0 && (
        <div className="space-y-3">
          {report.conflicts.map((c) => (
            <div key={c.description} className="rounded-xl border border-border/50 p-4">
              <div className="mb-1 flex items-center gap-2">
                <span className="font-medium capitalize">{c.type.replace(/_/g, " ")}</span>
                <span className="text-xs text-muted-foreground">
                  between {c.between.join(", ")}
                </span>
              </div>
              <p className="text-sm text-muted-foreground">{c.description}</p>
            </div>
          ))}
        </div>
      ),
    },
    {
      key: "scenarios",
      label: "Scenario Explorations",
      count: report.scenario_explorations.length,
      content: report.scenario_explorations.length > 0 && (
        <div className="space-y-3">
          {report.scenario_explorations.map((s) => (
            <div key={s.name} className="rounded-xl border border-border/50 p-4">
              <div className="mb-1 flex items-center gap-2">
                <span className="font-medium">{s.name}</span>
                <span className="text-xs text-muted-foreground">({s.horizon})</span>
              </div>
              {s.assumptions.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {s.assumptions.map((a) => (
                    <li key={a.description} className="text-sm text-muted-foreground">
                      {a.description}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      ),
    },
    {
      key: "recommendations",
      label: "Recommendations",
      count: report.recommendations.length,
      content: report.recommendations.length > 0 && (
        <ul className="space-y-2">
          {report.recommendations.map((r) => (
            <li key={r} className="flex items-start gap-2 text-sm text-muted-foreground">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
              {r}
            </li>
          ))}
        </ul>
      ),
    },
    {
      key: "key_factors",
      label: "Key Factors",
      count: report.reasoning.key_factors.length,
      content: report.reasoning.key_factors.length > 0 && (
        <ul className="space-y-2">
          {report.reasoning.key_factors.map((f) => (
            <li key={f} className="flex items-start gap-2 text-sm text-muted-foreground">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
              {f}
            </li>
          ))}
        </ul>
      ),
    },
  ];

  return (
    <div className="glass-card overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between p-6 text-left transition-colors hover:bg-accent/50"
      >
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">Full Deliberation Report</span>
          <Badge variant="secondary" className="ml-2 text-xs">
            {sections.reduce((sum, s) => sum + s.count, 0)} items
          </Badge>
        </div>
        {open ? <ChevronUp className="h-4 w-4 text-muted-foreground" /> : <ChevronDown className="h-4 w-4 text-muted-foreground" />}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="border-t border-border/50 px-6 pb-6 pt-4">
              <div className="space-y-6">
                {sections.map(
                  (section) =>
                    section.count > 0 &&
                    section.content && (
                      <div key={section.key}>
                        <h4 className="mb-3 text-sm font-medium text-muted-foreground">
                          {section.label}
                        </h4>
                        {section.content}
                      </div>
                    )
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="space-y-6">
      <div className="glass-card p-6">
        <div className="h-4 w-48 animate-pulse rounded bg-border" />
        <div className="mt-3 h-3 w-full animate-pulse rounded bg-border" />
        <div className="mt-2 h-3 w-3/4 animate-pulse rounded bg-border" />
      </div>
      <div className="glass-card p-6">
        <div className="h-4 w-32 animate-pulse rounded bg-border" />
        <div className="mt-4 space-y-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="flex items-center gap-3">
              <div className="h-6 w-6 animate-pulse rounded-full bg-border" />
              <div className="h-3 flex-1 animate-pulse rounded bg-border" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="glass-card mx-auto max-w-lg p-8 text-center">
      <AlertCircle className="mx-auto mb-4 h-12 w-12 text-destructive" />
      <h2 className="mb-2 text-lg font-semibold">Deliberation Error</h2>
      <p className="text-sm text-muted-foreground">{message}</p>
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

  if (error) return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <ErrorState message={error} />
    </div>
  );

  return (
    <div className="aurora-bg relative min-h-screen">
      <div className="relative mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        {!status && <LoadingSkeleton />}

        {status && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
            <div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
                <Clock className="h-3 w-3" />
                Session
              </div>
              <h1 className="text-2xl font-bold leading-tight sm:text-3xl">{status.question}</h1>
              <p className="mt-1 text-xs text-muted-foreground font-mono">{id}</p>
            </div>

            <div className="grid gap-6 lg:grid-cols-5">
              <div className="space-y-6 lg:col-span-3">
                {isRunning && (
                  <div className="glass-card p-6">
                    <ProgressTimeline steps={status.progress.steps} />
                  </div>
                )}

                {isComplete && status.verdict && <VerdictDisplay status={status} />}

                {isComplete && report && report.verdict.wisdom_score && (
                  <WisdomScoreSection report={report} />
                )}

                {isComplete && report && <ReportAccordion report={report} />}

                {status.status === "failed" && (
                  <ErrorState message={status.error || "Deliberation failed"} />
                )}
              </div>

              <div className="space-y-6 lg:col-span-2">
                {status.advisor_statuses.length > 0 && (
                  <div className="glass-card p-6">
                    <CouncilPanel advisors={status.advisor_statuses} />
                  </div>
                )}

                {isRunning && (
                  <div className="glass-card p-6">
                    <h3 className="mb-4 text-sm font-medium text-muted-foreground">Deliberation Status</h3>
                    <div className="flex items-center gap-3">
                      <Loader2 className="h-5 w-5 animate-spin text-primary" />
                      <div>
                        <p className="text-sm font-medium">Council is deliberating...</p>
                        <p className="text-xs text-muted-foreground">
                          Step {status.progress.steps_completed + 1} of {status.progress.steps_total}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {isComplete && (
                  <div className="glass-card p-6">
                    <h3 className="mb-3 text-sm font-medium text-muted-foreground">Summary</h3>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Advisors</span>
                        <span className="font-medium tabular-nums">{status.advisor_statuses.length}</span>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Steps Completed</span>
                        <span className="font-medium tabular-nums">{status.progress.steps_completed}/{status.progress.steps_total}</span>
                      </div>
                      {status.verdict && (
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">Confidence</span>
                          <span className="font-medium tabular-nums">{Math.round(status.verdict.confidence * 100)}%</span>
                        </div>
                      )}
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
