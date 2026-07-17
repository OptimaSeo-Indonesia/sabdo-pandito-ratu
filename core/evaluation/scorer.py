# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.models import (
    AdvisorResponse,
    Conflict,
    DeliberationState,
    PrincipleEvaluation,
    ScenarioExploration,
    WisdomScore,
)


class WisdomScorer:
    def compute(
        self,
        state: DeliberationState,
    ) -> WisdomScore:
        return WisdomScore(
            evidence_quality=self._score_evidence_quality(state.advisor_responses),
            perspective_diversity=self._score_perspective_diversity(
                state.advisor_responses, state.conflicts
            ),
            ethical_alignment=self._score_ethical_alignment(
                state.principle_evaluations
            ),
            long_term_impact=self._score_long_term_impact(state.scenarios),
            uncertainty_handling=self._score_uncertainty(state),
            reversibility=self._score_reversibility(state.advisor_responses),
        )

    def _score_evidence_quality(
        self, responses: list[AdvisorResponse]
    ) -> float:
        if not responses:
            return 50.0
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        has_data = sum(1 for r in responses if r.data_sources) / len(responses)
        return round((avg_confidence * 60 + has_data * 40), 1)

    def _score_perspective_diversity(
        self, responses: list[AdvisorResponse], conflicts: list[Conflict]
    ) -> float:
        if not responses:
            return 0.0
        unique_personas = set(r.persona for r in responses)
        diversity = min(len(unique_personas) / 6 * 100, 100)
        conflict_bonus = min(len(conflicts) * 5, 20)
        return round(min(diversity + conflict_bonus, 100), 1)

    def _score_ethical_alignment(
        self, evaluations: list[PrincipleEvaluation]
    ) -> float:
        if not evaluations:
            return 50.0
        weighted = sum(e.score * e.weight for e in evaluations)
        max_possible = 10 * sum(e.weight for e in evaluations)
        return round((weighted / max_possible) * 100, 1) if max_possible > 0 else 50.0

    def _score_long_term_impact(self, scenarios: list[ScenarioExploration]) -> float:
        if not scenarios:
            return 50.0
        long_scenarios = [
            s for s in scenarios if "10 years" in s.time_horizon
        ]
        if not long_scenarios:
            return 50.0
        avg_net = sum(s.net_impact for s in long_scenarios) / len(long_scenarios)
        return round(((avg_net + 10) / 20) * 100, 1)

    def _score_uncertainty(self, state: DeliberationState) -> float:
        # Higher score = better handling of uncertainty
        ca = state.context_analysis
        if isinstance(ca, dict):
            data_gaps = ca.get("data_gaps", [])
        else:
            data_gaps = ca.data_gaps if ca else []
        gaps = len(data_gaps)
        uncertainty_mentioned = sum(
            1 for r in state.advisor_responses if "uncertain" in r.reasoning.lower()
        )
        penalty = gaps * 5 + uncertainty_mentioned * 3
        return round(max(100 - penalty, 0), 1)

    def _score_reversibility(
        self, responses: list[AdvisorResponse]
    ) -> float:
        # Higher score = decision is more reversible
        irreversible_signals = sum(
            1
            for r in responses
            if any(
                w in r.reasoning.lower()
                for w in ["irreversible", "permanent", "cannot undo", "point of no return"]
            )
        )
        return round(max(100 - irreversible_signals * 15, 10), 1)

    def compute_advisor_scores(
        self, responses: list[AdvisorResponse]
    ) -> dict[str, float]:
        if not responses:
            return {}
        return {r.advisor_id: round(r.confidence * 100, 1) for r in responses}
