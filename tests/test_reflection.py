from core.deliberation.reflection import ReflectionNode, ReflectionResult
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Conflict,
    ConflictType,
    ContextAnalysis,
    DeliberationState,
    PrincipleEvaluation,
)


def test_reflection_initialization():
    node = ReflectionNode()
    assert len(node.ALL_PERSONAS) == 6


def test_reflection_detects_missing_perspectives():
    node = ReflectionNode()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="rational",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Test",
            confidence=0.8,
        )
    ]
    result = node.reflect(state)
    assert len(result["reflection"]["missing_perspectives"]) >= 5


def test_reflection_with_full_council():
    node = ReflectionNode()
    state = DeliberationState(question="Test")
    for p in AdvisorPersona:
        state.advisor_responses.append(
            AdvisorResponse(
                advisor_id=p.value,
                persona=p,
                stance="yes",
                summary=f"{p.value} analysis",
                reasoning="Test",
                confidence=0.8,
            )
        )
    result = node.reflect(state)
    assert len(result["reflection"]["missing_perspectives"]) == 0


def test_reflection_notes_consistency():
    node = ReflectionNode()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="a",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="A",
            reasoning="A",
            confidence=0.8,
        ),
        AdvisorResponse(
            advisor_id="b",
            persona=AdvisorPersona.HUMANITARIAN,
            stance="no",
            summary="B",
            reasoning="B",
            confidence=0.7,
        ),
    ]
    result = node.reflect(state)
    notes = result["reflection"]["reflection_notes"]
    has_disagreement_note = any(
        "Healthy disagreement" in n for n in notes
    )
    assert has_disagreement_note


def test_reflection_low_principles_flag():
    node = ReflectionNode()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="a",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="A",
            reasoning="A",
            confidence=0.8,
        )
    ]
    state.principle_evaluations = [
        PrincipleEvaluation(
            principle="fairness",
            score=4.0,
            weight=0.25,
            rationale="Low score",
            concerns=["Issue"],
        )
    ]
    result = node.reflect(state)
    issues = result["reflection"]["consistency_issues"]
    assert len(issues) >= 1
    assert "Principle" in issues[0]


def test_reflection_adjusts_confidence():
    node = ReflectionNode()
    state = DeliberationState(question="Test")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="a",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="A",
            reasoning="A",
            confidence=0.8,
        )
    ]
    state.context_analysis = ContextAnalysis(
        domain="tech",
        stakes="high",
        affected_stakeholders=["all"],
        time_sensitivity="high",
        data_gaps=["Missing market data", "Unclear regulation"],
    )
    result = node.reflect(state)
    assert result["adjusted_confidence"] <= 0.8
