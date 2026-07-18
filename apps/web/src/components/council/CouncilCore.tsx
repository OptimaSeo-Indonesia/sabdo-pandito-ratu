import { cn } from "../../lib/utils";
import { Sparkles, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import type { CouncilPhase } from "./types";

interface CouncilCoreProps {
  phase: CouncilPhase;
  consensusLevel?: number;
  verdict?: string;
  className?: string;
  style?: React.CSSProperties;
}

const PHASE_CONFIG: Record<
  CouncilPhase,
  { icon: typeof Sparkles; label: string; color: string; pulse: boolean }
> = {
  idle: {
    icon: Sparkles,
    label: "Council Ready",
    color: "from-primary/40 to-primary-600/20",
    pulse: false,
  },
  deliberating: {
    icon: Loader2,
    label: "Deliberating",
    color: "from-primary to-primary-600",
    pulse: true,
  },
  conflict: {
    icon: AlertCircle,
    label: "Conflict Detected",
    color: "from-destructive to-orange-600",
    pulse: true,
  },
  reflecting: {
    icon: Loader2,
    label: "Reflecting",
    color: "from-violet-500 to-purple-600",
    pulse: true,
  },
  consensus: {
    icon: CheckCircle2,
    label: "Building Consensus",
    color: "from-emerald-500 to-teal-600",
    pulse: true,
  },
  verdict: {
    icon: CheckCircle2,
    label: "Verdict Reached",
    color: "from-emerald-500 to-teal-600",
    pulse: false,
  },
};

export function CouncilCore({
  phase,
  consensusLevel = 0,
  verdict,
  className,
  style,
}: CouncilCoreProps) {
  const config = PHASE_CONFIG[phase];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "absolute flex flex-col items-center justify-center",
        className
      )}
      style={style}
    >
      <div
        className={cn(
          "relative flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br shadow-xl transition-all duration-700 sm:h-20 sm:w-20",
          config.color,
          phase !== "idle" && "shadow-[0_0_40px] shadow-primary/20"
        )}
      >
        {config.pulse && phase !== "deliberating" ? (
          <span className="absolute -inset-1 animate-ping rounded-full bg-white/10" />
        ) : null}
        {phase === "deliberating" ? (
          <Loader2 className="h-7 w-7 animate-spin text-white sm:h-8 sm:w-8" />
        ) : (
          <Icon className="h-7 w-7 text-white sm:h-8 sm:w-8" />
        )}
      </div>

      <p className="mt-2 text-xs font-medium text-foreground/80 sm:text-sm">
        {config.label}
      </p>

      {phase !== "idle" && phase !== "verdict" && (
        <div className="mt-1.5 flex items-center gap-2">
          <div className="h-1 w-16 overflow-hidden rounded-full bg-border sm:w-20">
            <div
              className="h-full rounded-full bg-primary transition-all duration-700"
              style={{ width: `${consensusLevel}%` }}
            />
          </div>
          <span className="text-[10px] tabular-nums text-muted-foreground">
            {consensusLevel}%
          </span>
        </div>
      )}

      {verdict && phase === "verdict" && (
        <p className="mt-1 text-[10px] font-semibold text-primary sm:text-xs">
          {verdict}
        </p>
      )}
    </div>
  );
}
