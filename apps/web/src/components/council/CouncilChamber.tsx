import { AdvisorNode } from "./AdvisorNode";
import { CouncilCore } from "./CouncilCore";
import { cn } from "../../lib/utils";
import {
  Brain, Scale, Shield, Eye, Lightbulb, Sparkles,
} from "lucide-react";
import type { AdvisorData } from "./types";

const ADVISORS: AdvisorData[] = [
  { id: "sage", name: "Sage", role: "Wisdom & Ethics", color: "#814AFF", icon: Brain },
  { id: "guardian", name: "Guardian", role: "Risk & Security", color: "#E8A32E", icon: Shield },
  { id: "strategist", name: "Strategist", role: "Long-term Planning", color: "#3B82F6", icon: Eye },
  { id: "analyst", name: "Analyst", role: "Evidence & Logic", color: "#00C896", icon: Scale },
  { id: "ethicist", name: "Ethicist", role: "Fairness & Rights", color: "#FF58B8", icon: Sparkles },
  { id: "visionary", name: "Visionary", role: "Innovation", color: "#4A9EFF", icon: Lightbulb },
];

const POSITIONS: Record<string, { top: string; left: string }> = {
  sage: { top: "0%", left: "50%" },
  strategist: { top: "22%", left: "82%" },
  ethicist: { top: "62%", left: "82%" },
  visionary: { top: "84%", left: "50%" },
  analyst: { top: "62%", left: "18%" },
  guardian: { top: "22%", left: "18%" },
};

const SVG_VIEWBOX = "0 0 700 560";

// Hexagon vertices matching advisor positions
const HEX_POINTS = [
  { x: 350, y: 28 },   // sage
  { x: 574, y: 123 },  // strategist
  { x: 574, y: 347 },  // ethicist
  { x: 350, y: 470 },  // visionary
  { x: 126, y: 347 },  // analyst
  { x: 126, y: 123 },  // guardian
];

interface CouncilChamberProps {
  className?: string;
  compact?: boolean;
  phase?: string;
  consensusLevel?: number;
  stepsComplete?: number;
  stepsTotal?: number;
  conflictsActive?: number;
  confidence?: number;
  wisdomScore?: number;
  advisorStatuses?: Array<{ persona: string; stance: string; confidence: number }>;
}

export function CouncilChamber({ className }: CouncilChamberProps) {
  const hexString = HEX_POINTS.map(p => `${p.x},${p.y}`).join(" ");

  return (
    <section
      className={cn(
        "bg-transparent relative overflow-hidden",
        className
      )}
      style={{ minHeight: "580px" }}
    >
      {/* Gunungan Background */}
      <img
        src="https://c.animaapp.com/mrqrcjormMWdDO/img/background-gunungan-illustration.png"
        alt=""
        className="pointer-events-none absolute opacity-60"
        style={{ top: "5%", left: "-35%", width: "163%", aspectRatio: "445/604", zIndex: 0 }}
      />

      {/* SVG Connection Lines */}
      <div className="relative" style={{ zIndex: 1, minHeight: "560px" }}>
        <svg
          viewBox={SVG_VIEWBOX}
          className="pointer-events-none absolute inset-0 h-full w-full"
          preserveAspectRatio="xMidYMid meet"
        >
          {/* Hexagon outline */}
          <polyline
            points={hexString}
            fill="none"
            stroke="rgba(108, 99, 255, 0.25)"
            strokeWidth="1.5"
            strokeDasharray="4 4"
          />

          {/* Center circle */}
          <circle
            cx="350" cy="248" r="90"
            fill="none"
            stroke="rgba(108, 99, 255, 0.25)"
            strokeWidth="1"
            strokeDasharray="3 3"
          />

          {/* Connection lines from center to each hex vertex */}
          {HEX_POINTS.map((p, i) => (
            <line
              key={i}
              x1="350" y1="248"
              x2={p.x} y2={p.y}
              stroke="rgba(108, 99, 255, 0.2)"
              strokeWidth="1"
              strokeDasharray="4 4"
            />
          ))}

          {/* Inner junction points */}
          {HEX_POINTS.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r="3" fill="rgba(108, 99, 255, 0.4)" />
          ))}

          {/* Outer hexagonal ring dots */}
          {HEX_POINTS.map((p, i) => (
            <circle key={`outer-${i}`} cx={p.x} cy={p.y} r="4" fill="rgba(108, 99, 255, 0.15)" />
          ))}
        </svg>

        {/* Advisor Nodes */}
        {ADVISORS.map((a) => {
          const pos = POSITIONS[a.id];
          return (
            <AdvisorNode
              key={a.id}
              advisor={a}
              style={{
                position: "absolute",
                top: pos.top,
                left: pos.left,
                transform: "translateX(-50%)",
                zIndex: 10,
              }}
            />
          );
        })}

        {/* Council Core */}
        <CouncilCore
          style={{
            position: "absolute",
            top: "22.6%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            zIndex: 20,
          }}
        />
      </div>
    </section>
  );
}

export { ADVISORS, POSITIONS };
