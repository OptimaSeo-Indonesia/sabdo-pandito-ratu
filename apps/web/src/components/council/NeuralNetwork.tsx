import { useEffect, useRef } from "react";
import type { NeuralConnection, ConnectionState } from "./types";

interface NeuralNetworkProps {
  connections: NeuralConnection[];
  positions: Record<string, { x: number; y: number }>;
  width: number;
  height: number;
}

const CONNECTION_COLORS: Record<ConnectionState, string> = {
  idle: "rgba(99, 102, 241, 0.08)",
  active: "rgba(99, 102, 241, 0.3)",
  agree: "rgba(52, 211, 153, 0.4)",
  disagree: "rgba(251, 191, 36, 0.4)",
  conflict: "rgba(251, 113, 133, 0.5)",
  consensus: "rgba(99, 102, 241, 0.25)",
};

const GLOW_COLORS: Record<ConnectionState, string> = {
  idle: "rgba(99, 102, 241, 0)",
  active: "rgba(99, 102, 241, 0.1)",
  agree: "rgba(52, 211, 153, 0.15)",
  disagree: "rgba(251, 191, 36, 0.15)",
  conflict: "rgba(251, 113, 133, 0.2)",
  consensus: "rgba(99, 102, 241, 0.08)",
};

export function NeuralNetwork({
  connections,
  positions,
  width,
  height,
}: NeuralNetworkProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  return (
    <svg
      ref={svgRef}
      className="pointer-events-none absolute inset-0 h-full w-full"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        {(["idle", "active", "agree", "disagree", "conflict", "consensus"] as ConnectionState[]).map((state) => (
          <filter key={state} id={`glow-${state}`}>
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        ))}
      </defs>
      {connections.map((conn, i) => {
        const from = positions[conn.from];
        const to = positions[conn.to];
        if (!from || !to) return null;

        const color = CONNECTION_COLORS[conn.state];
        const glow = GLOW_COLORS[conn.state];

        return (
          <g key={`${conn.from}-${conn.to}`}>
            <line
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={color}
              strokeWidth="1.5"
              filter={`url(#glow-${conn.state})`}
              className="transition-all duration-700"
            />
            {conn.state !== "idle" && (
              <circle
                r="2"
                fill={color}
                filter={`url(#glow-${conn.state})`}
              >
                <animateMotion
                  dur={`${2 + i * 0.5}s`}
                  repeatCount="indefinite"
                  path={`M${from.x},${from.y} L${to.x},${to.y}`}
                />
              </circle>
            )}
          </g>
        );
      })}
    </svg>
  );
}
