# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import re

from pydantic import BaseModel, Field

from core.models import AdvisorPersona


class EvaluationCriterion(BaseModel):
    name: str
    score: float = Field(default=0.0, ge=0, le=10)
    weight: float = Field(default=1.0, ge=0, le=1)
    rationale: str = ""


CRITERIA_DEFINITIONS: dict[AdvisorPersona, list[dict]] = {
    AdvisorPersona.RATIONAL_ANALYST: [
        {
            "name": "data_quality",
            "question": "How strong is the supporting data?",
            "weight": 0.30,
            "keywords": ["data", "statistics", "evidence", "%", "percent", "study", "research", "analysis", "metric", "measured"],
        },
        {
            "name": "logical_coherence",
            "question": "Is the reasoning logically sound?",
            "weight": 0.30,
            "keywords": ["because", "therefore", "if", "then", "implies", "leads to", "causes", "reason"],
        },
        {
            "name": "probability_assessment",
            "question": "Are probabilities and risks quantified?",
            "weight": 0.20,
            "keywords": ["probability", "risk", "chance", "likelihood", "uncertainty", "confidence", "odds", "%"],
        },
        {
            "name": "evidence_basis",
            "question": "Is the argument grounded in empirical evidence?",
            "weight": 0.20,
            "keywords": ["evidence", "study", "research", "data", "findings", "proven", "validated", "empirical"],
        },
    ],
    AdvisorPersona.HUMANITARIAN: [
        {
            "name": "human_dignity",
            "question": "Does this protect human dignity?",
            "weight": 0.30,
            "keywords": ["people", "human", "dignity", "rights", "welfare", "well-being", "care", "community", "fair"],
        },
        {
            "name": "fairness_distribution",
            "question": "Are benefits and burdens distributed fairly?",
            "weight": 0.25,
            "keywords": ["fair", "equal", "inequality", "equity", "distribution", "access", "bias", "discrimination"],
        },
        {
            "name": "vulnerable_populations",
            "question": "Is there disproportionate impact on vulnerable groups?",
            "weight": 0.25,
            "keywords": ["vulnerable", "minority", "poor", "disadvantaged", "marginalized", "children", "elderly", "disabled"],
        },
        {
            "name": "well_being",
            "question": "What is the net effect on human well-being?",
            "weight": 0.20,
            "keywords": ["well-being", "happiness", "health", "quality of life", "welfare", "benefit", "harm"],
        },
    ],
    AdvisorPersona.ECONOMIC: [
        {
            "name": "cost_impact",
            "question": "What is the direct and indirect cost?",
            "weight": 0.25,
            "keywords": ["cost", "expensive", "spend", "budget", "money", "price", "investment", "funding"],
        },
        {
            "name": "revenue_impact",
            "question": "What is the effect on revenue?",
            "weight": 0.25,
            "keywords": ["revenue", "income", "profit", "growth", "sales", "return", "roi", "financial"],
        },
        {
            "name": "resource_allocation",
            "question": "Are resources allocated efficiently?",
            "weight": 0.20,
            "keywords": ["resource", "efficient", "allocate", "optimize", "waste", "utilization", "capacity"],
        },
        {
            "name": "market_effect",
            "question": "How does this affect market position?",
            "weight": 0.15,
            "keywords": ["market", "competitive", "share", "position", "industry", "demand", "supply"],
        },
        {
            "name": "financial_risk",
            "question": "What is the financial risk exposure?",
            "weight": 0.15,
            "keywords": ["risk", "loss", "liability", "exposure", "volatility", "uncertainty", "downside"],
        },
    ],
    AdvisorPersona.LEGAL: [
        {
            "name": "compliance",
            "question": "Does this comply with applicable laws?",
            "weight": 0.30,
            "keywords": ["law", "legal", "compliance", "regulation", "statute", "act", "ordinance", "permit"],
        },
        {
            "name": "liability",
            "question": "What is the liability exposure?",
            "weight": 0.25,
            "keywords": ["liable", "liability", "lawsuit", "sue", "damages", "negligence", "responsibility"],
        },
        {
            "name": "regulatory_risk",
            "question": "What is the regulatory risk profile?",
            "weight": 0.25,
            "keywords": ["regulatory", "regulation", "government", "agency", "compliance", "approval", "license"],
        },
        {
            "name": "contractual_obligations",
            "question": "Are contractual obligations met?",
            "weight": 0.20,
            "keywords": ["contract", "agreement", "obligation", "terms", "clause", "breach", "commitment"],
        },
    ],
    AdvisorPersona.DEVILS_ADVOCATE: [
        {
            "name": "edge_cases",
            "question": "What edge cases could break this decision?",
            "weight": 0.30,
            "keywords": ["worst", "fail", "break", "extreme", "unexpected", "exception", "outlier", "rare"],
        },
        {
            "name": "assumption_challenge",
            "question": "Which assumptions are weakest?",
            "weight": 0.25,
            "keywords": ["assume", "assumption", "uncertain", "unknown", "if", "depends", "maybe", "perhaps"],
        },
        {
            "name": "failure_modes",
            "question": "What are the most likely failure modes?",
            "weight": 0.25,
            "keywords": ["fail", "failure", "risk", "problem", "issue", "downside", "negative", "worst-case"],
        },
        {
            "name": "unintended_consequences",
            "question": "What unintended consequences could arise?",
            "weight": 0.20,
            "keywords": ["consequence", "unintended", "side effect", "second-order", "knock-on", "ripple", "cascade"],
        },
    ],
    AdvisorPersona.LONG_TERM_STRATEGIST: [
        {
            "name": "systemic_impact",
            "question": "What are the second and third-order effects?",
            "weight": 0.30,
            "keywords": ["long-term", "future", "systemic", "widespread", "transform", "shift", "decade"],
        },
        {
            "name": "horizon_viability",
            "question": "Does this remain viable in 5-10 years?",
            "weight": 0.30,
            "keywords": ["sustainable", "viable", "long-term", "future-proof", "durable", "lasting", "permanent"],
        },
        {
            "name": "adaptability",
            "question": "How adaptable is this to changing conditions?",
            "weight": 0.20,
            "keywords": ["adapt", "flexible", "change", "evolve", "pivot", "adjust", "responsive", "agile"],
        },
        {
            "name": "legacy_effect",
            "question": "What structural legacy does this create?",
            "weight": 0.20,
            "keywords": ["legacy", "foundation", "infrastructure", "structural", "framework", "precedent", "long-term"],
        },
    ],
}


