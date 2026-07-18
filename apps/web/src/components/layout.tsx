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
    <div className="flex h-screen flex-col bg-[#03030e] text-foreground">
      <div className="flex flex-1 overflow-hidden">
        <aside className="flex w-[240px] shrink-0 flex-col bg-sidebar py-5 px-3 overflow-hidden">
          <Link to="/" className="flex items-center gap-2 px-4 mb-6">
            <img
              src="https://c.animaapp.com/mrqrcjormMWdDO/img/brand-logo-gunungan.png"
              alt="Sabdo Pandito Ratu"
              className="h-12 w-auto"
            />
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
              <p className="text-xs text-muted mb-1">Wisdom Today</p>
              <p className="text-lg font-bold text-foreground">3</p>
              <p className="text-[11px] text-muted">Deliberations</p>
              <div className="mt-2 h-[3px] rounded-full bg-progress-track overflow-hidden">
                <div className="h-full w-[91%] rounded-full bg-grad-primary-btn" />
              </div>
              <p className="mt-1 text-[11px] text-muted">91% Avg. Wisdom Score</p>
            </div>

            <p className="mt-4 text-[10px] text-muted text-center">
              &copy; 2025 Sabdo Pandito Ratu
            </p>
          </div>
        </aside>

        <main className="flex flex-1 flex-col overflow-y-auto">
          <div className="container-app flex flex-1 flex-col gap-6 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
