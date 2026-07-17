# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.models import Conflict, ConflictType, PrincipleEvaluation
from core.principles.engine import PrincipleEngine

from core.models import AdvisorPersona, AdvisorResponse


def test_principle_engine_initialization():
    engine = PrincipleEngine()
    assert len(engine.principles) == 5
    assert "fairness" in engine.principles
    assert "transparency" in engine.principles
    assert "sustainability" in engine.principles
    assert "human_impact" in engine.principles
    assert "accountability" in engine.principles


def test_evaluate_returns_all_principles():
    engine = PrincipleEngine()
    results = engine.evaluate(
        question="Test question",
        context={},
        advisor_responses=[],
        conflicts=[],
    )
    assert len(results) == 5
    assert all(isinstance(r, PrincipleEvaluation) for r in results)


def test_evaluate_scores_in_range():
    engine = PrincipleEngine()
    results = engine.evaluate(
        question="Test",
        context={},
        advisor_responses=[],
        conflicts=[],
    )
    for r in results:
        assert 0 <= r.score <= 10
        assert 0 <= r.weight <= 1


def test_fairness_detects_conflicts():
    engine = PrincipleEngine()
    conflict = Conflict(
        type=ConflictType.VALUE_TRADEOFF,
        description="Test conflict",
        between_personas=[
            AdvisorPersona.ECONOMIC,
            AdvisorPersona.HUMANITARIAN,
        ],
        root_cause="Value tradeoff",
    )
    results = engine.evaluate(
        question="Test",
        context={},
        advisor_responses=[],
        conflicts=[conflict],
    )
    fairness = [r for r in results if r.principle == "fairness"][0]
    assert len(fairness.concerns) > 0


def test_human_impact_uses_advisor_responses():
    engine = PrincipleEngine()
    responses = [
        AdvisorResponse(
            advisor_id="humanitarian",
            persona=AdvisorPersona.HUMANITARIAN,
            stance="no",
            summary="High human cost",
            reasoning="This decision negatively impacts workers",
            confidence=0.3,
        )
    ]
    results = engine.evaluate(
        question="Test",
        context={},
        advisor_responses=responses,
        conflicts=[],
    )
    human = [r for r in results if r.principle == "human_impact"][0]
    assert len(human.concerns) > 0
