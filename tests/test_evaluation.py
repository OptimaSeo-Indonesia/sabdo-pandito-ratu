# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.advisors.evaluation import AdvisorEvaluator, CRITERIA_DEFINITIONS
from core.models import AdvisorPersona


def test_evaluator_has_all_personas():
    assert len(CRITERIA_DEFINITIONS) == 6


def test_evaluator_get_criteria():
    evaluator = AdvisorEvaluator()
    criteria = evaluator.get_criteria(AdvisorPersona.RATIONAL_ANALYST)
    assert len(criteria) == 4


def test_evaluator_economic_has_five_criteria():
    evaluator = AdvisorEvaluator()
    criteria = evaluator.get_criteria(AdvisorPersona.ECONOMIC)
    assert len(criteria) == 5


def test_evaluator_returns_evaluation():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.HUMANITARIAN,
        question="Test question",
        context={},
    )
    assert result.persona == AdvisorPersona.HUMANITARIAN
    assert len(result.criteria) == 4
    assert result.argument


def test_evaluation_has_concerns():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.DEVILS_ADVOCATE,
        question="Test",
        context={},
    )
    assert isinstance(result.concerns, list)


def test_evaluation_score_range():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        question="Test",
        context={},
    )
    assert 0 <= result.overall_score <= 10
