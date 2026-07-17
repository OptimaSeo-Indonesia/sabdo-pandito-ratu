# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(str, Enum):
    PENDING = "pending"
    ANALYZING_CONTEXT = "analyzing_context"
    GENERATING_PERSPECTIVES = "generating_perspectives"
    COLLECTING_ARGUMENTS = "collecting_arguments"
    RESOLVING_CONFLICTS = "resolving_conflicts"
    EVALUATING_PRINCIPLES = "evaluating_principles"
    EXPLORING_SCENARIOS = "exploring_scenarios"
    REFLECTING = "reflecting"
    SCORING = "scoring"
    GENERATING_VERDICT = "generating_verdict"
    COMPLETED = "completed"
    FAILED = "failed"


class ConflictType(str, Enum):
    EXPLICIT_CONFLICT = "explicit_conflict"
    NUANCE_DIFFERENCE = "nuance_difference"
    CONSENSUS = "consensus"
    INCOMPATIBLE_ASSUMPTION = "incompatible_assumption"
    VALUE_TRADEOFF = "value_tradeoff"


# ─── Advisor Persona ────────────────────────────────────────────

class AdvisorPersona(str, Enum):
    RATIONAL_ANALYST = "rational_analyst"
    HUMANITARIAN = "humanitarian"
    ECONOMIC = "economic"
    LEGAL = "legal"
    DEVILS_ADVOCATE = "devils_advocate"
    LONG_TERM_STRATEGIST = "long_term_strategist"


PERSONA_DESCRIPTIONS: dict[AdvisorPersona, str] = {
    AdvisorPersona.RATIONAL_ANALYST: "Focuses on data, probabilities, and empirical evidence",
    AdvisorPersona.HUMANITARIAN: "Focuses on human impact, fairness, and dignity",
    AdvisorPersona.ECONOMIC: "Focuses on cost, efficiency, and financial sustainability",
    AdvisorPersona.LEGAL: "Focuses on compliance, regulation, and legal risk",
    AdvisorPersona.DEVILS_ADVOCATE: "Seeks weaknesses, edge cases, and failure modes",
    AdvisorPersona.LONG_TERM_STRATEGIST: "Focuses on 5-10 year impact and systemic effects",
}

PERSONA_SYSTEM_PROMPTS: dict[AdvisorPersona, str] = {
    AdvisorPersona.RATIONAL_ANALYST: (
        "You are a Rational Analyst. Evaluate the question based on data, "
        "probabilities, empirical evidence, and logical reasoning. "
        "Be skeptical of unsupported claims. Demand evidence."
    ),
    AdvisorPersona.HUMANITARIAN: (
        "You are a Humanitarian Advisor. Evaluate the question based on "
        "human impact, dignity, fairness, and well-being of all affected people. "
        "Speak for those who may not have a voice in this decision."
    ),
    AdvisorPersona.ECONOMIC: (
        "You are an Economic Advisor. Evaluate the question based on "
        "cost efficiency, financial sustainability, resource allocation, "
        "and long-term economic viability."
    ),
    AdvisorPersona.LEGAL: (
        "You are a Legal Advisor. Evaluate the question based on "
        "applicable laws, regulations, compliance requirements, "
        "and legal risks. Identify potential liabilities."
    ),
    AdvisorPersona.DEVILS_ADVOCATE: (
        "You are a Devil's Advocate. Your job is to challenge every assumption, "
        "find weaknesses in every argument, identify edge cases that could fail, "
        "and stress-test the proposed decision. Be ruthlessly critical."
    ),
    AdvisorPersona.LONG_TERM_STRATEGIST: (
        "You are a Long-Term Strategist. Evaluate the question based on "
        "10-year horizon outcomes, systemic effects, second-order consequences, "
        "and alignment with long-range goals."
    ),
}


# ─── Core Models ────────────────────────────────────────────────

class CapabilityRequirement(BaseModel):
    reasoning: int = Field(default=5, ge=0, le=10)
    structured_output: bool = True
    nuanced_language: bool = False
    ethical_reasoning: int = Field(default=0, ge=0, le=10)
    numerical_reasoning: int = Field(default=0, ge=0, le=10)
    long_context: bool = False
    high_reliability: bool = False


class ModelCapability(BaseModel):
    reasoning: int = Field(default=5, ge=0, le=10)
    structured_output: bool = True
    nuanced_language: bool = False
    ethical_reasoning: int = Field(default=0, ge=0, le=10)
    numerical_reasoning: int = Field(default=0, ge=0, le=10)
    long_context: bool = False
    high_reliability: bool = False
    cost_efficiency: int = Field(default=5, ge=0, le=10)


class ModelMetadata(BaseModel):
    id: str
    provider: str
    display_name: str
    context_window: int = 8192
    capability: ModelCapability = Field(default_factory=ModelCapability)
    latency: str = "medium"
    is_local: bool = False
    is_multimodal: bool = False


class ModelSelection(BaseModel):
    persona: AdvisorPersona
    requirements: CapabilityRequirement
    selected_model: str
    selected_provider: str
    selection_reason: str
    fallback_occurred: bool = False
    fallback_from: str | None = None


class LLMCallLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    persona: AdvisorPersona
    provider: str
    model: str
    step: str
    latency_ms: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    success: bool = True
    error_message: str | None = None
    retry_count: int = 0
    fallback_occurred: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdvisorProfile(BaseModel):
    persona: AdvisorPersona
    name: str
    description: str
    system_prompt: str
    active: bool = True
    priority_weights: dict[str, float] = Field(default_factory=dict)
    capability_requirements: CapabilityRequirement = Field(default_factory=CapabilityRequirement)


