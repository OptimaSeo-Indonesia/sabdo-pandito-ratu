# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import asyncio
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from core.deliberation.graph import DeliberationGraph, STEP_NAMES
from core.explainability.reporter import ExplainabilityReporter
from core.models import DeliberationState, SessionStatus
from core.memory.store import CollectiveWisdomMemory

router = APIRouter(tags=["deliberations"])

_sessions: dict[UUID, DeliberationState] = {}
_graph: DeliberationGraph | None = None
_memory: CollectiveWisdomMemory | None = None
_ws_clients: dict[UUID, set] = {}


def _get_graph() -> DeliberationGraph:
    global _graph
    if _graph is None:
        _graph = DeliberationGraph()
    return _graph


def _get_memory() -> CollectiveWisdomMemory:
    global _memory
    if _memory is None:
        _memory = CollectiveWisdomMemory()
    return _memory


async def _broadcast(session_id: UUID, event: dict) -> None:
    clients = _ws_clients.get(session_id, set())
    dead = set()
    for ws in clients:
        try:
            await ws.send_json(event)
        except Exception:
            dead.add(ws)
    clients -= dead


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


class DryRunRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    context: dict = Field(default_factory=dict)
    config: DeliberationConfig | None = None


@router.post("/deliberate/dry-run", status_code=200)
async def start_dry_run(body: DryRunRequest):
    now = datetime.now(timezone.utc)
    graph = DeliberationGraph(mode="dry_run")
    initial_steps = [
        {"name": name, "status": "pending", "started_at": None, "completed_at": None}
        for name in STEP_NAMES
    ]
    state = DeliberationState(
        session_id=uuid4(),
        question=body.question,
        context=body.context,
        steps=initial_steps,
        current_step=None,
        steps_completed=0,
        steps_total=9,
        created_at=now,
    )
    result = await graph.run(state)
    if isinstance(result, dict):
        result = DeliberationState(**result)
    reporter = ExplainabilityReporter()
    return {
        "session_id": str(result.session_id),
        "status": result.status.value,
        "verdict": result.verdict.model_dump() if result.verdict else None,
        "wisdom_score": result.wisdom_score.model_dump() if result.wisdom_score else None,
        "report": reporter.generate_report(result),
    }


@router.post("/deliberate", status_code=202)
async def start_deliberation(body: DeliberateRequest):
    session_id = uuid4()
    now = datetime.now(timezone.utc)
    initial_steps = [
        {"name": name, "status": "pending", "started_at": None, "completed_at": None}
        for name in STEP_NAMES
    ]
    initial_state = DeliberationState(
        session_id=session_id,
        question=body.question,
        context=body.context,
        steps=initial_steps,
        current_step=None,
        steps_completed=0,
        steps_total=9,
        created_at=now,
    )
    _sessions[session_id] = initial_state

    graph = _get_graph()
    asyncio.create_task(_run_deliberation(session_id, graph, initial_state))

    return {
        "session_id": str(session_id),
        "status": SessionStatus.PENDING.value,
        "status_url": f"/api/v1/deliberate/{session_id}",
        "estimated_completion_seconds": 30,
    }


async def _run_deliberation(
    session_id: UUID, graph: DeliberationGraph, initial_state: DeliberationState
) -> None:
    try:
        await _broadcast(session_id, {
            "type": "status_update",
            "session_id": str(session_id),
            "status": SessionStatus.PENDING.value,
            "current_step": None,
            "steps_completed": 0,
            "steps_total": 9,
            "event": "deliberation_started",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        result = await graph.run(initial_state)
        if isinstance(result, dict):
            completed = DeliberationState(**result)
        else:
            completed = result
        completed.completed_at = datetime.now(timezone.utc)
        _sessions[session_id] = completed
        memory = _get_memory()
        await memory.save_session(completed)
        await _broadcast(session_id, {
            "type": "completed",
            "session_id": str(session_id),
            "status": SessionStatus.COMPLETED.value,
            "verdict": {
                "decision": completed.verdict.decision if completed.verdict else "unknown",
                "confidence": completed.verdict.confidence if completed.verdict else 0.0,
                "wisdom_score": completed.wisdom_score.overall if completed.wisdom_score else None,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as exc:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("Deliberation %s failed: %s", session_id, exc)
        failed = initial_state
        failed.status = SessionStatus.FAILED
        failed.error_message = str(exc)
        _sessions[session_id] = failed
        await _broadcast(session_id, {
            "type": "error",
            "session_id": str(session_id),
            "status": SessionStatus.FAILED.value,
            "detail": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


@router.get("/deliberate/{session_id}")
async def get_deliberation(session_id: UUID):
    state = _sessions.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    result = {
        "session_id": str(session_id),
        "question": state.question,
        "status": state.status.value,
        "progress": {
            "current_step": state.current_step,
            "steps_completed": state.steps_completed,
            "steps_total": state.steps_total,
            "steps": [
                {
                    "name": s.name if hasattr(s, 'name') else s.get("name"),
                    "status": s.status if hasattr(s, 'status') else s.get("status"),
                }
                for s in state.steps
            ] if state.steps else [],
        },
        "advisor_statuses": [
            {
                "persona": r.persona.value,
                "stance": r.stance,
                "confidence": r.confidence,
            }
            for r in state.advisor_responses
        ],
    }

    if state.error_message:
        result["error"] = state.error_message

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
    if session_id not in _ws_clients:
        _ws_clients[session_id] = set()
    _ws_clients[session_id].add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            state = _sessions.get(session_id)
            if state is None:
                await websocket.send_json({"type": "error", "detail": "Session not found"})
                break
            if state.verdict:
                await websocket.send_json({
                    "type": "verdict",
                    "session_id": str(session_id),
                    "status": SessionStatus.COMPLETED.value,
                    "verdict": {
                        "decision": state.verdict.decision,
                        "confidence": state.verdict.confidence,
                        "wisdom_score": state.verdict.wisdom_score.overall if state.verdict.wisdom_score else None,
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            elif state.error_message:
                await websocket.send_json({
                    "type": "error",
                    "session_id": str(session_id),
                    "detail": state.error_message,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            else:
                await websocket.send_json({
                    "type": "status_update",
                    "session_id": str(session_id),
                    "status": state.status.value,
                    "current_step": state.current_step,
                    "steps_completed": state.steps_completed,
                    "steps_total": state.steps_total,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass
    finally:
        _ws_clients.get(session_id, set()).discard(websocket)
