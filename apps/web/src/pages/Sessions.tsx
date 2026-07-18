import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { listSessions, getSessionStats } from "../lib/api";
import type { SessionListItem, SessionStats } from "../types/api";
import { cn } from "../lib/utils";
import { Badge } from "../components/ui/badge";
import {
  FileText,
  BarChart3,
  TrendingUp,
  Users,
  ChevronRight,
  Loader2,
  Inbox,
  BrainCircuit,
} from "lucide-react";

function StatsCard({
  icon: Icon,
  label,
  value,
  color,
  delay,
}: {
  icon: typeof BarChart3;
  label: string;
  value: string | number;
  color: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="glass-card p-5"
    >
      <div className="flex items-center gap-3">
        <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${color}`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
        <div>
          <p className="text-2xl font-bold tabular-nums">{value}</p>
          <p className="text-xs text-muted-foreground">{label}</p>
        </div>
      </div>
    </motion.div>
  );
}

const STATUS_COLORS: Record<string, string> = {
  completed: "bg-success/10 text-success border-success/20",
  running: "bg-primary/10 text-primary border-primary/20",
  failed: "bg-destructive/10 text-destructive border-destructive/20",
  pending: "bg-muted text-muted-foreground border-border",
};

export default function Sessions() {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [stats, setStats] = useState<SessionStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, st] = await Promise.all([
          listSessions(),
          getSessionStats(),
        ]);
        setSessions(s.items);
        setStats(st);
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="aurora-bg relative min-h-screen">
      <div className="relative mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="mb-10">
            <Badge variant="default" className="mb-3 px-3 py-1">
              <BarChart3 className="mr-1.5 h-3 w-3" />
              Council History
            </Badge>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Session History
            </h1>
            <p className="mt-1 text-muted-foreground">
                  Review past deliberations and their outcomes
            </p>
          </div>

          {stats && (
            <div className="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatsCard
                icon={FileText}
                label="Total Sessions"
                value={stats.total_cases}
                color="bg-gradient-to-br from-primary to-primary-600"
                delay={0.1}
              />
              <StatsCard
                icon={TrendingUp}
                label="With Outcomes"
                value={stats.cases_with_outcomes}
                color="bg-gradient-to-br from-success to-emerald-600"
                delay={0.15}
              />
              <StatsCard
                icon={BarChart3}
                label="Avg Confidence"
                value={`${stats.avg_confidence}%`}
                color="bg-gradient-to-br from-violet-500 to-purple-600"
                delay={0.2}
              />
              <StatsCard
                icon={Users}
                label="Domains"
                value={stats.domains?.length || 0}
                color="bg-gradient-to-br from-cyan-500 to-blue-600"
                delay={0.25}
              />
            </div>
          )}

          <div className="glass-card overflow-hidden">
            {loading && (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="h-6 w-6 animate-spin text-primary" />
              </div>
            )}

            {!loading && sessions.length === 0 && (
              <div className="py-20 text-center">
                <Inbox className="mx-auto mb-4 h-12 w-12 text-muted-foreground/40" />
                <h3 className="text-lg font-medium text-muted-foreground">No sessions yet</h3>
                <p className="mt-1 text-sm text-muted-foreground/60">
                  Submit a question to start your first deliberation
                </p>
                <Link
                  to="/"
                  className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:underline"
                >
                  <BrainCircuit className="h-4 w-4" />
                  Ask a question
                </Link>
              </div>
            )}

            {!loading && sessions.length > 0 && (
              <div className="divide-y divide-border/50">
                {sessions.map((s, i) => (
                  <motion.div
                    key={s.session_id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.03 }}
                  >
                    <Link
                      to={`/session/${s.session_id}`}
                      className="group flex items-center gap-4 px-6 py-4 transition-colors hover:bg-accent/50"
                    >
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{s.question}</p>
                        <p className="mt-0.5 text-xs text-muted-foreground font-mono">
                          {s.session_id}
                        </p>
                      </div>
                      <Badge
                        variant="outline"
                        className={cn(
                          "shrink-0 border text-xs capitalize",
                          STATUS_COLORS[s.status] || "border-border"
                        )}
                      >
                        {s.status}
                      </Badge>
                      <ChevronRight className="h-4 w-4 shrink-0 text-muted-foreground/40 transition-transform group-hover:translate-x-0.5" />
                    </Link>
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
