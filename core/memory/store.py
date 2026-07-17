# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from datetime import datetime, timezone
from uuid import UUID

from core.models import DecisionCase, DeliberationState, Verdict


class CollectiveWisdomMemory:
    def __init__(self):
        self._cases: dict[str, DecisionCase] = {}

    async def save_session(self, state: DeliberationState) -> None:
        case = DecisionCase(
            question=state.question,
            domain=(
                state.context_analysis.domain if state.context_analysis else "general"
            ),
            verdict=state.verdict.decision if state.verdict else "unknown",
            confidence=state.verdict.confidence if state.verdict else 0.0,
            wisdom_score=state.wisdom_score,
        )
        self._cases[case.case_id] = case

    async def get_session(self, session_id: UUID) -> DeliberationState | None:
        return None

    async def save_verdict(self, session_id: UUID, verdict: Verdict) -> None:
        pass

    async def record_outcome(
        self,
        case_id: str,
        outcome: str,
        outcome_score: float,
        lessons: list[str],
    ) -> None:
        if case_id in self._cases:
            case = self._cases[case_id]
            case.outcome = outcome
            case.outcome_score = outcome_score
            case.lessons_learned = lessons
            case.reviewed_at = datetime.now(timezone.utc)

    async def find_similar_cases(
        self, question: str, domain: str | None = None, top_k: int = 5
    ) -> list[DecisionCase]:
        results = []
        for case in self._cases.values():
            words_q = set(question.lower().split())
            words_c = set(case.question.lower().split())
            overlap = len(words_q & words_c)
            if overlap > 2:
                results.append(case)
            elif domain and case.domain == domain:
                results.append(case)
        results.sort(key=lambda c: c.created_at, reverse=True)
        return results[:top_k]

    async def get_advisor_insights(self) -> list[dict]:
        return []

    async def list_sessions(
        self,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[DeliberationState], int]:
        return [], 0

    async def get_stats(self) -> dict:
        total = len(self._cases)
        with_outcome = sum(1 for c in self._cases.values() if c.outcome is not None)
        avg_confidence = (
            sum(c.confidence for c in self._cases.values()) / total
            if total > 0
            else 0
        )
        avg_outcome = (
            sum(
                c.outcome_score or 0
                for c in self._cases.values()
                if c.outcome_score is not None
            )
            / with_outcome
            if with_outcome > 0
            else 0
        )

        return {
            "total_cases": total,
            "cases_with_outcomes": with_outcome,
            "avg_confidence": round(avg_confidence, 2),
            "avg_outcome_score": round(avg_outcome, 2),
            "domains": list(
                set(c.domain for c in self._cases.values())
            ),
        }
