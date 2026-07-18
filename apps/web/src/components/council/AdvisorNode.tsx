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

const NODE_GLOWS: Record<string, string> = {
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
  className,
  style,
}: AdvisorNodeProps) {
  const nodeKey = name.toLowerCase();
  const gradient = NODE_COLORS[nodeKey] || color;
  const glow = NODE_GLOWS[nodeKey] || "shadow-primary/20";

  return (
    <div
      className={cn(
        "group absolute flex flex-col items-center transition-all duration-500",
        isActive && "z-10",
        className
      )}
      style={style}
    >
      <div
        className={cn(
          "relative flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br shadow-xl transition-all duration-500 sm:h-20 sm:w-20",
          gradient,
          glow,
          "shadow-[0_0_30px_var(--tw-shadow-color)]",
          isActive && "scale-110 shadow-[0_0_50px_var(--tw-shadow-color)]"
        )}
      >
        <Icon className="h-7 w-7 text-white sm:h-8 sm:w-8" />
        {isActive && (
          <span className="absolute -inset-1 animate-ping rounded-2xl bg-white/10" />
        )}
      </div>
      <div className="mt-2 text-center">
        <p className="text-xs font-semibold text-foreground sm:text-sm">{name}</p>
        <p className="text-[10px] text-muted-foreground/70 sm:text-xs">{role}</p>
      </div>

      {status !== "idle" && (
        <div className="mt-1.5 w-28 text-center sm:w-32">
          <div className="flex items-center justify-center gap-1.5">
            {status === "thinking" && (
              <span className="relative flex h-1.5 w-1.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-primary" />
              </span>
            )}
            {status === "done" && (
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
            )}
            <span
              className={cn(
                "text-[10px] leading-tight sm:text-xs",
                status === "thinking" && "text-primary",
                status === "done" && "text-success",
                status === "conflict" && "text-destructive",
                status === "idle" && "text-muted-foreground"
              )}
            >
              {statusLabel}
            </span>
          </div>
          {status === "thinking" && (
            <div className="mt-1 h-0.5 w-full overflow-hidden rounded-full bg-border">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
