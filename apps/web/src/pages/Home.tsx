import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { startDeliberation, startDryRun } from "../lib/api";
import { cn } from "../lib/utils";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { CouncilChamber } from "../components/council/CouncilChamber";
import {
  Send,
  Upload,
  Mic,
  ArrowRight,
  Sparkles,
  Loader2,
} from "lucide-react";
import type { CouncilPhase } from "../components/council/types";

const EXAMPLE_PROMPTS = [
  "Should universal basic income be implemented globally?",
  "What is the ethical approach to AI regulation?",
  "How should we address climate change?",
  "Should remote work become the standard?",
];

export default function Home() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [useDryRun, setUseDryRun] = useState(false);
  const [councilPhase, setCouncilPhase] = useState<CouncilPhase>("idle");
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      if (councilPhase === "idle") {
        setCouncilPhase("deliberating");
        setTimeout(() => setCouncilPhase("idle"), 3000);
      }
    }, 8000);
    return () => clearInterval(timer);
  }, [councilPhase]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    setCouncilPhase("deliberating");
    try {
      const fn = useDryRun ? startDryRun : startDeliberation;
      const result = await fn(question);
      navigate(`/session/${result.session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
      setCouncilPhase("idle");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative min-h-screen">
      <div className="relative mx-auto max-w-7xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <Badge variant="default" className="mb-4 inline-flex px-4 py-1.5 text-xs font-medium uppercase tracking-wider">
            <Sparkles className="mr-1.5 h-3 w-3" />
            Multi-AI Deliberation Engine
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Sabdo{" "}
            <span className="text-gradient">Pandito</span>{" "}
            Ratu
          </h1>
          <p className="mx-auto mt-5 max-w-xl text-base text-muted-foreground sm:text-[22px] sm:leading-relaxed">
            Multiple AI advisors analyze, debate, reflect, and produce transparent decisions.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.15 }}
          className="mx-auto mt-12 max-w-2xl sm:max-w-3xl lg:max-w-4xl"
        >
          <CouncilChamber phase={councilPhase} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.35 }}
          className="mx-auto mt-12 w-full max-w-[900px]"
        >
          <form onSubmit={handleSubmit}>
            <div className="glass-card group relative overflow-hidden" style={{ padding: 28 }}>
              <div className="shimmer pointer-events-none absolute inset-0 opacity-0 group-focus-within:opacity-100" />
              <div className="relative space-y-5">
                <div className="flex items-center justify-between">
                  <label htmlFor="question" className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Submit a Question
                  </label>
                  <span
                    className={cn(
                      "text-xs tabular-nums text-muted-foreground",
                      question.length > 500 && "text-destructive"
                    )}
                  >
                    {question.length}/1000
                  </span>
                </div>

                <textarea
                  ref={inputRef}
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value.slice(0, 1000))}
                  rows={4}
                  maxLength={1000}
                  className="w-full resize-none bg-transparent text-base placeholder:text-muted-foreground/40 focus:outline-none"
                  placeholder="What ethical framework should guide the development of artificial general intelligence?"
                />

                <div className="flex flex-wrap gap-1.5">
                  {EXAMPLE_PROMPTS.map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => {
                        setQuestion(prompt);
                        inputRef.current?.focus();
                      }}
                      className="rounded-lg border border-white/10 px-2.5 py-1 text-[11px] text-muted-foreground transition-colors hover:border-primary/30 hover:text-primary"
                    >
                      {prompt.length > 35 ? prompt.slice(0, 35) + "..." : prompt}
                    </button>
                  ))}
                </div>

                <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/10 pt-5">
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-white/5"
                    >
                      <Upload className="h-3.5 w-3.5" />
                      Context
                    </button>
                    <button
                      type="button"
                      className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-white/5"
                    >
                      <Mic className="h-3.5 w-3.5" />
                      Voice
                    </button>
                    <label className="flex cursor-pointer items-center gap-2 rounded-lg px-2.5 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-white/5">
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
                            : "border-white/20 bg-transparent"
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
      </div>
    </div>
  );
}