class Perspective(BaseModel):
    advisor_id: str
    stance: str = "neutral"
    summary: str = ""
    reasoning: str = ""
    confidence: float = Field(default=0.5, ge=0, le=1)
    key_points: list[str] = Field(default_factory=list)


class AdvisorResponse(BaseModel):
    advisor_id: str
    persona: AdvisorPersona
    stance: str
    summary: str
    reasoning: str
    confidence: float = Field(ge=0, le=1)
    key_points: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class Argument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    advisor_id: str
    persona: AdvisorPersona
    claim: str
    evidence: str
    reasoning: str
    supports_stance: str | None = None


class Conflict(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: ConflictType
    description: str
    between_personas: list[AdvisorPersona]
    root_cause: str
    resolution: str | None = None


# ─── Principle Evaluation ───────────────────────────────────────

class PrincipleEvaluation(BaseModel):
    principle: str
    score: float = Field(ge=0, le=10)
    weight: float = Field(ge=0, le=1)
    rationale: str
    concerns: list[str] = Field(default_factory=list)


# ─── Scenario Exploration ───────────────────────────────────────

class ScenarioAssumption(BaseModel):
    description: str
    confidence: float = Field(default=0.5, ge=0, le=1)


class ScenarioExploration(BaseModel):
    scenario_name: str
    time_horizon: str
    probability: float = Field(ge=0, le=1)
    assumptions: list[ScenarioAssumption] = Field(default_factory=list)
    uncertainty_level: str = "medium"
    positive_outcomes: list[str] = Field(default_factory=list)
    negative_outcomes: list[str] = Field(default_factory=list)
    net_impact: float = Field(ge=-10, le=10)


# ─── Wisdom Score ───────────────────────────────────────────────

class WisdomScore(BaseModel):
    evidence_quality: float = Field(ge=0, le=100)
    perspective_diversity: float = Field(ge=0, le=100)
    ethical_alignment: float = Field(ge=0, le=100)
    long_term_impact: float = Field(ge=0, le=100)
    uncertainty_handling: float = Field(ge=0, le=100)
    reversibility: float = Field(ge=0, le=100)

    @property
    def overall(self) -> float:
        weights = {
            "evidence_quality": 0.25,
            "perspective_diversity": 0.15,
            "ethical_alignment": 0.20,
            "long_term_impact": 0.15,
            "uncertainty_handling": 0.15,
            "reversibility": 0.10,
        }
        return round(
            self.evidence_quality * weights["evidence_quality"]
            + self.perspective_diversity * weights["perspective_diversity"]
            + self.ethical_alignment * weights["ethical_alignment"]
            + self.long_term_impact * weights["long_term_impact"]
            + self.uncertainty_handling * weights["uncertainty_handling"]
            + self.reversibility * weights["reversibility"],
            1,
        )


# ─── Context ────────────────────────────────────────────────────

class ContextAnalysis(BaseModel):
    domain: str
    stakes: str
    affected_stakeholders: list[str] = Field(default_factory=list)
    time_sensitivity: str
    key_constraints: list[str] = Field(default_factory=list)
    data_gaps: list[str] = Field(default_factory=list)


# ─── Verdict ────────────────────────────────────────────────────

class Verdict(BaseModel):
    decision: str
    confidence: float = Field(ge=0, le=1)
    wisdom_score: WisdomScore | None = None
    summary: str
    principle_evaluations: list[PrincipleEvaluation] = Field(default_factory=list)
    scenarios: list[ScenarioExploration] = Field(default_factory=list)
    reflection: dict | None = None
    key_factors: list[str] = Field(default_factory=list)
    supporting_arguments: list[dict] = Field(default_factory=list)
    opposing_arguments: list[dict] = Field(default_factory=list)
    conflicts: list[dict] = Field(default_factory=list)
    conflict_resolution: str | None = None
    uncertainty_factors: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    scores: dict[str, float] = Field(default_factory=dict)
    model_selections: list[ModelSelection] = Field(default_factory=list)
    llm_call_logs: list[LLMCallLog] = Field(default_factory=list)


# ─── Deliberation State ─────────────────────────────────────────

class DeliberationState(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    question: str
    context: dict = Field(default_factory=dict)
    status: SessionStatus = SessionStatus.PENDING
    context_analysis: ContextAnalysis | None = None
    advisor_responses: list[AdvisorResponse] = Field(default_factory=list)
    arguments: list[Argument] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    principle_evaluations: list[PrincipleEvaluation] = Field(default_factory=list)
    scenarios: list[ScenarioExploration] = Field(default_factory=list)
    wisdom_score: WisdomScore | None = None
    reflection: dict | None = None
    scores: dict[str, float] = Field(default_factory=dict)
    verdict: Verdict | None = None
    error_message: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    model_selections: list[ModelSelection] = Field(default_factory=list)
    llm_call_logs: list[LLMCallLog] = Field(default_factory=list)


# ─── Collective Wisdom Memory ───────────────────────────────────

class DecisionCase(BaseModel):
    case_id: str = Field(default_factory=lambda: str(uuid4()))
    question: str
    domain: str
    verdict: str
    confidence: float
    wisdom_score: WisdomScore | None = None
    outcome: str | None = None
    outcome_score: float | None = Field(default=None, ge=-10, le=10)
    lessons_learned: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: datetime | None = None
