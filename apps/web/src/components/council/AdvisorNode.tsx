import { AdvisorIcon } from "./icons";
import type { AdvisorData } from "./types";

interface AdvisorNodeProps {
  advisor: AdvisorData;
  style?: React.CSSProperties;
}

function alpha(c: string): string {
  return c + "8C";
}

export function AdvisorNode({ advisor, style }: AdvisorNodeProps) {
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
            background: `radial-gradient(circle at 40% 35%, ${alpha(color)} 0%, hsl(var(--background) / 0.9) 70%)`,
          }}
        >
          <AdvisorIcon id={advisor.id} size={32} color={color} />
        </div>
        <span className="text-foreground font-semibold text-sm text-center leading-tight">
          {advisor.name}
        </span>
        <span className="text-muted text-[11px] text-center leading-tight">
          {advisor.role}
        </span>
        <div className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-green-400" />
          <span className="text-[11px] text-[#22c55e]">Ready</span>
        </div>
      </div>
    </div>
  );
}
