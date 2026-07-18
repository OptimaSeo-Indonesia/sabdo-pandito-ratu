import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { useTheme } from "./theme-provider";
import { cn } from "../lib/utils";
import { Background } from "./background/Background";
import {
  Sun,
  Moon,
  Sparkles,
  Home,
  History,
  BookOpen,
  Settings,
  User,
  Menu,
  X,
} from "lucide-react";
import { Button } from "./ui/button";
import { useState } from "react";

const NAV_ITEMS = [
  { to: "/", label: "Home", icon: Home },
  { to: "/sessions", label: "History", icon: History },
  { to: "/docs", label: "Documentation", icon: BookOpen },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Layout({ children }: { children: ReactNode }) {
  const { theme, toggle } = useTheme();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="relative flex min-h-screen flex-col">
      <Background />
      <nav className="sticky top-0 z-50 h-[72px] border-b border-white/10 bg-white/[0.03] backdrop-blur-[18px] supports-[backdrop-filter]:bg-white/[0.02]">
        <div className="mx-auto flex h-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-[#3A6FD8] shadow-lg shadow-primary/20">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <span className="text-lg font-semibold tracking-tight">
              Sabdo{" "}
              <span className="text-gradient">Pandito</span>{" "}
              Ratu
            </span>
          </Link>

          <div className="hidden items-center gap-1 md:flex">
            {NAV_ITEMS.map((item) => {
              const isActive = location.pathname === item.to;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-white/5"
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
            <div className="ml-2 h-5 w-px bg-white/10" />
            <Button
              variant="ghost"
              size="icon"
              onClick={toggle}
              className="ml-1 h-9 w-9"
              aria-label="Toggle theme"
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-9 w-9"
              aria-label="Profile"
            >
              <User className="h-4 w-4" />
            </Button>
          </div>

          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>

        {mobileOpen && (
          <div className="border-t border-white/10 bg-black/20 px-4 pb-4 pt-2 backdrop-blur-[18px] md:hidden">
            {NAV_ITEMS.map((item) => {
              const isActive = location.pathname === item.to;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-white/5"
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
            <button
              onClick={toggle}
              className="mt-1 flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-white/5"
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
              {theme === "dark" ? "Light" : "Dark"} Mode
            </button>
          </div>
        )}
      </nav>

      <main className="flex-1 px-4 sm:px-8 lg:px-[64px]">{children}</main>

      <footer className="border-t border-white/10 py-8">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <p className="text-sm text-muted-foreground">
            Sabdo Pandito Ratu &mdash;{" "}
            <span className="text-gradient font-medium">
              Multi-AI Deliberation Engine
            </span>
          </p>
          <p className="mt-1 text-xs text-muted-foreground/60">
            Open Source &middot; Transparent &middot; Reasoned Verdicts
          </p>
        </div>
      </footer>
    </div>
  );
}
