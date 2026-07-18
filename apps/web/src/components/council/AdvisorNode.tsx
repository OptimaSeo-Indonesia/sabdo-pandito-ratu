import type { LucideIcon } from "lucide-react";
import type { AdvisorData } from "./types";

interface AdvisorNodeProps {
  advisor: AdvisorData;
  style?: React.CSSProperties;
}

function alpha(c: string): string {
  return c + "80"; // 50% opacity hex
}

function glow(c: string): string {
  return c + "4D"; // 30% opacity hex
}

export function AdvisorNode({ advisor, style }: AdvisorNodeProps) {
  const Icon = advisor.icon;
  const color = advisor.color;

  return (
    <div style={style}>
      <div className="flex flex-col items-center gap-1">
        <div
          className="flex items-center justify-center rounded-full"
          style={{
            width: "72px",
            height: "72px",
            border: `2px solid ${alpha(color)}`,
            background: `radial-gradient(circle at 40% 35%, ${glow(color)} 0%, rgba(3,7,22,0.9) 70%)`,
            boxShadow: `0 0 20px ${glow(color)}, 0 0 40px ${glow(color)}`,
          }}
        >
          <Icon size={32} strokeWidth={1.5} color={color} />
        </div>
        <span className="text-foreground font-semibold text-sm text-center leading-tight">
          {advisor.name}
        </span>
        <span className="text-muted text-[11px] text-center leading-tight">
          {advisor.role}
        </span>
        <div className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-[#22C55E] shadow-[0_0_6px_#22C55E]" />
          <span className="text-[11px] text-green-400">Ready</span>
        </div>
      </div>
    </div>
  );
}
