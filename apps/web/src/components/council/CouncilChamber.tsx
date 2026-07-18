import { useState, useEffect, useCallback, useRef } from "react";
import { AdvisorNode } from "./AdvisorNode";
import { NeuralNetwork } from "./NeuralNetwork";
import { CouncilCore } from "./CouncilCore";
import { cn } from "../../lib/utils";
import {
  Brain,
  Scale,
  Shield,
  Eye,
  Lightbulb,
  Sparkles,
} from "lucide-react";
import type {
  AdvisorData,
  AdvisorState,
  NeuralConnection,
  ConnectionState,
  CouncilPhase,
} from "./types";

const ADVISORS: AdvisorData[] = [
  { id: "sage", name: "Sage", role: "Wisdom & Ethics", color: "from-violet-500 to-purple-700", icon: Brain },
  { id: "guardian", name: "Guardian", role: "Risk & Security", color: "from-amber-500 to-orange-700", icon: Shield },
  { id: "strategist", name: "Strategist", role: "Long-term Planning", color: "from-blue-500 to-indigo-700", icon: Eye },
  { id: "analyst", name: "Analyst", role: "Evidence & Logic", color: "from-emerald-500 to-teal-700", icon: Scale },
  { id: "ethicist", name: "Ethicist", role: "Fairness & Rights", color: "from-rose-500 to-pink-700", icon: Sparkles },
  { id: "visionary", name: "Visionary", role: "Innovation", color: "from-cyan-500 to-blue-700", icon: Lightbulb },
];

const IDLE_STATUSES = [
  "Awaiting query...",
  "Standing by...",
  "Prepared...",
  "Ready...",
];

const THINKING_PHRASES: Record<string, string[]> = {
  sage: [
    "Evaluating ethical principles...",
    "Weighing moral implications...",
    "Considering virtue framework...",
    "Assessing wisdom alignment...",
  ],
  guardian: [
    "Scanning for risks...",
    "Assessing security threats...",
    "Evaluating safeguards...",
    "Checking stability...",
  ],
  strategist: [
    "Projecting long-term impact...",
    "Analyzing systemic effects...",
    "Mapping future scenarios...",
    "Calculating trajectories...",
  ],
  analyst: [
    "Gathering evidence...",
    "Cross-referencing sources...",
    "Confidence increasing...",
    "Quantifying uncertainty...",
  ],
  ethicist: [
    "Checking fairness...",
    "Evaluating rights impact...",
    "Scanning for bias...",
    "Assessing inclusivity...",
  ],
  visionary: [
    "Generating alternatives...",
    "Exploring possibilities...",
    "Connecting insights...",
    "Synthesizing perspectives...",
  ],
};

const POSITIONS = {
  sage: { x: 50, y: 10 },
  guardian: { x: 18, y: 28 },
  strategist: { x: 82, y: 28 },
  core: { x: 50, y: 47 },
  analyst: { x: 18, y: 66 },
  ethicist: { x: 82, y: 66 },
  visionary: { x: 50, y: 85 },
};

const INITIAL_CONNECTIONS: NeuralConnection[] = [
  { from: "sage", to: "guardian", state: "idle" },
  { from: "sage", to: "strategist", state: "idle" },
  { from: "guardian", to: "strategist", state: "idle" },
  { from: "guardian", to: "analyst", state: "idle" },
  { from: "strategist", to: "ethicist", state: "idle" },
  { from: "analyst", to: "ethicist", state: "idle" },
  { from: "analyst", to: "visionary", state: "idle" },
  { from: "ethicist", to: "visionary", state: "idle" },
  { from: "sage", to: "core", state: "idle" },
  { from: "guardian", to: "core", state: "idle" },
  { from: "strategist", to: "core", state: "idle" },
  { from: "analyst", to: "core", state: "idle" },
  { from: "ethicist", to: "core", state: "idle" },
  { from: "visionary", to: "core", state: "idle" },
  { from: "guardian", to: "ethicist", state: "idle" },
  { from: "strategist", to: "analyst", state: "idle" },
];

function randomItem<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

