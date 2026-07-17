# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.models import AdvisorPersona, AdvisorResponse
from core.simulation.simulator import ScenarioExplorer


def test_explorer_initialization():
    sim = ScenarioExplorer()
    assert len(sim.HORIZONS) == 4


def test_explore_returns_scenarios():
    sim = ScenarioExplorer()
    responses = [
        AdvisorResponse(
            advisor_id="economic",
            persona=AdvisorPersona.ECONOMIC,
            stance="yes",
            summary="Cost effective",
            reasoning="Good ROI",
            confidence=0.8,
        ),
        AdvisorResponse(
            advisor_id="humanitarian",
            persona=AdvisorPersona.HUMANITARIAN,
            stance="no",
            summary="High human cost",
            reasoning="Job losses",
            confidence=0.7,
        ),
    ]
    scenarios = sim.explore(
        question="Test", advisor_responses=responses, decision="proceed"
    )
    assert len(scenarios) == 12  # 4 horizons × 3 biases


def test_scenarios_have_probability_range():
    sim = ScenarioExplorer()
    responses = [
        AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Testing",
            confidence=0.9,
        )
    ]
    scenarios = sim.explore(
        question="Test", advisor_responses=responses, decision="proceed"
    )
    for s in scenarios:
        assert 0 <= s.probability <= 1


def test_long_term_horizon_lower_confidence():
    sim = ScenarioExplorer()
    responses = [
        AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Testing",
            confidence=0.9,
        )
    ]
    scenarios = sim.explore(
        question="Test", advisor_responses=responses, decision="proceed"
    )
    short_term = [s for s in scenarios if "6 months" in s.time_horizon]
    long_term = [s for s in scenarios if "10 years" in s.time_horizon]
    if short_term and long_term:
        avg_short = sum(s.probability for s in short_term) / len(short_term)
        avg_long = sum(s.probability for s in long_term) / len(long_term)
        assert avg_short >= avg_long


def test_scenarios_have_assumptions():
    sim = ScenarioExplorer()
    responses = [
        AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Testing",
            confidence=0.9,
        )
    ]
    scenarios = sim.explore(
        question="Test", advisor_responses=responses, decision="proceed"
    )
    for s in scenarios:
        assert len(s.assumptions) > 0
        assert s.uncertainty_level in ("low", "medium", "high")


def test_explorer_uses_scenario_exploration_model():
    from core.models import ScenarioExploration

    sim = ScenarioExplorer()
    responses = [
        AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Testing",
            confidence=0.9,
        )
    ]
    scenarios = sim.explore(
        question="Test", advisor_responses=responses, decision="proceed"
    )
    assert all(isinstance(s, ScenarioExploration) for s in scenarios)
