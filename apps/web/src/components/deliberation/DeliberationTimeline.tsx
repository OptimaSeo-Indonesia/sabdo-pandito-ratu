import { motion } from "framer-motion";
import { cn } from "../../lib/utils";
import {
  Eye,
  Lightbulb,
  Scale,
  Shield,
  Sparkles,
  BarChart3,
  FileText,
  Brain,
  CheckCircle2,
  Loader2,
  type LucideIcon,
} from "lucide-react";

interface Step {
  name: string;
  label: string;
  status: "pending" | "in_progress" | "completed" | "failed";
  icon: LucideIcon;
}

const DELIBERATION_STEPS: Step[] = [
  { name: "analyze_context", label: "Context Analysis", status: "pending", icon: Eye },
  { name: "generate_perspectives", label: "Perspective Generation", status: "pending", icon: Lightbulb },
  { name: "collect_arguments", label: "Argument Collection", status: "pending", icon: Scale },
  { name: "resolve_conflicts", label: "Conflict Resolution", status: "pending", icon: Shield },
  { name: "evaluate_principles", label: "Ethical Review", status: "pending", icon: Sparkles },
  { name: "explore_scenarios", label: "Scenario Exploration", status: "pending", icon: Eye },
  { name: "reflect", label: "Reflection", status: "pending", icon: Brain },
  { name: "score_wisdom", label: "Wisdom Scoring", status: "pending", icon: BarChart3 },
  { name: "generate_verdict", label: "Verdict Generation", status: "pending", icon: FileText },
];

interface DeliberationTimelineProps {
  steps: Array<{ name: string; status: string }>;
  className?: string;
}

export function DeliberationTimeline({
  steps: externalSteps,
  className,
}: DeliberationTimelineProps) {
  const steps = DELIBERATION_STEPS.map((s) => {
    const ext = externalSteps.find((es) => es.name === s.name);
    if (!ext) return s;
    return {
      ...s,
      status: ext.status as Step["status"],
    };
  });

  const completed = steps.filter((s) => s.status === "completed").length;
  const total = steps.length;

  return (
    <div className={cn("space-y-1", className)}>
      <div className="mb-3 flex items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
          Deliberation Pipeline
        </span>
        <span className="text-xs tabular-nums text-muted-foreground">
          {completed}/{total}
        </span>
      </div>

      <div className="relative">
        <div className="absolute bottom-0 left-[15px] top-0 w-px bg-border" />
        <div
          className="absolute bottom-0 left-[15px] w-px bg-primary transition-all duration-700"
          style={{ height: `${(completed / total) * 100}%` }}
        />

        <div className="space-y-0">
          {steps.map((step, i) => {
            const isDone = step.status === "completed";
            const isActive = step.status === "in_progress";
            const isFailed = step.status === "failed";
            const Icon = step.icon;

            return (
              <motion.div
                key={step.name}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.04 }}
                className={cn(
                  "relative flex items-center gap-3 rounded-lg px-4 py-2.5 transition-all duration-300",
                  isActive && "bg-primary/[0.04]",
                  isDone && "opacity-80"
                )}
              >
                <div
                  className={cn(
                    "relative z-10 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-500",
                    isDone &&
                      "border-success bg-success text-white shadow-[0_0_12px] shadow-success/30",
                    isActive &&
                      "border-primary bg-primary/10 text-primary shadow-[0_0_12px] shadow-primary/20",
                    isFailed &&
                      "border-destructive bg-destructive/10 text-destructive",
                    !isDone &&
                      !isActive &&
                      !isFailed &&
                      "border-border bg-transparent text-muted-foreground"
                  )}
                >
                  {isDone ? (
                    <CheckCircle2 className="h-3.5 w-3.5" />
                  ) : isActive ? (
                    <Loader2 className="h-3 w-3 animate-spin" />
                  ) : (
                    <Icon className="h-3.5 w-3.5" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <p
                    className={cn(
                      "text-sm font-medium leading-tight transition-colors",
                      isDone && "text-foreground",
                      isActive && "text-primary",
                      isFailed && "text-destructive",
                      !isDone && !isActive && !isFailed && "text-muted-foreground"
                    )}
                  >
                    {step.label}
                  </p>
                </div>

                <div className="shrink-0">
                  {isActive && (
                    <span className="flex items-center gap-1.5 text-xs text-primary">
                      <span className="relative flex h-2 w-2">
                        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
                        <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
                      </span>
                      In progress
                    </span>
                  )}
                  {isDone && (
                    <CheckCircle2 className="h-4 w-4 text-success" />
                  )}
                  {isFailed && (
                    <span className="text-xs text-destructive">Failed</span>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
