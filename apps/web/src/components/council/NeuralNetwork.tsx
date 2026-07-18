import { useRef, useMemo } from "react";
import type { NeuralConnection } from "./types";

interface NeuralNetworkProps {
  connections: NeuralConnection[];
  positions: Record<string, { x: number; y: number }>;
  width: number;
  height: number;
  phase: string;
}

type ConnColor =
  | "idle"
  | "active"
  | "agree"
  | "debating"
  | "conflict"
  | "reflection"
  | "consensus";

const LINE_COLORS: Record<ConnColor, { main: string; glow: string; width: number }> = {
  idle: { main: "rgba(99,102,241,0.06)", glow: "rgba(99,102,241,0)", width: 1 },
  active: { main: "rgba(99,102,241,0.25)", glow: "rgba(99,102,241,0.08)", width: 1.5 },
  agree: { main: "rgba(52,211,153,0.35)", glow: "rgba(52,211,153,0.15)", width: 1.5 },
  debating: { main: "rgba(251,191,36,0.35)", glow: "rgba(251,191,36,0.15)", width: 1.5 },
  conflict: { main: "rgba(251,113,133,0.45)", glow: "rgba(251,113,133,0.2)", width: 2 },
  reflection: { main: "rgba(167,139,250,0.35)", glow: "rgba(167,139,250,0.15)", width: 1.5 },
  consensus: { main: "rgba(99,102,241,0.2)", glow: "rgba(99,102,241,0.08)", width: 1 },
};

const LABEL_OFFSETS: Record<string, { x: number; y: number }> = {
  "sage-guardian": { x: 0, y: -8 },
  "sage-strategist": { x: 0, y: -8 },
  "guardian-strategist": { x: 0, y: -10 },
  "guardian-analyst": { x: -10, y: 0 },
  "strategist-ethicist": { x: 10, y: 0 },
  "analyst-ethicist": { x: 0, y: 10 },
  "analyst-visionary": { x: 0, y: 8 },
  "ethicist-visionary": { x: 0, y: 8 },
  "guardian-ethicist": { x: -8, y: 0 },
  "strategist-analyst": { x: 8, y: 0 },
};

const CONN_LABELS: Record<ConnColor, string> = {
  idle: "",
  active: "",
  agree: "Agree",
  debating: "Debate",
  conflict: "Conflict",
  reflection: "Reflect",
  consensus: "Consensus",
};

export function NeuralNetwork({
  connections,
  positions,
  width,
  height,
  phase,
}: NeuralNetworkProps) {
  const uniqueId = useMemo(() => Math.random().toString(36).slice(2, 6), []);

  return (
    <svg
      className="pointer-events-none absolute inset-0 h-full w-full"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <filter id={`ng-${uniqueId}`}>
          <feGaussianBlur stdDeviation="2.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <filter id={`ng-s-${uniqueId}`}>
          <feGaussianBlur stdDeviation="1.5" />
        </filter>
      </defs>

      {connections.map((conn) => {
        const from = positions[conn.from];
        const to = positions[conn.to];
        if (!from || !to) return null;

        const key = [conn.from, conn.to].sort().join("-");
        const colors = LINE_COLORS[conn.state as ConnColor] || LINE_COLORS.idle;
        const midX = (from.x + to.x) / 2;
        const midY = (from.y + to.y) / 2;
        const label = CONN_LABELS[conn.state as ConnColor];
        const offset = LABEL_OFFSETS[key];

        return (
          <g key={`${conn.from}-${conn.to}`}>
            <line
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={colors.glow}
              strokeWidth={colors.width + 4}
              filter={`url(#ng-s-${uniqueId})`}
              className="transition-all duration-700"
            />
            <line
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={colors.main}
              strokeWidth={colors.width}
              strokeLinecap="round"
              filter={`url(#ng-${uniqueId})`}
              strokeDasharray={conn.state !== "idle" ? "4 6" : "none"}
              className="transition-all duration-700"
            >
              {conn.state !== "idle" && (
                <animate attributeName="stroke-dashoffset" from="0" to="-20" dur="1s" repeatCount="indefinite" />
              )}
            </line>

            <circle
              cx={from.x}
              cy={from.y}
              r={conn.state !== "idle" ? 2.5 : 1.5}
              fill={colors.main}
              filter={`url(#ng-${uniqueId})`}
              className="transition-all duration-500"
            />

            {label && offset && (
              <text
                x={midX + (offset.x || 0)}
                y={midY + (offset.y || 0)}
                textAnchor="middle"
                dominantBaseline="middle"
                fill={colors.main}
                fontSize="8"
                fontFamily="system-ui"
                className="transition-all duration-500"
                style={{ opacity: 0.7 }}
              >
                {label}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}
