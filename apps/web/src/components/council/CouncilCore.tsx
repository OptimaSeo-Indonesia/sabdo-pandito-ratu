import { cn } from "../../lib/utils";

interface CouncilCoreProps {
  phase: "idle" | "deliberating" | "conflict" | "reflecting" | "consensus" | "verdict";
  stepsComplete?: number;
  stepsTotal?: number;
  consensusLevel?: number;
  conflictsActive?: number;
  confidence?: number;
  wisdomScore?: number;
  advisorCount?: number;
  className?: string;
  style?: React.CSSProperties;
}

interface PhaseConfig {
  title: string;
  subtitle: string;
  accent: string;
  glow: string;
}

const PHASES: Record<string, PhaseConfig> = {
  idle: {
    title: "Council Ready",
    subtitle: "Awaiting question",
    accent: "from-primary/30 to-primary-600/10",
    glow: "shadow-primary/10",
  },
  deliberating: {
    title: "Deliberating",
    subtitle: "Advisors analyzing",
    accent: "from-primary to-primary-600",
    glow: "shadow-primary/30",
  },
  conflict: {
    title: "Conflict Detected",
    subtitle: "Resolving disagreements",
    accent: "from-rose-500 to-orange-600",
    glow: "shadow-rose-500/30",
  },
  reflecting: {
    title: "Reflecting",
    subtitle: "Synthesizing insights",
    accent: "from-violet-500 to-purple-600",
    glow: "shadow-violet-500/30",
  },
  consensus: {
    title: "Building Consensus",
    subtitle: "Reaching alignment",
    accent: "from-emerald-500 to-teal-600",
    glow: "shadow-emerald-500/30",
  },
  verdict: {
    title: "Verdict Ready",
    subtitle: "Deliberation complete",
    accent: "from-emerald-400 to-teal-500",
    glow: "shadow-emerald-400/30",
  },
};

export function CouncilCore({
  phase,
  stepsComplete = 0,
  stepsTotal = 9,
  consensusLevel = 0,
  conflictsActive = 0,
  confidence,
  wisdomScore,
  advisorCount = 6,
  className,
  style,
}: CouncilCoreProps) {
  const cfg = PHASES[phase] || PHASES.idle;
  const isIdle = phase === "idle";
  const isActive = !isIdle && phase !== "verdict";
  const isComplete = phase === "verdict";

  return (
    <div
      className={cn(
        "absolute flex flex-col items-center justify-center text-center",
        className
      )}
      style={style}
    >
      <div
        className={cn(
          "relative flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br shadow-xl transition-all duration-1000 sm:h-16 sm:w-16",
          cfg.accent,
          cfg.glow,
          isActive && "shadow-[0_0_40px_var(--tw-shadow-color)]",
          isComplete && "shadow-[0_0_50px_var(--tw-shadow-color)]"
        )}
      >
        {isActive && (
          <span className="absolute inset-0 animate-ping rounded-full bg-white/15" />
        )}
        {isComplete && (
          <>
            <span className="absolute inset-0 animate-ping rounded-full bg-white/10" />
            <span
              className="absolute inset-2 rounded-full bg-white/20 blur-sm"
              style={{ animation: "pulseSoft 2s ease-in-out infinite" }}
            />
          </>
        )}
        {isIdle && (
          <span
            className="absolute inset-1 rounded-full bg-white/10 blur-[2px]"
            style={{ animation: "pulseSoft 3s ease-in-out infinite" }}
          />
        )}
        <div className="relative z-10 text-center">
          {isComplete ? (
            <svg className="mx-auto h-5 w-5 text-white sm:h-6 sm:w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : isActive ? (
            <svg className="mx-auto h-5 w-5 animate-spin text-white sm:h-6 sm:w-6" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          ) : (
            <svg className="mx-auto h-5 w-5 text-white/90 sm:h-6 sm:w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a10 10 0 1010 10M12 2v4M12 2l3 3M12 6l-3-3" />
            </svg>
          )}
        </div>
      </div>

      <p className="mt-2 text-xs font-semibold text-foreground/90 sm:text-sm">
        {cfg.title}
      </p>

      <div className="mt-0.5 space-y-0.5">
        {isIdle && (
          <>
            <p className="text-[10px] text-muted-foreground/70 sm:text-xs">
              {advisorCount} Advisors &middot; Transparency Enabled
            </p>
            <p className="text-[10px] text-muted-foreground/50">
              {cfg.subtitle}
            </p>
          </>
        )}

        {isActive && (
          <>
            <p className="text-[10px] text-muted-foreground/70 sm:text-xs">
              Step {stepsComplete + 1}/{stepsTotal}
              {conflictsActive > 0 && (
                <span className="ml-1.5 text-rose-400">
                  &middot; {conflictsActive} Conflict{conflictsActive > 1 ? "s" : ""}
                </span>
              )}
            </p>
            {consensusLevel > 0 && (
              <div className="mt-1 flex items-center justify-center gap-1.5">
                <div className="h-1 w-16 overflow-hidden rounded-full bg-border sm:w-20">
                  <div
                    className={cn(
                      "h-full rounded-full transition-all duration-700",
                      phase === "conflict"
                        ? "bg-gradient-to-r from-rose-500 to-orange-400"
                        : "bg-gradient-to-r from-primary to-primary-400"
                    )}
                    style={{ width: `${consensusLevel}%` }}
                  />
                </div>
                <span className="text-[10px] tabular-nums text-muted-foreground">
                  {consensusLevel}%
                </span>
              </div>
            )}
          </>
        )}

        {isComplete && (
          <>
            {confidence != null && (
              <p className="text-[10px] text-muted-foreground/70 sm:text-xs">
                Confidence {Math.round(confidence * 100)}%
                {wisdomScore != null && (
                  <span className="ml-1.5 text-primary">
                    &middot; Wisdom {wisdomScore}
                  </span>
                )}
              </p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
