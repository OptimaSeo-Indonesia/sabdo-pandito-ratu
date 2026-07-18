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

const ADVISOR_GRADIENTS: Record<string, string> = {
  sage: "from-violet-500/20 to-purple-700/20",
  strategist: "from-blue-500/20 to-indigo-700/20",
  guardian: "from-amber-500/20 to-orange-700/20",
  analyst: "from-emerald-500/20 to-teal-700/20",
  ethicist: "from-rose-500/20 to-pink-700/20",
  visionary: "from-cyan-500/20 to-blue-700/20",
};

const ICON_GRADIENTS: Record<string, string> = {
  sage: "from-violet-500 to-purple-700",
  strategist: "from-blue-500 to-indigo-700",
  guardian: "from-amber-500 to-orange-700",
  analyst: "from-emerald-500 to-teal-700",
  ethicist: "from-rose-500 to-pink-700",
  visionary: "from-cyan-500 to-blue-700",
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
  const glassGradient = ADVISOR_GRADIENTS[nodeKey] || ADVISOR_GRADIENTS.sage;
  const iconGradient = ICON_GRADIENTS[nodeKey] || ICON_GRADIENTS.sage;
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
            "relative flex h-20 w-20 items-center justify-center rounded-[20px] border border-white/10 bg-white/[0.05] backdrop-blur-[18px] shadow-xl transition-all duration-700 sm:h-24 sm:w-24",
            isActive && "scale-110",
            isThinking && "shadow-[0_0_30px_rgba(79,140,255,0.2)]",
            isDone && "shadow-[0_0_20px_rgba(52,211,153,0.2)]"
          )}
        >
          <div className={cn(
            "absolute inset-0 rounded-[20px] opacity-20",
            glassGradient
          )} />
          <div className={cn(
            "relative z-10 flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br sm:h-12 sm:w-12",
            iconGradient
          )}>
            <Icon className="h-5 w-5 text-white sm:h-6 sm:w-6" />
          </div>

          {isThinking && (
            <>
              <span className="absolute -inset-1 animate-ping rounded-[20px] bg-white/15" />
              <span className="absolute -inset-2 rounded-[20px] bg-white/5 blur-sm" />
            </>
          )}

          {isIdle && (
            <span
              className="absolute -inset-1 rounded-[20px] bg-white/5 blur-[2px]"
              style={{ animation: "pulseSoft 3s ease-in-out infinite" }}
            />
          )}

          {isConflict && (
            <span className="absolute -inset-1.5 animate-pulse rounded-[20px] border-2 border-rose-400/40" />
          )}
        </div>
      </div>

      <div className="mt-1.5 text-center">
        <p className="text-[10px] font-semibold text-foreground/90 sm:text-xs">{name}</p>
        <p className="text-[8px] text-muted-foreground/60 sm:text-[10px]">{role}</p>
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