PERSONA_STANCE_BIASES: dict[AdvisorPersona, dict[str, float]] = {
    AdvisorPersona.RATIONAL_ANALYST: {"yes": 0.15, "cautious_yes": 0.40, "neutral": 0.30, "cautious_no": 0.10, "no": 0.05},
    AdvisorPersona.HUMANITARIAN: {"yes": 0.25, "cautious_yes": 0.35, "neutral": 0.20, "cautious_no": 0.10, "no": 0.10},
    AdvisorPersona.ECONOMIC: {"yes": 0.30, "cautious_yes": 0.30, "neutral": 0.15, "cautious_no": 0.15, "no": 0.10},
    AdvisorPersona.LEGAL: {"yes": 0.05, "cautious_yes": 0.25, "neutral": 0.25, "cautious_no": 0.30, "no": 0.15},
    AdvisorPersona.DEVILS_ADVOCATE: {"yes": 0.00, "cautious_yes": 0.10, "neutral": 0.15, "cautious_no": 0.35, "no": 0.40},
    AdvisorPersona.LONG_TERM_STRATEGIST: {"yes": 0.10, "cautious_yes": 0.25, "neutral": 0.25, "cautious_no": 0.25, "no": 0.15},
}


POSITIVE_BIAS_KEYWORDS = {
    "opportunity", "benefit", "growth", "improve", "advantage", "profit",
    "gain", "good", "excellent", "promising", "potential", "success",
}

