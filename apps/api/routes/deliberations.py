# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from core.deliberation.graph import DeliberationGraph
from core.explainability.reporter import ExplainabilityReporter
from core.models import DeliberationState

router = APIRouter(tags=["deliberations"])

_sessions: dict[UUID, DeliberationState] = {}


class DeliberationConfig(BaseModel):
    advisors: list[str] | None = None
    debate_rounds: int = Field(default=2, ge=0, le=5)
    judge: str | None = None
    return_full_report: bool = True
    timeout_seconds: int = Field(default=60, ge=10, le=300)


class DeliberateRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    context: dict = Field(default_factory=dict)
    config: DeliberationConfig | None = None


@router.post("/deliberate", status_code=202)
async def start_deliberation(body: DeliberateRequest):
    session_id = uuid4()
    initial_state = DeliberationState(
        session_id=session_id,
        question=body.question,
        context=body.context,
    )
    _sessions[session_id] = initial_state

    return {
        "session_id": str(session_id),
        "status": "pending",
        "status_url": f"/api/v1/deliberate/{session_id}",
        "estimated_completion_seconds": 30,
    }


@router.get("/deliberate/{session_id}")
async def get_deliberation(session_id: UUID):
    state = _sessions.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    result = {
        "session_id": str(session_id),
        "question": state.question,
        "status": state.status.value,
        "advisor_statuses": [
            {
                "persona": r.persona.value,
                "stance": r.stance,
                "confidence": r.confidence,
            }
            for r in state.advisor_responses
        ],
    }

    if state.verdict:
        reporter = ExplainabilityReporter()
        result["verdict"] = {
            "decision": state.verdict.decision,
            "confidence": state.verdict.confidence,
            "summary": state.verdict.summary,
            "wisdom_score": (
                state.verdict.wisdom_score.overall
                if state.verdict.wisdom_score
                else None
            ),
        }
        result["report_url"] = f"/api/v1/deliberate/{session_id}/report"

    return result


@router.get("/deliberate/{session_id}/report")
async def get_deliberation_report(session_id: UUID):
    state = _sessions.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    reporter = ExplainabilityReporter()
    return reporter.generate_report(state)


@router.websocket("/ws/deliberate/{session_id}")
async def deliberation_ws(websocket: WebSocket, session_id: UUID):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
