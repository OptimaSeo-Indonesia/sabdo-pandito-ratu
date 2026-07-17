# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from core.memory.store import CollectiveWisdomMemory

router = APIRouter(tags=["sessions"])

_memory: CollectiveWisdomMemory | None = None


def _get_memory() -> CollectiveWisdomMemory:
    global _memory
    if _memory is None:
        _memory = CollectiveWisdomMemory()
    return _memory


@router.get("/sessions")
async def list_sessions(
    status: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    memory = _get_memory()
    items, total = await memory.list_sessions(
        status=status, limit=limit, offset=offset
    )
    return {
        "items": [
            {
                "session_id": str(s.session_id) if isinstance(s.session_id, UUID) else str(s.get("session_id", "")),
                "question": s.question if hasattr(s, "question") else s.get("question", ""),
                "status": s.status.value if hasattr(s, "status") else s.get("status", ""),
            }
            for s in items
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/sessions/stats")
async def get_session_stats():
    memory = _get_memory()
    return await memory.get_stats()
