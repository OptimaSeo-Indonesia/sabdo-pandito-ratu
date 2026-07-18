import { useState, useEffect, useCallback, useRef } from "react";
import { AdvisorNode } from "./AdvisorNode";
import { NeuralNetwork } from "./NeuralNetwork";
import { CouncilCore } from "./CouncilCore";
import { cn } from "../../lib/utils";
import {
  Brain, Scale, Shield, Eye, Lightbulb, Sparkles,
} from "lucide-react";
import type { AdvisorData, AdvisorState, NeuralConnection, ConnectionState } from "./types";

const ADVISORS: AdvisorData[] = [
  { id: "sage", name: "Sage", role: "Wisdom & Ethics", color: "from-violet-500 to-purple-700", icon: Brain },
  { id: "guardian", name: "Guardian", role: "Risk & Security", color: "from-amber-500 to-orange-700", icon: Shield },
  { id: "strategist", name: "Strategist", role: "Long-term Planning", color: "from-blue-500 to-indigo-700", icon: Eye },
  { id: "analyst", name: "Analyst", role: "Evidence & Logic", color: "from-emerald-500 to-teal-700", icon: Scale },
  { id: "ethicist", name: "Ethicist", role: "Fairness & Rights", color: "from-rose-500 to-pink-700", icon: Sparkles },
  { id: "visionary", name: "Visionary", role: "Innovation", color: "from-cyan-500 to-blue-700", icon: Lightbulb },
];

const IDLE_PHRASES = [
  "Awaiting query", "Standing by", "Prepared", "Ready",
];

const THINKING_PHRASES: Record<string, string[]> = {
  sage: ["Evaluating ethics", "Weighing values", "Assessing wisdom", "Synthesizing"],
  guardian: ["Scanning risks", "Assessing threats", "Evaluating safety", "Stability check"],
  strategist: ["Projecting impact", "Analyzing systems", "Mapping scenarios", "Calculating"],
  analyst: ["Gathering evidence", "Cross-referencing", "Confidence rising", "Scoring"],
  ethicist: ["Checking fairness", "Rights impact", "Scanning bias", "Inclusivity"],
  visionary: ["Exploring ideas", "Connecting dots", "Generating paths", "Synthesizing"],
};

const POSITIONS = {
  sage: { x: 50, y: 8 },
  guardian: { x: 16, y: 27 },
  strategist: { x: 84, y: 27 },
  core: { x: 50, y: 48 },
  analyst: { x: 16, y: 67 },
  ethicist: { x: 84, y: 67 },
  visionary: { x: 50, y: 85 },
};

const BASE_CONNECTIONS: NeuralConnection[] = [
  { from: "sage", to: "guardian", state: "idle" }, { from: "sage", to: "strategist", state: "idle" },
  { from: "guardian", to: "strategist", state: "idle" }, { from: "guardian", to: "analyst", state: "idle" },
  { from: "strategist", to: "ethicist", state: "idle" }, { from: "analyst", to: "ethicist", state: "idle" },
  { from: "analyst", to: "visionary", state: "idle" }, { from: "ethicist", to: "visionary", state: "idle" },
  { from: "sage", to: "core", state: "idle" }, { from: "guardian", to: "core", state: "idle" },
  { from: "strategist", to: "core", state: "idle" }, { from: "analyst", to: "core", state: "idle" },
  { from: "ethicist", to: "core", state: "idle" }, { from: "visionary", to: "core", state: "idle" },
  { from: "guardian", to: "ethicist", state: "idle" }, { from: "strategist", to: "analyst", state: "idle" },
];

function pick<T>(arr: T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }

type Phase = "idle" | "deliberating" | "conflict" | "reflecting" | "consensus" | "verdict";

interface CouncilChamberProps {
  className?: string;
  compact?: boolean;
  phase?: Phase;
  consensusLevel?: number;
  stepsComplete?: number;
  stepsTotal?: number;
  conflictsActive?: number;
  confidence?: number;
  wisdomScore?: number;
  advisorStatuses?: Array<{ persona: string; stance: string; confidence: number }>;
}

