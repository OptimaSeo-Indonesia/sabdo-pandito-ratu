import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { startDeliberation, startDryRun } from "../lib/api";
import { cn } from "../lib/utils";
import { CouncilChamber } from "../components/council/CouncilChamber";
import { DeliberationTimeline } from "../components/deliberation/DeliberationTimeline";
import {
  Send,
  Upload,
  Mic,
  Sparkles,
  LayoutGrid,
  List,
  Loader2,
  Lightbulb,
} from "lucide-react";

const EXAMPLE_PROMPTS = [
  "Should universal basic income be implemented globally?",
  "What is the ethical approach to AI regulation?",
  "How should we address climate change?",
  "Should remote work become the standard?",
];

const ADVISOR_STATUSES = [
  { id: "sage", name: "Sage", desc: "Evaluating principles...", pct: 78, iconColor: "text-primary", barGradient: "bg-grad-sage", bgClass: "bg-primary/10 border-primary/30" },
  { id: "strategist", name: "Strategist", desc: "Mapping implications...", pct: 62, iconColor: "text-[#4A9EFF]", barGradient: "bg-grad-strategist", bgClass: "bg-[#3D6BFF]/10 border-[#4A9EFF]/30" },
  { id: "guardian", name: "Guardian", desc: "Scanning risks...", pct: 91, iconColor: "text-accent", barGradient: "bg-grad-guardian", bgClass: "bg-accent/10 border-accent/30" },
  { id: "analyst", name: "Analyst", desc: "Analyzing evidence...", pct: 85, iconColor: "text-[#00C896]", barGradient: "bg-grad-analyst", bgClass: "bg-[#00C896]/10 border-[#00C896]/30" },
  { id: "visionary", name: "Visionary", desc: "Exploring alternatives...", pct: 70, iconColor: "text-[#4A9EFF]", barGradient: "bg-grad-visionary", bgClass: "bg-[#3D6BFF]/10 border-[#4A9EFF]/30" },
  { id: "ethicist", name: "Ethicist", desc: "Checking fairness...", pct: 66, iconColor: "text-[#FF58B8]", barGradient: "bg-grad-ethicist", bgClass: "bg-[#FF4FA3]/10 border-[#FF58B8]/30" },
];

const DELIBERATION_STEPS = [
  { name: "question_received", label: "Question Received", status: "completed" as const },
  { name: "context_analysis", label: "Context Analysis", status: "completed" as const },
  { name: "perspective_generation", label: "Perspective Generation", status: "in_progress" as const },
  { name: "conflict_detection", label: "Conflict Detection", status: "pending" as const },
  { name: "ethical_review", label: "Ethical Review", status: "pending" as const },
  { name: "reflection", label: "Reflection", status: "pending" as const },
  { name: "consensus_building", label: "Consensus Building", status: "pending" as const },
  { name: "final_verdict", label: "Final Verdict", status: "pending" as const },
];