NEGATIVE_BIAS_KEYWORDS = {
    "risk", "loss", "danger", "threat", "problem", "issue", "concern",
    "difficult", "challenge", "costly", "expensive", "harm", "damage",
}


class AdvisorEvaluation(BaseModel):
    persona: AdvisorPersona
    overall_score: float = Field(default=0.0, ge=0, le=10)
    criteria: list[EvaluationCriterion] = Field(default_factory=list)
    argument: str = ""
    concerns: list[str] = Field(default_factory=list)
    stance: str = "neutral"


class AdvisorEvaluator:
    def get_criteria(self, persona: AdvisorPersona) -> list[dict]:
        return CRITERIA_DEFINITIONS.get(persona, [])

    def _score_keyword_match(self, text: str, keywords: list[str]) -> float:
        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw in text_lower)
        if not keywords:
            return 5.0
        ratio = matches / len(keywords)
        return round(min(ratio * 10, 10), 1)

    def _determine_stance(self, question: str, persona: AdvisorPersona, overall_score: float) -> str:
        question_lower = question.lower()
        positive_count = sum(1 for kw in POSITIVE_BIAS_KEYWORDS if kw in question_lower)
        negative_count = sum(1 for kw in NEGATIVE_BIAS_KEYWORDS if kw in question_lower)
        sentiment = positive_count - negative_count

        bias = PERSONA_STANCE_BIASES.get(persona, {})
        raw = overall_score / 10.0 + sentiment * 0.05

        if raw > 0.7:
            return "yes"
        elif raw > 0.5:
            edge = bias.get("cautious_yes", 0.3) * 2
            return "cautious_yes" if edge > 0.6 else "yes"
        elif raw > 0.3:
            return "cautious_no" if negative_count > positive_count else "cautious_yes"
        elif raw > 0.1:
            return "cautious_no"
        else:
            return "no"

    def evaluate(
        self, persona: AdvisorPersona, question: str, context: dict
    ) -> AdvisorEvaluation:
        criteria_defs = self.get_criteria(persona)
        combined_text = f"{question} {' '.join(str(v) for v in context.values())}" if context else question

        criteria = []
        concerns = []

        for c in criteria_defs:
            keywords = c.get("keywords", [])
            score = self._score_keyword_match(combined_text, keywords)
            rationale = f"Analyzed: {c['question']} — matched {score/10:.0%} of criteria signals"
            if score < 3:
                concerns.append(f"Limited signal for {c['name']}: insufficient data to evaluate")
            criteria.append(EvaluationCriterion(
                name=c["name"],
                weight=c["weight"],
                score=score,
                rationale=rationale,
            ))

        total_weight = sum(c.weight for c in criteria)
        overall = (
            sum(c.score * c.weight for c in criteria) / total_weight
            if total_weight > 0
            else 0.0
        )

        stance = self._determine_stance(question, persona, overall)

        argument = self._build_argument(persona, stance, criteria)

        return AdvisorEvaluation(
            persona=persona,
            overall_score=round(overall, 1),
            criteria=criteria,
            argument=argument,
            concerns=concerns,
            stance=stance,
        )

    def _build_argument(self, persona: AdvisorPersona, stance: str, criteria: list[EvaluationCriterion]) -> str:
        top = sorted(criteria, key=lambda c: c.score, reverse=True)
        bottom = sorted(criteria, key=lambda c: c.score)[:2]
        parts = [f"From a {persona.value} perspective, the assessment is **{stance}**."]
        if top:
            strongest = top[0]
            parts.append(f"Strongest signal: {strongest.name} ({strongest.score}/10).")
        for b in bottom:
            if b.score < 5:
                parts.append(f"Weakness: {b.name} ({b.score}/10) — {b.rationale}")
        return " ".join(parts)
