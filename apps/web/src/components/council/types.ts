import type { LucideIcon } from "lucide-react";

export interface AdvisorData {
  id: string;
  name: string;
  role: string;
  color: string;
  icon: LucideIcon;
}

export interface AdvisorState {
  id: string;
  status: string;
  statusLabel: string;
  progress: number;
  stance?: string;
  confidence?: number;
}

export type ConnectionState = "idle" | "active" | "agree" | "disagree" | "conflict" | "consensus";
export type CouncilPhase = "idle" | "deliberating" | "conflict" | "reflecting" | "consensus" | "verdict";

export interface NeuralConnection {
  from: string;
  to: string;
  state: ConnectionState;
}
