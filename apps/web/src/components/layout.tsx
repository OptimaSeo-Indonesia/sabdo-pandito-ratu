import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "../lib/utils";
import {
  Home,
  Layers,
  History,
  Users,
  BookOpen,
  BarChart3,
  Settings,
  FileText,
  Heart,
  Astroid,
} from "lucide-react";

const SIDEBAR_ITEMS = [
  { to: "/", label: "Home", icon: Home, match: (p: string) => p === "/" },
  { to: "/deliberations", label: "Deliberations", icon: Layers, match: (p: string) => p.startsWith("/deliberations") || p.startsWith("/session/") },
  { to: "/sessions", label: "History", icon: History, match: (p: string) => p === "/sessions" },
  { to: "/council", label: "Council", icon: Users, match: (p: string) => p.startsWith("/council") },
  { to: "/knowledge", label: "Knowledge", icon: BookOpen, match: (p: string) => p.startsWith("/knowledge") },
  { to: "/analytics", label: "Analytics", icon: BarChart3, match: (p: string) => p.startsWith("/analytics") },
  { to: "/settings", label: "Settings", icon: Settings, match: (p: string) => p.startsWith("/settings") },
  { to: "/docs", label: "Documentation", icon: FileText, match: (p: string) => p.startsWith("/docs") },
];

export default function Layout({ children }: { children: ReactNode }) {
  const location = useLocation();

  return (
    <div className="relative z-10 flex h-screen flex-col bg-[#03030e] text-foreground">
      <div className="flex flex-1 overflow-hidden">
        <aside className="flex w-[240px] min-w-[240px] shrink-0 flex-col bg-sidebar py-5 px-3 overflow-hidden">
          <Link to="/" className="flex flex-col items-start gap-1 px-4 mb-6">
            <img
              src="/img/brand-logo-gunungan.png"
              alt="Sabdo Pandito Ratu"
              className="h-12 w-auto"
            />
            <span className="text-sm font-bold text-foreground leading-tight">Sabdo Pandito Ratu</span>
            <span className="text-[10px] text-muted leading-tight">Multi-AI Deliberation Engine</span>
          </Link>

          <nav className="flex flex-col gap-0">
            {SIDEBAR_ITEMS.map((item) => {
              const isActive = item.match(location.pathname);
              const Icon = item.icon;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    "flex items-center gap-3 px-4 py-[10px] rounded-[10px] text-sm font-medium transition-all",
                    isActive
                      ? "bg-grad-active-nav border border-[rgba(108,99,255,0.55)] text-foreground"
                      : "text-muted hover:text-foreground hover:bg-[rgba(108,99,255,0.06)]"
                  )}
                >
                  <Icon className={cn("h-4 w-4", isActive ? "text-primary" : "text-muted")} />
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <div className="mt-auto px-1">
            <div className="bg-card card-ref rounded-2xl p-4">
              <div className="flex items-center gap-2 mb-1">
                <img
                  src="/img/council-core-emblem.png"
                  alt=""
                  className="w-4 h-4 object-contain"
                />
                <p className="text-xs text-muted">Wisdom Today</p>
              </div>
              <p className="text-lg font-bold text-foreground">3</p>
              <p className="text-[11px] text-muted">Deliberations</p>
              <div className="mt-2 h-[3px] rounded-full bg-progress-track overflow-hidden">
                <div className="h-full w-[91%] rounded-full bg-grad-primary-btn" />
              </div>
              <p className="mt-1 text-[11px] text-muted">91% Avg. Wisdom Score</p>
            </div>
          </div>
        </aside>

        <main className="flex flex-1 flex-col overflow-y-auto">
          <div className="container-app flex flex-1 flex-col gap-6 py-6">
            {children}
          </div>
        </main>
      </div>

      {/* Full-width Footer */}
      <footer className="border-t border-white/5 py-3 px-6 shrink-0">
        <div className="container-app mx-auto flex items-center justify-between text-[11px] text-muted/60">
          <span>&copy; 2026 Sabdo Pandito Ratu</span>
          <span className="flex items-center gap-3 text-[12px] text-muted/50 italic">
            <Astroid className="h-3 w-3 text-primary/50" />
            Kebijaksanaan lahir dari keberagaman perspektif.
            <Astroid className="h-3 w-3 text-primary/50" />
          </span>
          <span className="flex items-center gap-1.5">
            <span>Open Source Deliberation Engine</span>
            <Heart className="h-3 w-3 text-danger" />
            <svg viewBox="0 0 24 24" className="h-3 w-3" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
          </span>
        </div>
      </footer>

      {/* Gunungan watermark background */}
      <div className="fixed inset-0 pointer-events-none z-0 flex items-center justify-center opacity-[0.04]"
        style={{ transform: 'translateX(-15%)' }}>
        <img
          src="/img/brand-logo-gunungan.png"
          alt=""
          className="h-full w-auto object-contain max-h-screen"
        />
      </div>
    </div>
  );
}
