import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { useTheme } from "./theme-provider";
import { cn } from "../lib/utils";
import {
  Sun,
  Moon,
  Sparkles,
  Home,
  History,
  Menu,
  X,
} from "lucide-react";
import { Button } from "./ui/button";
import { useState } from "react";

const NAV_ITEMS = [
  { to: "/", label: "Home", icon: Home },
  { to: "/sessions", label: "History", icon: History },
];

export default function Layout({ children }: { children: ReactNode }) {
  const { theme, toggle } = useTheme();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="relative flex min-h-screen flex-col">
      <nav className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-600 shadow-lg shadow-primary/20">
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
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
            <div className="ml-2 h-5 w-px bg-border" />
            <Button
              variant="ghost"
              size="icon"
              onClick={toggle}
              className="ml-1"
              aria-label="Toggle theme"
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
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
          <div className="border-t border-border/50 px-4 pb-4 pt-2 md:hidden">
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
                      : "text-muted-foreground hover:bg-accent"
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
            <button
              onClick={toggle}
              className="mt-1 flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-accent"
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

      <main className="flex-1">{children}</main>

      <footer className="border-t border-border/50 py-8">
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
