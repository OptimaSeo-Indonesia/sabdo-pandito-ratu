import { motion } from "framer-motion";
import { cn } from "../../lib/utils";
import {
  Brain,
  Scale,
  Shield,
  Eye,
  Lightbulb,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Target,
  GitBranch,
  FileText,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import type { FullReport, Verdict } from "../../types/api";

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
            stroke="hsl(var(--border))"
            strokeWidth="6"
            className="opacity-50"
          />
          <motion.circle
            cx="50" cy="50" r="42"
            fill="none"
            stroke={`hsl(${color})`}
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
      className="glass-card flex items-center gap-3 p-4"
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
  alternatives,
}: {
  factors: string[];
  alternatives: string[];
}) {
  const [expanded, setExpanded] = useState(true);

  const branches = [
    { label: "Question", icon: Target, children: [] as string[] },
    { label: "Evidence", icon: Scale, children: factors.slice(0, 3) },
    { label: "Assumptions", icon: Eye, children: factors.slice(3, 6) },
    { label: "Conflicts", icon: Shield, children: [] },
    { label: "Reflection", icon: Brain, children: [] },
    { label: "Consensus", icon: TrendingUp, children: [] },
    { label: "Decision", icon: CheckCircle2, children: [] },
  ];

  return (
    <div className="glass-card overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4 transition-colors hover:bg-accent/50"
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
        <div className="border-t border-border/50 px-4 pb-4 pt-2">
          <div className="relative pl-6">
            <div className="absolute bottom-0 left-[7px] top-0 w-px bg-border" />
            {branches.map((branch, i) => (
              <div key={branch.label} className="relative py-1.5">
                <div className="absolute -left-[22px] top-[10px] flex h-3 w-3 items-center justify-center rounded-full border border-border bg-card">
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
                      <p
                        key={child}
                        className="text-[11px] text-muted-foreground/70"
                      >
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

import { useState, useMemo } from "react";

export function VerdictDashboard({ verdict, report }: VerdictDashboardProps) {
  const ws = report.verdict.wisdom_score;
  const overallScore = ws?.overall ?? verdict.wisdom_score ?? 0;
  const confidencePct = Math.round(verdict.confidence * 100);

  const metrics = useMemo(() => {
    const items = [
      { icon: Brain, label: "Wisdom Score", value: `${overallScore}/100`, color: "bg-gradient-to-br from-primary to-primary-600" },
      { icon: TrendingUp, label: "Confidence", value: `${confidencePct}%`, color: "bg-gradient-to-br from-emerald-500 to-teal-600" },
    ];

    const consensusScore = report.conflicts.length > 0
      ? Math.max(0, 100 - report.conflicts.length * 15)
      : 85;
    items.push({
      icon: Target,
      label: "Consensus",
      value: `${consensusScore}%`,
      color: "bg-gradient-to-br from-violet-500 to-purple-600",
    });

    const conflictScore = Math.min(report.conflicts.length * 20, 100);
    items.push({
      icon: AlertTriangle,
      label: "Conflict Level",
      value: `${conflictScore}%`,
      color: "bg-gradient-to-br from-amber-500 to-orange-600",
    });

    items.push({
      icon: Scale,
      label: "Ethical Alignment",
      value: `${Math.round(
        report.principle_evaluations.reduce((s, p) => s + p.score, 0) /
          Math.max(report.principle_evaluations.length, 1) *
          10
      )}%`,
      color: "bg-gradient-to-br from-cyan-500 to-blue-600",
    });

    return items;
  }, [overallScore, confidencePct, report]);

  return (
    <div className="space-y-6">
      <div>
        <div className="mb-1 flex items-center gap-2">
          <FileText className="h-4 w-4 text-primary" />
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
            Executive Intelligence Summary
          </span>
        </div>
        <h2 className="text-2xl font-bold sm:text-3xl">{verdict.decision}</h2>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="glass-card col-span-1 flex items-center justify-center p-6 sm:col-span-2 lg:col-span-1">
          <div className="flex gap-6">
            <Gauge value={overallScore} label="Wisdom" color="var(--primary)" />
            <Gauge value={confidencePct} label="Confidence" color="160 84% 39%" />
          </div>
        </div>

        {metrics.map((m, i) => (
          <InsightCard key={m.label} {...m} index={i} />
        ))}
      </div>

      {verdict.summary && (
        <div className="glass-card p-5">
          <p className="text-sm leading-relaxed text-muted-foreground">
            {verdict.summary}
          </p>
        </div>
      )}

      {ws && (
        <div className="glass-card p-5">
          <h3 className="mb-4 text-sm font-medium text-muted-foreground">
            Wisdom Score Dimensions
          </h3>
          <div className="grid gap-3 sm:grid-cols-2">
            {Object.entries(ws)
              .filter(([k]) => k !== "overall")
              .map(([key, val]) => (
                <div key={key}>
                  <div className="mb-1 flex items-center justify-between text-xs">
                    <span className="capitalize text-muted-foreground">
                      {key.replace(/_/g, " ")}
                    </span>
                    <span className="font-medium tabular-nums">{String(val)}/100</span>
                  </div>
                  <div className="h-1.5 overflow-hidden rounded-full bg-border">
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

      <ReasoningTree
        factors={report.reasoning.key_factors}
        alternatives={report.alternatives || []}
      />

      {report.recommendations.length > 0 && (
        <div className="glass-card p-5">
          <h3 className="mb-3 text-sm font-medium text-muted-foreground">
            Recommended Actions
          </h3>
          <ul className="space-y-2">
            {report.recommendations.map((r) => (
              <li
                key={r}
                className="flex items-start gap-2 text-sm text-foreground/80"
              >
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}

      {report.alternatives.length > 0 && (
        <div className="glass-card p-5">
          <h3 className="mb-3 text-sm font-medium text-muted-foreground">
            Alternative Decisions
          </h3>
          <ul className="space-y-2">
            {report.alternatives.map((a) => (
              <li
                key={a}
                className="flex items-start gap-2 text-sm text-foreground/80"
              >
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-muted-foreground/40" />
                {a}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