interface CouncilChamberProps {
  className?: string;
  compact?: boolean;
  phase?: CouncilPhase;
  advisorStates?: AdvisorState[];
  consensusLevel?: number;
  verdict?: string;
  onPhaseChange?: (phase: CouncilPhase) => void;
}

export function CouncilChamber({
  className,
  compact = false,
  phase: externalPhase,
  advisorStates: externalAdvisorStates,
  consensusLevel: externalConsensus = 0,
  verdict,
  onPhaseChange,
}: CouncilChamberProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 400, height: 500 });

  const [internalAdvisorStates, setInternalAdvisorStates] = useState<
    AdvisorState[]
  >(() =>
    ADVISORS.map((a) => ({
      id: a.id,
      status: "idle",
      statusLabel: randomItem(IDLE_STATUSES),
      progress: 0,
    }))
  );

  const [connections, setConnections] =
    useState<NeuralConnection[]>(INITIAL_CONNECTIONS);

  const [internalPhase, setInternalPhase] = useState<CouncilPhase>("idle");
  const phase = externalPhase || internalPhase;

  const advisorStates = externalAdvisorStates || internalAdvisorStates;

  useEffect(() => {
    if (!containerRef.current) return;
    const obs = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setContainerSize({ width, height });
      }
    });
    obs.observe(containerRef.current);
    return () => obs.disconnect();
  }, []);

  const getAdvisorPosition = useCallback(
    (id: string) => {
      const p = POSITIONS[id as keyof typeof POSITIONS];
      if (!p) return { x: 0, y: 0 };
      return {
        x: (p.x / 100) * containerSize.width,
        y: (p.y / 100) * containerSize.height,
      };
    },
    [containerSize]
  );

  const idleCycleRef = useRef<ReturnType<typeof setInterval>>();

  useEffect(() => {
    if (phase !== "idle") {
      if (idleCycleRef.current) clearInterval(idleCycleRef.current);
      return;
    }

    idleCycleRef.current = setInterval(() => {
      setInternalAdvisorStates((prev) =>
        prev.map((s) => ({
          ...s,
          statusLabel:
            Math.random() > 0.6
              ? randomItem(IDLE_STATUSES)
              : s.statusLabel,
        }))
      );
    }, 4000);

    return () => {
      if (idleCycleRef.current) clearInterval(idleCycleRef.current);
    };
  }, [phase]);

  const isIdle = phase === "idle";
  const showAsThinking = phase !== "idle" && phase !== "verdict";

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative w-full",
        compact ? "aspect-[4/5] max-h-[400px]" : "aspect-[4/5] max-h-[600px]",
        className
      )}
    >
      <NeuralNetwork
        connections={connections}
        positions={Object.fromEntries(
          [...ADVISORS.map((a) => a.id), "core"].map((id) => [
            id,
            getAdvisorPosition(id),
          ])
        )}
        width={containerSize.width}
        height={containerSize.height}
      />

      {ADVISORS.map((advisor) => {
        const pos = POSITIONS[advisor.id as keyof typeof POSITIONS];
        const state = advisorStates.find((s) => s.id === advisor.id);
        const isActive =
          state?.status === "thinking" || state?.status === "conflict";

        return (
          <AdvisorNode
            key={advisor.id}
            name={advisor.name}
            role={advisor.role}
            icon={advisor.icon}
            color={advisor.color}
            status={state?.status || "idle"}
            statusLabel={state?.statusLabel || ""}
            progress={state?.progress || 0}
            isActive={isActive}
            style={{
              left: `${pos.x}%`,
              top: `${pos.y}%`,
              transform: "translate(-50%, -50%)",
            }}
          />
        );
      })}

      <CouncilCore
        phase={phase}
        consensusLevel={externalConsensus}
        verdict={verdict}
        style={{
          left: `${POSITIONS.core.x}%`,
          top: `${POSITIONS.core.y}%`,
          transform: "translate(-50%, -50%)",
        }}
      />
    </div>
  );
}

export { ADVISORS, THINKING_PHRASES, IDLE_STATUSES, POSITIONS };
