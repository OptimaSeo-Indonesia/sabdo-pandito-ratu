# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session as SASession, sessionmaker

from core.models import DecisionCase, DeliberationState, Verdict

logger = logging.getLogger(__name__)


def _to_responses(responses: list) -> list:
    from core.models import AdvisorResponse
    return [AdvisorResponse(**r) if isinstance(r, dict) else r for r in responses]


def _to_conflicts(conflicts: list) -> list:
    from core.models import Conflict
    return [Conflict(**c) if isinstance(c, dict) else c for c in conflicts]


class CollectiveWisdomMemory:
    def __init__(self, db_url: str | None = None):
        self._cases: dict[str, DecisionCase] = {}
        self._db_url = db_url
        self._engine = None
        self._session_factory = None
        if db_url:
            try:
                self._engine = create_engine(db_url)
                self._session_factory = sessionmaker(bind=self._engine)
                logger.info("CollectiveWisdomMemory connected to database")
            except Exception as exc:
                logger.warning("Could not connect to database, using in-memory: %s", exc)

    def _db_session(self) -> SASession | None:
        if self._session_factory:
            return self._session_factory()
        return None

    async def save_session(self, state: DeliberationState) -> None:
        from apps.api.db.models import DeliberationSessionModel
        domain = state.context_analysis.domain if state.context_analysis else "general"
        stakes = state.context_analysis.stakes if state.context_analysis else "unknown"
        time_sens = state.context_analysis.time_sensitivity if state.context_analysis else "moderate"
        stakeholders = state.context_analysis.affected_stakeholders if state.context_analysis else []
        data_gaps = state.context_analysis.data_gaps if state.context_analysis else []
        constraints = state.context_analysis.key_constraints if state.context_analysis else []

        case = DecisionCase(
            question=state.question,
            domain=domain,
            verdict=state.verdict.decision if state.verdict else "unknown",
            confidence=state.verdict.confidence if state.verdict else 0.0,
            wisdom_score=state.wisdom_score,
        )
        self._cases[case.case_id] = case

        if self._db_session:
            session = self._db_session()
            try:
                db_model = DeliberationSessionModel(
                    session_id=state.session_id,
                    question=state.question,
                    context=state.context,
                    status=state.status.value,
                    domain=domain,
                    stakes=stakes,
                    time_sensitivity=time_sens,
                    affected_stakeholders=stakeholders,
                    data_gaps=data_gaps,
                    key_constraints=constraints,
                    wisdom_score=state.wisdom_score.model_dump() if state.wisdom_score else None,
                    reflection=state.reflection,
                    scores=state.scores,
                    verdict=state.verdict.model_dump() if state.verdict else None,
                    created_at=state.created_at,
                    completed_at=state.completed_at or datetime.now(timezone.utc),
                )
                session.add(db_model)
                session.commit()
            except Exception as exc:
                logger.error("Failed to save session to DB: %s", exc)
                if session:
                    session.rollback()
            finally:
                if session:
                    session.close()

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
            session = self._db_session()
            if session:
                from apps.api.db.models import DecisionCaseModel
                try:
                    stmt = select(DecisionCaseModel).where(
                        DecisionCaseModel.case_id == case_id
                    )
                    result = session.execute(stmt).scalar_one_or_none()
                    if result:
                        result.outcome = outcome
                        result.outcome_score = outcome_score
                        result.lessons_learned = lessons
                        result.reviewed_at = datetime.now(timezone.utc)
                        session.commit()
                except Exception as exc:
                    logger.error("Failed to update outcome in DB: %s", exc)
                    if session:
                        session.rollback()
                finally:
                    session.close()

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
        session = self._db_session()
        if session:
            from apps.api.db.models import DeliberationSessionModel
            try:
                stmt = select(DeliberationSessionModel)
                if status:
                    stmt = stmt.where(DeliberationSessionModel.status == status)
                stmt = stmt.order_by(DeliberationSessionModel.created_at.desc())
                stmt = stmt.offset(offset).limit(limit)
                rows = session.execute(stmt).scalars().all()
                total = len(rows)
                states = []
                for r in rows:
                    s = DeliberationState(
                        session_id=r.session_id,
                        question=r.question,
                        context=r.context or {},
                        status=r.status,
                    )
                    states.append(s)
                return states, total
            except Exception as exc:
                logger.error("Failed to list sessions from DB: %s", exc)
                if session:
                    session.close()
                return [], 0
            finally:
                if session:
                    session.close()
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
