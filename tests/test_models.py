# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.models import (
    AdvisorPersona,
    AdvisorProfile,
    Conflict,
    ConflictType,
    DeliberationState,
    SessionStatus,
    Verdict,
    WisdomScore,
)


def test_advisor_persona_enum():
    assert len(AdvisorPersona) == 6


def test_advisor_profile_creation():
    profile = AdvisorProfile(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        name="Rational Analyst",
        description="Data-driven analysis",
        system_prompt="You are a rational analyst",
    )
    assert profile.persona == AdvisorPersona.RATIONAL_ANALYST
    assert profile.active is True
    assert profile.capability_requirements is not None


def test_deliberation_state_defaults():
    state = DeliberationState(question="Test question")
    assert state.status == SessionStatus.PENDING
    assert state.advisor_responses == []
    assert state.arguments == []
    assert state.verdict is None


def test_verdict_structure():
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
        summary="Test summary",
        recommendations=["Recommendation 1"],
    )
    assert verdict.decision == "Proceed with caution"
    assert verdict.confidence == 0.78
    assert verdict.wisdom_score.overall == 76.8


def test_conflict_creation():
    conflict = Conflict(
        type=ConflictType.VALUE_TRADEOFF,
        description="Economic vs Human values",
        between_personas=[
            AdvisorPersona.ECONOMIC,
            AdvisorPersona.HUMANITARIAN,
        ],
        root_cause="Different value priorities",
    )
    assert conflict.type == ConflictType.VALUE_TRADEOFF
    assert len(conflict.between_personas) == 2


def test_wisdom_score_computation():
    score = WisdomScore(
        evidence_quality=90,
        perspective_diversity=80,
        ethical_alignment=70,
        long_term_impact=60,
        uncertainty_handling=50,
        reversibility=40,
    )
    assert score.overall == 69.0
    assert 0 <= score.overall <= 100
