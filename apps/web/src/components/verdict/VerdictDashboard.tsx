import { motion } from "framer-motion";
import { cn } from "../../lib/utils";
import {
  Brain,
  Scale,
  Shield,
  Eye,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Target,
  GitBranch,
  FileText,
  ChevronDown,
  ChevronRight,
  Lightbulb,
  BarChart3,
} from "lucide-react";
import type { FullReport, Verdict } from "../../types/api";
import { useState } from "react";

interface VerdictDashboardProps {
  verdict: Verdict;
  report: FullReport;
}

function Gauge({ value, label, color, size = "md" }: { value: number; label: string; color: string; size?: "sm" | "md" | "lg" }) {
  const isSm = size === "sm";
  return (
    <div className="flex flex-col items-center">
      <div className={cn("relative", isSm ? "h-16 w-16" : "h-20 w-20 sm:h-24 sm:w-24")}>
        <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50" cy="50" r="42"
            fill="none"
            stroke="rgba(255,255,255,0.1)"
            strokeWidth="6"
          />
          <motion.circle
            cx="50" cy="50" r="42"
            fill="none"
            stroke={color}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={`${2 * Math.PI * 42}`}
            initial={{ strokeDashoffset: 2 * Math.PI * 42 }}
            animate={{
              strokeDashoffset: 2 * Math.PI * 42 * (1 - value / 100),
            }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={cn("font-bold tabular-nums", isSm ? "text-sm" : "text-lg sm:text-xl")}>
            {Math.round(value)}
            {isSm ? "" : "%"}
          </span>
        </div>
      </div>
      <p className={cn("mt-1 text-center font-medium text-muted-foreground", isSm ? "text-[10px]" : "text-xs")}>
        {label}
      </p>
    </div>
  );
}

function InsightCard({
  icon: Icon,
  label,
  value,
  color,
  index,
}: {
  icon: typeof Brain;
  label: string;
  value: string | number;
  color: string;
  index: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 + index * 0.05 }}
      className="bg-card card-ref flex items-center gap-3 p-4"
    >
      <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${color}`}>
        <Icon className="h-5 w-5 text-white" />
      </div>
      <div className="min-w-0">
        <p className="text-lg font-bold tabular-nums leading-tight">{value}</p>
        <p className="text-xs text-muted-foreground truncate">{label}</p>
      </div>
    </motion.div>
  );
}

function ReasoningTree({
  factors,
}: {
  factors: string[];
}) {
  const [expanded, setExpanded] = useState(true);

  const branches = [
    { label: "Evidence", icon: Scale, children: factors.slice(0, 3) },
    { label: "Assumptions", icon: Eye, children: factors.slice(3, 6) },
    { label: "Conflicts", icon: Shield, children: [] },
    { label: "Reflection", icon: Brain, children: [] },
    { label: "Consensus", icon: TrendingUp, children: [] },
    { label: "Decision", icon: CheckCircle2, children: [] },
  ];

  return (
    <div className="bg-card card-ref overflow-hidden rounded-2xl">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4 transition-colors hover:bg-white/5"
      >
        <div className="flex items-center gap-2">
          <GitBranch className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm font-medium">Reasoning Tree</span>
        </div>
        {expanded ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground" />
        )}
      </button>
      {expanded && (
        <div className="border-t border-white/10 px-4 pb-4 pt-2">
          <div className="relative pl-6">
            <div className="absolute bottom-0 left-[7px] top-0 w-px bg-white/10" />
            {branches.map((branch) => (
              <div key={branch.label} className="relative py-1.5">
                <div className="absolute -left-[22px] top-[10px] flex h-3 w-3 items-center justify-center rounded-full border border-white/10 bg-white/5">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary/60" />
                </div>
                <div className="flex items-center gap-2">
                  <branch.icon className="h-3.5 w-3.5 text-muted-foreground" />
                  <span className="text-xs font-medium text-foreground/80">
                    {branch.label}
                  </span>
                </div>
                {branch.children.length > 0 && (
                  <div className="mt-1 ml-5 space-y-0.5">
                    {branch.children.map((child) => (
                      <p key={child} className="text-[11px] text-muted-foreground/70">
                        {child}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function CollapsibleSection({ title, icon: Icon, children, defaultOpen = false }: { title: string; icon: typeof Brain; children: React.ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="bg-card card-ref overflow-hidden rounded-2xl">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between p-4 transition-colors hover:bg-white/5"
      >
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm font-medium">{title}</span>
        </div>
        {open ? <ChevronDown className="h-4 w-4 text-muted-foreground" /> : <ChevronRight className="h-4 w-4 text-muted-foreground" />}
      </button>
      {open && <div className="border-t border-white/10 px-4 pb-4 pt-3">{children}</div>}
    </div>
  );
}

export function VerdictDashboard({ verdict, report }: VerdictDashboardProps) {
  const ws = report.verdict.wisdom_score;
  const overallScore = ws?.overall ?? verdict.wisdom_score ?? 0;
  const confidencePct = Math.round(verdict.confidence * 100);

  const consensusScore = report.conflicts.length > 0
    ? Math.max(0, 100 - report.conflicts.length * 15)
    : 85;
  const conflictScore = Math.min(report.conflicts.length * 20, 100);
  const ethicalAlignment = Math.round(
    report.principle_evaluations.reduce((s, p) => s + p.score, 0) /
      Math.max(report.principle_evaluations.length, 1) * 10
  );

  return (
    <div className="mx-auto w-full max-w-[1280px]">
      <div className="mb-1 flex items-center gap-2">
        <FileText className="h-4 w-4 text-primary" />
        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
          Executive Intelligence Summary
        </span>
      </div>
      <h2 className="mb-6 text-2xl font-bold sm:text-3xl">{verdict.decision}</h2>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          {/* Executive Summary */}
          {verdict.summary && (
            <div className="bg-card card-ref rounded-2xl p-5">
              <p className="text-sm leading-relaxed text-muted-foreground">
                {verdict.summary}
              </p>
            </div>
          )}

          {/* Reasoning */}
          <ReasoningTree factors={report.reasoning.key_factors} />

          {/* Transcript - collapsible sections */}
          <div className="space-y-3">
            {report.scenario_explorations.length > 0 && (
              <CollapsibleSection title="Scenario Explorations" icon={Lightbulb} defaultOpen={false}>
                <div className="space-y-3">
                  {report.scenario_explorations.map((s) => (
                    <div key={s.name} className="border-b border-white/5 pb-2 last:border-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-foreground/80">{s.name}</span>
                        <span className="text-xs tabular-nums text-muted-foreground">{s.horizon} · {Math.round(s.probability * 100)}%</span>
                      </div>
                      {s.assumptions.length > 0 && (
                        <div className="mt-1 flex flex-wrap gap-1">
                          {s.assumptions.map((a) => (
                            <span key={a.description} className="rounded-md bg-white/5 px-1.5 py-0.5 text-[10px] text-muted-foreground">
                              {a.description}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CollapsibleSection>
            )}

            {report.conflicts.length > 0 && (
              <CollapsibleSection title="Conflicts" icon={Shield} defaultOpen={false}>
                <div className="space-y-2">
                  {report.conflicts.map((c) => (
                    <div key={c.description} className="rounded-lg bg-white/5 p-3">
                      <div className="flex items-center gap-2 text-xs">
                        <AlertTriangle className="h-3 w-3 text-amber-400 shrink-0" />
                        <span className="font-medium text-amber-400/80 capitalize">{c.type.replace(/_/g, " ")}</span>
                      </div>
                      <p className="mt-1 text-xs text-muted-foreground">{c.description}</p>
                      <p className="mt-0.5 text-[10px] text-muted-foreground/60">Between: {c.between.join(", ")}</p>
                    </div>
                  ))}
                </div>
              </CollapsibleSection>
            )}

            {report.principle_evaluations.length > 0 && (
              <CollapsibleSection title="Principle Evaluations" icon={Scale} defaultOpen={false}>
                <div className="space-y-2">
                  {report.principle_evaluations.map((p) => (
                    <div key={p.principle} className="flex items-center justify-between text-xs">
                      <span className="text-foreground/80 capitalize">{p.principle.replace(/_/g, " ")}</span>
                      <span className="tabular-nums font-medium">{p.score}/10</span>
                    </div>
                  ))}
                </div>
              </CollapsibleSection>
            )}

            {report.alternatives.length > 0 && (
              <CollapsibleSection title="Alternatives Considered" icon={GitBranch} defaultOpen={false}>
                <ul className="space-y-2">
                  {report.alternatives.map((a) => (
                    <li key={a} className="flex items-start gap-2 text-xs text-foreground/80">
                      <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-muted-foreground/40" />
                      {a}
                    </li>
                  ))}
                </ul>
              </CollapsibleSection>
            )}
          </div>
        </div>

        <div className="space-y-6">
          {/* Confidence & Wisdom gauges */}
          <div className="bg-card card-ref rounded-2xl p-5">
            <div className="flex justify-center gap-8">
              <Gauge value={overallScore} label="Wisdom" color="#4F8CFF" />
              <Gauge value={confidencePct} label="Confidence" color="#34D399" />
            </div>
          </div>

          {/* Wisdom dimensions */}
          {ws && (
            <div className="bg-card card-ref rounded-2xl p-5">
              <h3 className="mb-4 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Wisdom Dimensions
              </h3>
              <div className="space-y-3">
                {Object.entries(ws)
                  .filter(([k]) => k !== "overall")
                  .map(([key, val]) => (
                    <div key={key}>
                      <div className="mb-1 flex items-center justify-between text-xs">
                        <span className="capitalize text-muted-foreground">{key.replace(/_/g, " ")}</span>
                        <span className="font-medium tabular-nums">{String(val)}/100</span>
                      </div>
                      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${val}%` }}
                          transition={{ duration: 0.8, ease: "easeOut", delay: 0.5 }}
                          className="h-full rounded-full bg-gradient-to-r from-primary to-primary-400"
                        />
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Metrics */}
          <InsightCard icon={Target} label="Consensus" value={`${consensusScore}%`} color="bg-gradient-to-br from-violet-500 to-purple-600" index={0} />
          <InsightCard icon={AlertTriangle} label="Conflict Level" value={`${conflictScore}%`} color="bg-gradient-to-br from-amber-500 to-orange-600" index={1} />
          <InsightCard icon={Scale} label="Ethical Alignment" value={`${ethicalAlignment}%`} color="bg-gradient-to-br from-cyan-500 to-blue-600" index={2} />

          {/* Recommendations */}
          {report.recommendations.length > 0 && (
            <div className="bg-card card-ref rounded-2xl p-5">
              <h3 className="mb-3 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Recommendations
              </h3>
              <ul className="space-y-2">
                {report.recommendations.map((r) => (
                  <li key={r} className="flex items-start gap-2 text-xs text-foreground/80">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
