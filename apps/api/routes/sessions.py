# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from fastapi import APIRouter, Query

router = APIRouter(tags=["sessions"])


@router.get("/sessions")
async def list_sessions(
    status: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {"items": [], "total": 0, "limit": limit, "offset": offset}