export function CouncilChamber({
  compact = false,
  phase: externalPhase,
  consensusLevel: extConsensus = 0,
  stepsComplete = 0,
  stepsTotal = 9,
  conflictsActive = 0,
  confidence,
  wisdomScore,
  advisorStatuses,
  className,
}: CouncilChamberProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 400, height: 500 });

  const [phase, setPhase] = useState<Phase>("idle");
  const activePhase = externalPhase || phase;

  useEffect(() => {
    if (!advisorStatuses) return;
    setAdvisorStates((prev) =>
      prev.map((s) => {
        const match = advisorStatuses.find((a) => a.persona === s.id);
        if (!match) return s;
        return {
          ...s,
          status: "thinking" as const,
          confidence: match.confidence,
          stance: match.stance,
          progress: Math.round(match.confidence * 100),
          statusLabel: THINKING_PHRASES[s.id]
            ? pick(THINKING_PHRASES[s.id])
            : "Analyzing",
        };
      })
    );
  }, [advisorStatuses]);

  const [advisorStates, setAdvisorStates] = useState<AdvisorState[]>(() =>
    ADVISORS.map((a) => ({ id: a.id, status: "idle", statusLabel: pick(IDLE_PHRASES), progress: 0 }))
  );

  const [connections, setConnections] = useState<NeuralConnection[]>(BASE_CONNECTIONS);

  useEffect(() => {
    if (!ref.current) return;
    const obs = new ResizeObserver((entries) => {
      for (const e of entries) setSize({ width: e.contentRect.width, height: e.contentRect.height });
    });
    obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  const getPos = useCallback(
    (id: string) => {
      const p = POSITIONS[id as keyof typeof POSITIONS];
      return p ? { x: (p.x / 100) * size.width, y: (p.y / 100) * size.height } : { x: 0, y: 0 };
    },
    [size]
  );

  // Idle animation cycle
  useEffect(() => {
    if (activePhase !== "idle") return;
    const t = setInterval(() => {
      setAdvisorStates((prev) =>
        prev.map((s) => ({ ...s, statusLabel: Math.random() > 0.5 ? pick(IDLE_PHRASES) : s.statusLabel }))
      );
      setConnections((prev) =>
        prev.map((c) => {
          if (Math.random() > 0.85) return { ...c, state: "active" as ConnectionState };
          return { ...c, state: "idle" as ConnectionState };
        })
      );
      setTimeout(() => setConnections((prev) => prev.map((c) => ({ ...c, state: "idle" as ConnectionState }))), 1500);
    }, 4000);
    return () => clearInterval(t);
  }, [activePhase]);

  // Simulate deliberating connections
  useEffect(() => {
    if (activePhase === "idle" || activePhase === "verdict") return;
    const t = setInterval(() => {
      setConnections((prev) =>
        prev.map((c) => {
          const r = Math.random();
          if (activePhase === "conflict") {
            if ((c.from === "guardian" && c.to === "ethicist") || (c.from === "strategist" && c.to === "analyst"))
              return { ...c, state: "conflict" as ConnectionState };
            if (r > 0.6) return { ...c, state: "debating" as ConnectionState };
          }
          if (activePhase === "reflecting") {
            if (r > 0.5) return { ...c, state: "reflection" as ConnectionState };
          }
          if (activePhase === "consensus") {
            if (r > 0.4) return { ...c, state: "consensus" as ConnectionState };
          }
          if (r > 0.7) return { ...c, state: "active" as ConnectionState };
          if (r > 0.85) return { ...c, state: "agree" as ConnectionState };
          return { ...c, state: "active" as ConnectionState };
        })
      );
    }, 3000);
    return () => clearInterval(t);
  }, [activePhase]);

  // Verdict connections
  useEffect(() => {
    if (activePhase !== "verdict") return;
    setConnections((prev) => prev.map((c) => ({ ...c, state: "consensus" as ConnectionState })));
  }, [activePhase]);

  return (
    <div
      ref={ref}
      className={cn(
        "relative mx-auto w-full max-w-[620px]",
        compact ? "aspect-square max-h-[380px]" : "aspect-square",
        className
      )}
    >
      <NeuralNetwork
        connections={connections}
        positions={Object.fromEntries(
          [...ADVISORS.map((a) => a.id), "core"].map((id) => [id, getPos(id)])
        )}
        width={size.width}
        height={size.height}
        phase={activePhase}
      />

      {ADVISORS.map((a) => {
        const pos = POSITIONS[a.id as keyof typeof POSITIONS];
        const st = advisorStates.find((s) => s.id === a.id);
        return (
          <AdvisorNode
            key={a.id}
            name={a.name}
            role={a.role}
            icon={a.icon}
            color={a.color}
            status={st?.status || "idle"}
            statusLabel={st?.statusLabel || ""}
            progress={st?.progress || 0}
            isActive={st?.status === "thinking" || st?.status === "conflict"}
            score={st?.confidence != null ? Math.round(st.confidence * 100) : undefined}
            scoreLabel={st?.stance}
            style={{ left: `${pos.x}%`, top: `${pos.y}%`, transform: "translate(-50%, -50%)" }}
          />
        );
      })}

      <CouncilCore
        phase={activePhase}
        stepsComplete={stepsComplete}
        stepsTotal={stepsTotal}
        consensusLevel={extConsensus}
        conflictsActive={conflictsActive}
        confidence={confidence}
        wisdomScore={wisdomScore}
        style={{ left: `${POSITIONS.core.x}%`, top: `${POSITIONS.core.y}%`, transform: "translate(-50%, -50%)" }}
      />
    </div>
  );
}

export { ADVISORS, THINKING_PHRASES, IDLE_PHRASES, POSITIONS };
