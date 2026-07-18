import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { startDeliberation, startDryRun } from "../lib/api";
import { cn } from "../lib/utils";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import {
  Sparkles,
  ArrowRight,
  Zap,
  Brain,
  Shield,
  Eye,
  Scale,
  Lightbulb,
  Send,
  Upload,
  Mic,
  CheckCircle2,
  Loader2,
} from "lucide-react";

const EXAMPLE_PROMPTS = [
  "Should universal basic income be implemented globally?",
  "What is the ethical approach to AI regulation?",
  "How should we address climate change?",
  "Should remote work become the standard?",
];

const ADVISORS = [
  { name: "Sage", icon: Brain, role: "Wisdom & Ethics", color: "from-violet-500 to-purple-600" },
  { name: "Strategist", icon: Eye, role: "Long-term Planning", color: "from-blue-500 to-indigo-600" },
  { name: "Analyst", icon: Scale, role: "Evidence & Logic", color: "from-emerald-500 to-teal-600" },
  { name: "Guardian", icon: Shield, role: "Risk & Security", color: "from-amber-500 to-orange-600" },
  { name: "Visionary", icon: Lightbulb, role: "Innovation", color: "from-cyan-500 to-blue-600" },
  { name: "Ethicist", icon: Sparkles, role: "Fairness & Rights", color: "from-rose-500 to-pink-600" },
];

const STEPS = [
  { step: 1, title: "Submit", desc: "Ask a question to the council" },
  { step: 2, title: "Analyze", desc: "Context & perspectives generated" },
  { step: 3, title: "Deliberate", desc: "Advisors debate & reflect" },
  { step: 4, title: "Conclude", desc: "Reasoned verdict delivered" },
];

export default function Home() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [useDryRun, setUseDryRun] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const fn = useDryRun ? startDryRun : startDeliberation;
      const result = await fn(question);
      navigate(`/session/${result.session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative">
      <div className="aurora-bg pointer-events-none fixed inset-0" />

      <div className="relative mx-auto max-w-5xl px-4 pb-24 pt-16 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="text-center"
        >
          <Badge variant="default" className="mb-6 px-4 py-1.5 text-xs font-medium tracking-wide uppercase">
            <Sparkles className="mr-1.5 h-3 w-3" />
            Multi-AI Deliberation Engine v0.1
          </Badge>
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
            Sabdo{" "}
            <span className="text-gradient">Pandito</span>{" "}
            Ratu
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground sm:text-xl">
            Ask a question. Six AI advisors deliberate, challenge assumptions,
            and deliver a transparent, reasoned verdict.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15, ease: "easeOut" }}
          className="mt-10"
        >
          <form onSubmit={handleSubmit}>
            <div className="glass-card group relative overflow-hidden p-1">
              <div className="shimmer pointer-events-none absolute inset-0 opacity-0 group-focus-within:opacity-100" />
              <div className="relative space-y-4 rounded-xl p-6 sm:p-8">
                <div className="flex items-center justify-between">
                  <label htmlFor="question" className="text-sm font-medium text-muted-foreground">
                    Your Question
                  </label>
                  <span className={cn(
                    "text-xs tabular-nums text-muted-foreground",
                    question.length > 500 && "text-destructive"
                  )}>
                    {question.length}/1000
                  </span>
                </div>

                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value.slice(0, 1000))}
                  rows={4}
                  maxLength={1000}
                  className="w-full resize-none bg-transparent text-lg placeholder:text-muted-foreground/40 focus:outline-none"
                  placeholder="What ethical framework should guide the development of artificial general intelligence?"
                />

                <div className="flex flex-wrap gap-2">
                  {EXAMPLE_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => setQuestion(prompt)}
                      className="rounded-lg border border-border/50 px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-primary/30 hover:text-primary"
                    >
                      {prompt.length > 40 ? prompt.slice(0, 40) + "..." : prompt}
                    </button>
                  ))}
                </div>

                <div className="flex flex-wrap items-center justify-between gap-4 border-t border-border/50 pt-4">
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-accent"
                    >
                      <Upload className="h-3.5 w-3.5" />
                      Context
                    </button>
                    <button
                      type="button"
                      className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-accent"
                    >
                      <Mic className="h-3.5 w-3.5" />
                      Voice
                    </button>
                    <label className="flex cursor-pointer items-center gap-2 rounded-lg px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-accent">
                      <input
                        type="checkbox"
                        checked={useDryRun}
                        onChange={(e) => setUseDryRun(e.target.checked)}
                        className="sr-only"
                      />
                      <div
                        className={cn(
                          "flex h-4 w-7 rounded-full border transition-colors",
                          useDryRun
                            ? "border-primary bg-primary"
                            : "border-border bg-transparent"
                        )}
                      >
                        <div
                          className={cn(
                            "h-3.5 w-3.5 rounded-full bg-white transition-transform",
                            useDryRun && "translate-x-3"
                          )}
                        />
                      </div>
                      Dry Run
                    </label>
                  </div>

                  <Button
                    type="submit"
                    size="lg"
                    disabled={loading || !question.trim()}
                    className="group relative overflow-hidden"
                  >
                    <AnimatePresence mode="wait">
                      {loading ? (
                        <motion.span
                          key="loading"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          className="flex items-center gap-2"
                        >
                          <Loader2 className="h-4 w-4 animate-spin" />
                          Submitting...
                        </motion.span>
                      ) : (
                        <motion.span
                          key="idle"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          className="flex items-center gap-2"
                        >
                          <Send className="h-4 w-4" />
                          Deliberate
                          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                        </motion.span>
                      )}
                    </AnimatePresence>
                  </Button>
                </div>

                {error && (
                  <motion.p
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-sm text-destructive"
                  >
                    {error}
                  </motion.p>
                )}
              </div>
            </div>
          </form>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-16"
        >
          <div className="mb-8 text-center">
            <h2 className="text-2xl font-semibold">Council of AI Advisors</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Six specialized personas deliberate your question
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {ADVISORS.map((advisor, i) => (
              <motion.div
                key={advisor.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.35 + i * 0.07 }}
                className="glass-card group relative overflow-hidden p-5"
              >
                <div className="flex items-start gap-4">
                  <div
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${advisor.color} shadow-lg`}
                  >
                    <advisor.icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold">{advisor.name}</h3>
                    <p className="text-xs text-muted-foreground">{advisor.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-20"
        >
          <h2 className="mb-8 text-center text-2xl font-semibold">How It Works</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {STEPS.map((s, i) => (
              <motion.div
                key={s.step}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.65 + i * 0.08 }}
                className="glass-card p-6 text-center"
              >
                <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary font-bold text-sm">
                  {s.step}
                </div>
                <h3 className="font-semibold">{s.title}</h3>
                <p className="mt-1 text-xs text-muted-foreground">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-20 text-center"
        >
          <div className="glass-card inline-flex items-center gap-2 px-6 py-3">
            <CheckCircle2 className="h-4 w-4 text-success" />
            <span className="text-sm text-muted-foreground">
              All deliberation is fully transparent and auditable
            </span>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
