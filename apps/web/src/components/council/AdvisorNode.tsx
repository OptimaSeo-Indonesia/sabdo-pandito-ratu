import { type LucideIcon } from "lucide-react";
import { cn } from "../../lib/utils";

interface AdvisorNodeProps {
  name: string;
  role: string;
  icon: LucideIcon;
  color: string;
  status: string;
  statusLabel: string;
  progress: number;
  isActive: boolean;
  score?: number;
  scoreLabel?: string;
  className?: string;
  style?: React.CSSProperties;
}

const NODE_COLORS: Record<string, string> = {
  sage: "from-violet-500 to-purple-700",
  strategist: "from-blue-500 to-indigo-700",
  guardian: "from-amber-500 to-orange-700",
  analyst: "from-emerald-500 to-teal-700",
  ethicist: "from-rose-500 to-pink-700",
  visionary: "from-cyan-500 to-blue-700",
};

const GLOW_CLASSES: Record<string, string> = {
  sage: "shadow-violet-500/20",
  strategist: "shadow-blue-500/20",
  guardian: "shadow-amber-500/20",
  analyst: "shadow-emerald-500/20",
  ethicist: "shadow-rose-500/20",
  visionary: "shadow-cyan-500/20",
};

export function AdvisorNode({
  name,
  role,
  icon: Icon,
  color,
  status,
  statusLabel,
  progress,
  isActive,
  score,
  scoreLabel,
  className,
  style,
}: AdvisorNodeProps) {
  const nodeKey = name.toLowerCase();
  const gradient = NODE_COLORS[nodeKey] || color;
  const glowClass = GLOW_CLASSES[nodeKey] || "shadow-primary/20";
  const isThinking = status === "thinking";
  const isDone = status === "done";
  const isConflict = status === "conflict";
  const isIdle = status === "idle";

  return (
    <div
      className={cn(
        "group absolute flex flex-col items-center transition-all duration-700",
        isActive && "z-10",
        className
      )}
      style={style}
    >
      <div className="relative">
        <div
          className={cn(
            "relative flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br shadow-xl transition-all duration-700 sm:h-16 sm:w-16",
            gradient,
            glowClass,
            isActive && "scale-110",
            isThinking && "shadow-[0_0_30px_var(--tw-shadow-color)]",
            isDone && "shadow-[0_0_20px_var(--tw-shadow-color)]"
          )}
        >
          <Icon className="h-6 w-6 text-white sm:h-7 sm:w-7" />

          {isThinking && (
            <>
              <span className="absolute -inset-1 animate-ping rounded-2xl bg-white/15" />
              <span className="absolute -inset-2 rounded-2xl bg-white/5 blur-sm" />
            </>
          )}

          {isIdle && (
            <span
              className="absolute -inset-1 rounded-2xl bg-white/5 blur-[2px]"
              style={{ animation: "pulseSoft 3s ease-in-out infinite" }}
            />
          )}

          {isConflict && (
            <span className="absolute -inset-1.5 animate-pulse rounded-2xl border-2 border-rose-400/40" />
          )}
        </div>
      </div>

      <div className="mt-1.5 text-center">
        <p className="text-[11px] font-semibold text-foreground/90 sm:text-xs">{name}</p>
        <p className="text-[9px] text-muted-foreground/60 sm:text-[10px]">{role}</p>
      </div>

      {status !== "idle" && (
        <div className="mt-1 w-24 text-center sm:w-28">
          <p
            className={cn(
              "text-[9px] leading-tight sm:text-[10px]",
              isThinking && "text-primary",
              isDone && "text-success",
              isConflict && "text-destructive"
            )}
          >
            {isThinking && (
              <span className="mr-1 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-primary align-middle" />
            )}
            {statusLabel}
          </p>

          {isThinking && (
            <div className="mt-1 h-1 overflow-hidden rounded-full bg-border">
              <div
                className="h-full rounded-full bg-gradient-to-r from-primary/80 to-primary transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          )}

          {score != null && (
            <div className="mt-0.5 flex items-center justify-center gap-1">
              <div className="h-0.5 w-8 overflow-hidden rounded-full bg-border sm:w-10">
                <div
                  className={cn(
                    "h-full rounded-full transition-all duration-500",
                    score >= 70 ? "bg-success" : score >= 40 ? "bg-warning" : "bg-destructive"
                  )}
                  style={{ width: `${score}%` }}
                />
              </div>
              <span className="text-[9px] tabular-nums font-medium text-muted-foreground sm:text-[10px]">
                {scoreLabel || `${score}%`}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
