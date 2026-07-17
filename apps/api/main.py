from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes import deliberations, advisors, sessions

settings = get_settings()

app = FastAPI(
    title="Sabdo Pandito Ratu API",
    description="Open source deliberation engine for multi-AI decision making",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deliberations.router, prefix="/api/v1")
app.include_router(advisors.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
