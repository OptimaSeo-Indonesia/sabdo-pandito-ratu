# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2026 OptimaSeo Indonesia
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

from core.explainability.reporter import ExplainabilityReporter
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Conflict,
    ConflictType,
    ContextAnalysis,
    DeliberationState,
    PrincipleEvaluation,
    Verdict,
    WisdomScore,
)


def test_build_verdict():
    state = _make_test_state()
    reporter = ExplainabilityReporter()
    verdict = reporter.build_verdict(state)
    assert verdict.decision
    assert verdict.confidence > 0
    assert verdict.summary
    assert verdict.wisdom_score is not None


def test_generate_report_structure():
    state = _make_test_state()
    reporter = ExplainabilityReporter()
    report = reporter.generate_report(state)
    assert "case" in report
    assert "verdict" in report
    assert "council_composition" in report
    assert "conflicts" in report
    assert "principle_evaluations" in report
    assert "scenario_explorations" in report
    assert "recommendations" in report


def test_generate_summary_contains_decision():
    wisdom = WisdomScore(
        evidence_quality=80,
        perspective_diversity=70,
        ethical_alignment=85,
        long_term_impact=75,
        uncertainty_handling=60,
        reversibility=90,
    )
    verdict = Verdict(
        decision="Proceed with caution",
        confidence=0.78,
        wisdom_score=wisdom,
        summary="Council recommends proceeding",
        recommendations=["Phase 1", "Phase 2"],
        uncertainty_factors=["Market volatility"],
        alternatives=["Alternative A"],
    )
    reporter = ExplainabilityReporter()
    summary = reporter.generate_summary(verdict)
    assert "SABDO PANDITO RATU" in summary
    assert "DECISION:" in summary
    assert "Proceed with caution" in summary
    assert "RECOMMENDATIONS" in summary
    assert "UNCERTAINTIES" in summary


def test_report_determines_decision_correctly():
    state = _make_test_state()
    reporter = ExplainabilityReporter()
    verdict = reporter.build_verdict(state)
    assert verdict.decision in [
        "Proceed with recommended course of action",
        "Proceed with caution — monitor key risk factors",
        "Do not proceed — risks outweigh benefits",
        "Defer decision — requires additional data and analysis",
        "Further analysis required",
        "Insufficient perspectives to reach a decision",
    ]


def _make_test_state() -> DeliberationState:
    state = DeliberationState(question="Should we invest in AI?")
    state.context_analysis = ContextAnalysis(
        domain="technology",
        stakes="high",
        affected_stakeholders=["employees", "customers", "shareholders"],
        time_sensitivity="medium",
        key_constraints=["budget", "talent"],
        data_gaps=["competitor data"],
    )
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="rational",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Strong market opportunity",
            reasoning="AI market growing at 35% CAGR",
            confidence=0.85,
        ),
        AdvisorResponse(
            advisor_id="humanitarian",
            persona=AdvisorPersona.HUMANITARIAN,
            stance="cautious_yes",
            summary="Must ensure ethical deployment",
            reasoning="Job displacement risk needs mitigation",
            confidence=0.72,
        ),
        AdvisorResponse(
            advisor_id="economic",
            persona=AdvisorPersona.ECONOMIC,
            stance="yes",
            summary="Positive ROI within 3 years",
            reasoning="Cost savings justify investment",
            confidence=0.78,
        ),
        AdvisorResponse(
            advisor_id="legal",
            persona=AdvisorPersona.LEGAL,
            stance="cautious_yes",
            summary="Regulatory compliance achievable",
            reasoning="EU AI Act requirements can be met",
            confidence=0.70,
        ),
        AdvisorResponse(
            advisor_id="devils_advocate",
            persona=AdvisorPersona.DEVILS_ADVOCATE,
            stance="no",
            summary="Overhyped market, high failure rate",
            reasoning="70% of AI projects fail to deliver",
            confidence=0.65,
        ),
        AdvisorResponse(
            advisor_id="strategist",
            persona=AdvisorPersona.LONG_TERM_STRATEGIST,
            stance="yes",
            summary="Essential for long-term competitiveness",
            reasoning="10-year horizon requires AI capability",
            confidence=0.88,
        ),
    ]
    state.conflicts = [
        Conflict(
            type=ConflictType.VALUE_TRADEOFF,
            description="Optimism vs skepticism",
            between_personas=[
                AdvisorPersona.LONG_TERM_STRATEGIST,
                AdvisorPersona.DEVILS_ADVOCATE,
            ],
            root_cause="Different risk tolerance and time horizons",
        )
    ]
    state.principle_evaluations = [
        PrincipleEvaluation(
            principle="fairness",
            score=7.5,
            weight=0.25,
            rationale="Moderate alignment",
        ),
        PrincipleEvaluation(
            principle="transparency",
            score=8.0,
            weight=0.20,
            rationale="Strong alignment",
        ),
        PrincipleEvaluation(
            principle="sustainability",
            score=7.0,
            weight=0.20,
            rationale="Moderate alignment",
        ),
        PrincipleEvaluation(
            principle="human_impact",
            score=6.5,
            weight=0.25,
            rationale="Needs attention",
            concerns=["Job displacement risk"],
        ),
        PrincipleEvaluation(
            principle="accountability",
            score=8.0,
            weight=0.10,
            rationale="Strong alignment",
        ),
    ]
    state.wisdom_score = WisdomScore(
        evidence_quality=82,
        perspective_diversity=78,
        ethical_alignment=73,
        long_term_impact=80,
        uncertainty_handling=65,
        reversibility=70,
    )
    return state
