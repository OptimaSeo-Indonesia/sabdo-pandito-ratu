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
        },
        {
            "name": "logical_coherence",
            "question": "Is the reasoning logically sound?",
            "weight": 0.30,
        },
        {
            "name": "probability_assessment",
            "question": "Are probabilities and risks quantified?",
            "weight": 0.20,
        },
        {
            "name": "evidence_basis",
            "question": "Is the argument grounded in empirical evidence?",
            "weight": 0.20,
        },
    ],
    AdvisorPersona.HUMANITARIAN: [
        {
            "name": "human_dignity",
            "question": "Does this protect human dignity?",
            "weight": 0.30,
        },
        {
            "name": "fairness_distribution",
            "question": "Are benefits and burdens distributed fairly?",
            "weight": 0.25,
        },
        {
            "name": "vulnerable_populations",
            "question": "Is there disproportionate impact on vulnerable groups?",
            "weight": 0.25,
        },
        {
            "name": "well_being",
            "question": "What is the net effect on human well-being?",
            "weight": 0.20,
        },
    ],
    AdvisorPersona.ECONOMIC: [
        {
            "name": "cost_impact",
            "question": "What is the direct and indirect cost?",
            "weight": 0.25,
        },
        {
            "name": "revenue_impact",
            "question": "What is the effect on revenue?",
            "weight": 0.25,
        },
        {
            "name": "resource_allocation",
            "question": "Are resources allocated efficiently?",
            "weight": 0.20,
        },
        {
            "name": "market_effect",
            "question": "How does this affect market position?",
            "weight": 0.15,
        },
        {
            "name": "financial_risk",
            "question": "What is the financial risk exposure?",
            "weight": 0.15,
        },
    ],
    AdvisorPersona.LEGAL: [
        {
            "name": "compliance",
            "question": "Does this comply with applicable laws?",
            "weight": 0.30,
        },
        {
            "name": "liability",
            "question": "What is the liability exposure?",
            "weight": 0.25,
        },
        {
            "name": "regulatory_risk",
            "question": "What is the regulatory risk profile?",
            "weight": 0.25,
        },
        {
            "name": "contractual_obligations",
            "question": "Are contractual obligations met?",
            "weight": 0.20,
        },
    ],
    AdvisorPersona.DEVILS_ADVOCATE: [
        {
            "name": "edge_cases",
            "question": "What edge cases could break this decision?",
            "weight": 0.30,
        },
        {
            "name": "assumption_challenge",
            "question": "Which assumptions are weakest?",
            "weight": 0.25,
        },
        {
            "name": "failure_modes",
            "question": "What are the most likely failure modes?",
            "weight": 0.25,
        },
        {
            "name": "unintended_consequences",
            "question": "What unintended consequences could arise?",
            "weight": 0.20,
        },
    ],
    AdvisorPersona.LONG_TERM_STRATEGIST: [
        {
            "name": "systemic_impact",
            "question": "What are the second and third-order effects?",
            "weight": 0.30,
        },
        {
            "name": "horizon_viability",
            "question": "Does this remain viable in 5-10 years?",
            "weight": 0.30,
        },
        {
            "name": "adaptability",
            "question": "How adaptable is this to changing conditions?",
            "weight": 0.20,
        },
        {
            "name": "legacy_effect",
            "question": "What structural legacy does this create?",
            "weight": 0.20,
        },
    ],
}


class AdvisorEvaluation(BaseModel):
    persona: AdvisorPersona
    overall_score: float = Field(default=0.0, ge=0, le=10)
    criteria: list[EvaluationCriterion] = Field(default_factory=list)
    argument: str = ""
    concerns: list[str] = Field(default_factory=list)


class AdvisorEvaluator:
    def get_criteria(self, persona: AdvisorPersona) -> list[dict]:
        return CRITERIA_DEFINITIONS.get(persona, [])

    def evaluate(
        self, persona: AdvisorPersona, question: str, context: dict
    ) -> AdvisorEvaluation:
        criteria_defs = self.get_criteria(persona)
        criteria = [
            EvaluationCriterion(
                name=c["name"],
                weight=c["weight"],
                rationale=f"Evaluated: {c['question']}",
            )
            for c in criteria_defs
        ]

        overall = (
            sum(c.score * c.weight for c in criteria) / sum(c.weight for c in criteria)
            if criteria
            else 0.0
        )

        return AdvisorEvaluation(
            persona=persona,
            overall_score=round(overall, 1),
            criteria=criteria,
            argument=f"Analysis from {persona.value} perspective",
            concerns=[],
        )
