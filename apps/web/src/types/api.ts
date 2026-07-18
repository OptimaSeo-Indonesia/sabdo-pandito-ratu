export interface StepInfo {
  name: string;
  status: string;
}

export interface AdvisorStatus {
  persona: string;
  stance: string;
  confidence: number;
}

export interface Progress {
  current_step: string | null;
  steps_completed: number;
  steps_total: number;
  steps: StepInfo[];
}

export interface Verdict {
  decision: string;
  confidence: number;
  summary: string;
  wisdom_score: number | null;
}

export interface DeliberationStatus {
  session_id: string;
  question: string;
  status: string;
  progress: Progress;
  advisor_statuses: AdvisorStatus[];
  verdict?: Verdict;
  report_url?: string;
  error?: string;
}

export interface WisdomScore {
  evidence_quality: number;
  perspective_diversity: number;
  ethical_alignment: number;
  long_term_impact: number;
  uncertainty_handling: number;
  reversibility: number;
  overall: number;
}

export interface PrincipleEvaluation {
  principle: string;
  score: number;
  weight: number;
  rationale: string;
  concerns: string[];
}

export interface ScenarioAssumption {
  description: string;
  confidence: number;
}

export interface ScenarioExploration {
  name: string;
  horizon: string;
  probability: number;
  assumptions: ScenarioAssumption[];
  uncertainty_level: string;
  net_impact: number;
}

export interface Conflict {
  type: string;
  description: string;
  between: string[];
  root_cause: string;
}

export interface Reflection {
  coverage: string;
  consistency: string;
  principle_alignment: string;
  uncertainty: string;
  adjusted_confidence: number;
}

export interface ReportCase {
  session_id: string;
  question: string;
  domain: string;
}

export interface ReportVerdict {
  decision: string;
  confidence: number;
  wisdom_score: WisdomScore | null;
  overall_score: number | null;
}

export interface ReportReasoning {
  key_factors: string[];
  supporting: unknown[];
  opposing: unknown[];
  conflict_resolution: string | null;
}

export interface FullReport {
  case: ReportCase;
  verdict: ReportVerdict;
  council_composition: AdvisorStatus[];
  conflicts: Conflict[];
  principle_evaluations: PrincipleEvaluation[];
  scenario_explorations: ScenarioExploration[];
  reflection: Reflection | null;
  reasoning: ReportReasoning;
  uncertainties: string[];
  alternatives: string[];
  recommendations: string[];
  model_selections?: unknown[];
  llm_call_logs?: unknown[];
}

export interface StartResponse {
  session_id: string;
  status: string;
  status_url: string;
  estimated_completion_seconds: number;
}

export interface DryRunResponse {
  session_id: string;
  status: string;
  verdict: Verdict | null;
  wisdom_score: WisdomScore | null;
  report: FullReport;
}

export interface AdvisorProfile {
  persona: string;
  name: string;
  description: string;
  active: boolean;
}

export interface SessionListItem {
  session_id: string;
  question: string;
  status: string;
}

export interface SessionStats {
  total_cases: number;
  cases_with_outcomes: number;
  avg_confidence: number;
  avg_outcome_score: number;
  domains: string[];
}
