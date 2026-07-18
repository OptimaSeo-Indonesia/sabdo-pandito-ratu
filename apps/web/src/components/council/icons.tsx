import { User, Map, ShieldEllipsis, Brain, Lightbulb, Scale } from "lucide-react";
import type { LucideIcon } from "lucide-react";

const ICON_MAP: Record<string, LucideIcon> = {
  sage: User,
  strategist: Map,
  guardian: ShieldEllipsis,
  analyst: Brain,
  visionary: Lightbulb,
  ethicist: Scale,
};

interface IconProps {
  id: string;
  size?: number;
  color?: string;
  className?: string;
}

export function AdvisorIcon({ id, size = 24, color, className }: IconProps) {
  const Icon = ICON_MAP[id];
  if (!Icon) return null;
  return <Icon size={size} color={color} strokeWidth={1.5} className={className} />;
}
