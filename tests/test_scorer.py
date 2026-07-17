# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2025 OptimaSeo Indonesia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from core.evaluation.scorer import WisdomScorer
from core.models import (
    AdvisorResponse,
    AdvisorPersona,
    DeliberationState,
    PrincipleEvaluation,
    ScenarioAssumption,
    ScenarioExploration,
    WisdomScore,
)


def test_wisdom_scorer_initialization():
    scorer = WisdomScorer()
    assert scorer is not None


def test_compute_returns_wisdom_score():
    scorer = WisdomScorer()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="rational",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Test reasoning",
            confidence=0.85,
        )
    ]
    state.principle_evaluations = [
        PrincipleEvaluation(
            principle="fairness",
            score=8.0,
            weight=0.25,
            rationale="Good",
        ),
        PrincipleEvaluation(
            principle="transparency",
            score=7.0,
            weight=0.20,
            rationale="Good",
        ),
    ]
    state.scenarios = [
        ScenarioExploration(
            scenario_name="optimistic_10_years",
            time_horizon="10 years",
            probability=0.7,
            assumptions=[ScenarioAssumption(description="Market grows", confidence=0.6)],
            net_impact=6.0,
        )
    ]
    result = scorer.compute(state)
    assert isinstance(result, WisdomScore)
    assert 0 <= result.evidence_quality <= 100
    assert 0 <= result.perspective_diversity <= 100
    assert 0 <= result.ethical_alignment <= 100
    assert 0 <= result.overall <= 100


def test_evidence_quality_from_confidence():
    scorer = WisdomScorer()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="a",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="A",
            reasoning="A",
            confidence=0.9,
        )
    ]
    result = scorer.compute(state)
    assert result.evidence_quality > 50


def test_advisor_scores():
    scorer = WisdomScorer()
    responses = [
        AdvisorResponse(
            advisor_id="a",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="A",
            reasoning="A",
            confidence=0.85,
        ),
        AdvisorResponse(
            advisor_id="b",
            persona=AdvisorPersona.HUMANITARIAN,
            stance="no",
            summary="B",
            reasoning="B",
            confidence=0.75,
        ),
    ]
    scores = scorer.compute_advisor_scores(responses)
    assert scores["a"] == 85.0
    assert scores["b"] == 75.0


def test_ethical_alignment_from_principles():
    scorer = WisdomScorer()
    state = DeliberationState(question="Test")
    state.principle_evaluations = [
        PrincipleEvaluation(
            principle="fairness",
            score=9.0,
            weight=0.25,
            rationale="Strong",
        ),
        PrincipleEvaluation(
            principle="transparency",
            score=8.0,
            weight=0.20,
            rationale="Strong",
        ),
    ]
    result = scorer.compute(state)
    assert result.ethical_alignment > 50