export default function Home() {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [useDryRun, setUseDryRun] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);

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
    <>
      {/* Header Row */}
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-5xl font-bold leading-[1.05] tracking-tight">
            Sabdo{" "}
            <span className="text-gradient-brand">Pandito Ratu</span>
          </h1>
          <p className="text-accent font-semibold text-xl">
            Multi-AI Deliberation Engine
          </p>
          <p className="text-muted text-sm leading-6 max-w-[320px]">
            Multiple AI advisors analyze, debate, reflect, and produce transparent decisions.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center rounded-[10px] bg-button-secondary p-1 gap-0">
            <button className="flex items-center justify-center h-8 w-8 rounded-md bg-background text-foreground">
              <LayoutGrid className="h-4 w-4" />
            </button>
            <button className="flex items-center justify-center h-8 w-8 rounded-md text-muted hover:text-foreground">
              <List className="h-4 w-4" />
            </button>
          </div>
          <div className="flex items-center gap-2 bg-button-secondary rounded-[10px] px-3 py-1.5">
            <div className="h-6 w-6 rounded-full bg-grad-primary-btn flex items-center justify-center text-[10px] font-bold text-white">
              PU
            </div>
            <div>
              <p className="text-xs font-medium text-foreground leading-tight">Pandita Utama</p>
              <p className="text-[10px] text-muted leading-tight">Admin</p>
            </div>
            <span className="ml-1 text-[9px] font-bold uppercase text-white bg-grad-primary-btn rounded-md px-1.5 py-0.5 leading-normal">
              Pro
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="flex flex-1 gap-6 overflow-hidden" style={{ minHeight: 0 }}>
        {/* Left Column */}
        <div className="flex flex-1 flex-col gap-6 overflow-auto">
          {/* Council Diagram */}
          <CouncilChamber />

          {/* Question Input */}
          <section className="w-full rounded-2xl p-4 card-ref" style={{ backgroundColor: "#070D22" }}>
            <h2 className="text-base font-semibold text-foreground mb-4">
              Submit a Question to the Council
            </h2>
            <form onSubmit={handleSubmit}>
              <div
                className="rounded-[10px] mb-3"
                style={{
                  backgroundColor: "#050A1B",
                  border: "1px solid rgba(108, 99, 255, 0.16)",
                  position: "relative",
                }}
              >
                <textarea
                  ref={inputRef}
                  value={question}
                  onChange={(e) => setQuestion(e.target.value.slice(0, 2000))}
                  rows={4}
                  maxLength={2000}
                  className="w-full bg-transparent rounded-[10px] px-4 py-3 text-sm text-foreground placeholder:text-muted outline-none resize-none"
                  placeholder="Ask anything. The council will deliberate with wisdom and transparency..."
                  style={{ minHeight: "100px" }}
                />
                <span className="absolute bottom-2 right-3 text-[11px] text-muted">
                  {question.length} / 2000
                </span>
              </div>

              <div className="flex items-center justify-between gap-2 flex-wrap">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    className="flex items-center gap-1.5 rounded-[10px] px-3 py-2 text-xs text-muted"
                    style={{ backgroundColor: "#111633", border: "1px solid rgba(255,255,255,0.08)" }}
                  >
                    <Upload className="h-3.5 w-3.5" />
                    Upload Context
                  </button>
                  <button
                    type="button"
                    className="flex items-center gap-1.5 rounded-[10px] px-3 py-2 text-xs text-muted"
                    style={{ backgroundColor: "#111633", border: "1px solid rgba(255,255,255,0.08)" }}
                  >
                    <Mic className="h-3.5 w-3.5" />
                    Voice Input
                  </button>
                  <button
                    type="button"
                    className="flex items-center gap-1.5 rounded-[10px] px-3 py-2 text-xs text-muted"
                    style={{ backgroundColor: "#111633", border: "1px solid rgba(255,255,255,0.08)" }}
                  >
                    <Lightbulb className="h-3.5 w-3.5" />
                    Suggested Prompts
                  </button>
                </div>

                <div className="flex items-center gap-3">
                  <label className="flex cursor-pointer items-center gap-2 text-xs text-muted">
                    <input
                      type="checkbox"
                      checked={useDryRun}
                      onChange={(e) => setUseDryRun(e.target.checked)}
                      className="sr-only"
                    />
                    <div
                      className="flex h-5 w-9 rounded-full items-center px-0.5 transition-colors"
                      style={{ backgroundColor: useDryRun ? "#6C63FF" : "#1A1F36" }}
                    >
                      <div
                        className={cn(
                          "h-4 w-4 rounded-full bg-white transition-transform",
                          useDryRun && "translate-x-4"
                        )}
                      />
                    </div>
                    Dry Run (No LLM Calls)
                  </label>
                  <button
                    type="submit"
                    disabled={loading || !question.trim()}
                    className="flex items-center gap-2 rounded-[10px] px-5 py-2.5 text-sm font-semibold text-white disabled:opacity-50 disabled:pointer-events-none"
                    style={{
                      background: "linear-gradient(90deg, #A44BFF 0%, #6C63FF 100%)",
                      boxShadow: "0 8px 24px rgba(108, 99, 255, 0.35)",
                      minWidth: "140px",
                    }}
                  >
                    {loading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                    {loading ? "Submitting..." : "Deliberate"}
                  </button>
                </div>
              </div>

              {error && (
                <p className="mt-2 text-xs text-danger">{error}</p>
              )}
            </form>
          </section>
        </div>

        {/* Right Column - 380px */}
        <div className="flex w-[380px] shrink-0 flex-col gap-6 overflow-auto">
          {/* Deliberation Progress */}
          <section className="bg-card card-ref rounded-2xl p-4 flex flex-col gap-0">
            <div className="flex items-center justify-between mb-3">
              <span className="text-base font-semibold text-foreground">
                Deliberation Progress
              </span>
              <span className="flex items-center gap-1 text-[11px] font-medium text-success">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success opacity-75" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-success" />
                </span>
                Live
              </span>
            </div>

            <DeliberationTimeline steps={DELIBERATION_STEPS} />
          </section>

          {/* Council Status */}
          <section className="bg-card card-ref rounded-[18px] p-4">
            <h2 className="text-base font-semibold text-foreground mb-4">
              Council Status
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {ADVISOR_STATUSES.map((a) => {
                const Icon = a.id === "sage" ? Sparkles : a.id === "strategist" ? Lightbulb : a.id === "guardian" ? Upload : a.id === "analyst" ? Send : a.id === "visionary" ? Sparkles : Upload;
                return (
                  <div key={a.id} className="flex items-start gap-2">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border ${a.bgClass}`}>
                      <Icon className={`h-4 w-4 ${a.iconColor}`} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-semibold text-foreground leading-tight">{a.name}</p>
                      <p className="text-[10px] text-muted leading-tight truncate">{a.desc}</p>
                      <div className="mt-1 flex items-center gap-1.5">
                        <div className="flex-1 h-[3px] rounded-full bg-progress-track overflow-hidden">
                          <div className={`h-full rounded-full ${a.barGradient}`} style={{ width: `${a.pct}%` }} />
                        </div>
                        <span className="text-[10px] text-muted font-medium shrink-0">{a.pct}%</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      </div>
    </>
  );
}
