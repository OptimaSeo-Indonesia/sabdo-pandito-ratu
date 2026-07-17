# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import logging
import time as time_module

from core.inference.adapter import InferenceAdapter, InferenceCapabilities
from core.inference.registry import InferenceRegistry
from core.models import (
    AdvisorPersona,
    CapabilityRequirement,
    InferenceSelection,
    LLMCallLog,
)

logger = logging.getLogger(__name__)


class InferenceSelectionEngine:
    def __init__(
        self,
        registry: InferenceRegistry | None = None,
    ) -> None:
        self._registry = registry or InferenceRegistry()

    @property
    def registry(self) -> InferenceRegistry:
        return self._registry

    def select(
        self,
        persona: AdvisorPersona,
        requirement: CapabilityRequirement,
    ) -> InferenceSelection:
        adapters = self._registry.list_available()
        if not adapters:
            return InferenceSelection(
                persona=persona,
                requirements=requirement,
                selected_adapter="",
                selected_model="",
                selection_reason="No inference adapters available. Configure API keys in .env",
            )

        scored: list[tuple[InferenceAdapter, str, float]] = []
        for adapter in adapters:
            caps = adapter.capabilities
            for model in caps.models:
                score = self._compute_match(caps, requirement, model)
                scored.append((adapter, model, score))

        scored.sort(key=lambda x: x[2], reverse=True)
        best = scored[0]
        return InferenceSelection(
            persona=persona,
            requirements=requirement,
            selected_adapter=best[0].adapter_id,
            selected_model=best[1],
            selection_reason=(
                f"Capability score {best[2]:.1f}/10 — "
                f"best match across {len(scored)} available adapter/model(s)"
            ),
        )

    def _compute_match(
        self,
        caps: InferenceCapabilities,
        req: CapabilityRequirement,
        _model: str,
    ) -> float:
        if req.structured_output and not caps.supports_structured_output:
            return -1.0

        context_score = min(caps.context_window / 32000, 1.0) * 10 if caps.context_window > 0 else 5.0
        req_ctx = 1.0 if req.long_context else 0.0
        ctx_match = context_score * (0.5 + 0.5 * req_ctx)

        base = ctx_match * 0.4 + 6.0 * 0.6
        if caps.is_local:
            base += 1.0
        return round(base, 2)

    async def call_with_logging(
        self,
        persona: AdvisorPersona,
        step: str,
        adapter: InferenceAdapter,
        method_name: str,
        *args,
        **kwargs,
    ) -> tuple:
        caps = adapter.capabilities
        log = LLMCallLog(
            persona=persona,
            provider=adapter.adapter_id,
            model=caps.models[0] if caps.models else "unknown",
            step=step,
        )
        start = time_module.monotonic()
        try:
            result = await getattr(adapter, method_name)(*args, **kwargs)
            elapsed = int((time_module.monotonic() - start) * 1000)
            log.latency_ms = elapsed
            log.success = True
            return result, log
        except Exception as e:
            elapsed = int((time_module.monotonic() - start) * 1000)
            log.latency_ms = elapsed
            log.success = False
            log.error_message = str(e)
            logger.warning("Inference call failed: %s/%s/%s — %s", step, persona.value, method_name, e)
            raise
