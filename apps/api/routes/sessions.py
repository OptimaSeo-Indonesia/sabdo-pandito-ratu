from fastapi import APIRouter, Query

router = APIRouter(tags=["sessions"])


@router.get("/sessions")
async def list_sessions(
    status: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {"items": [], "total": 0, "limit": limit, "offset": offset}
