# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes import deliberations, advisors, sessions

logger = logging.getLogger(__name__)

settings = get_settings()

# ── OpenTelemetry instrumentation ────────────────────────────────
try:
    from opentelemetry import trace
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    resource = Resource.create({"service.name": "sabdo-pandito-ratu"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    _instrumented = True
    logger.info("OpenTelemetry instrumentation enabled")
except ImportError:
    _instrumented = False
    logger.info("OpenTelemetry not available — instrumentation disabled")

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

if _instrumented:
    FastAPIInstrumentor.instrument_app(app)

app.include_router(deliberations.router, prefix="/api/v1")
app.include_router(advisors.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
