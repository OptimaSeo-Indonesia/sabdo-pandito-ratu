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

_VERIFIED_WEIGHT = 0.3


class BackendSelector:
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

        scored: list[tuple[InferenceAdapter, str, float, float, float]] = []
        for adapter in adapters:
            caps = adapter.capabilities
            for model in caps.models:
                declared, verified, combined = self._compute_score(caps, requirement)
                scored.append((adapter, model, declared, verified, combined))

        scored.sort(key=lambda x: x[4], reverse=True)
        best = scored[0]
        reason_parts = [
            f"Declared={best[2]:.1f}/10",
        ]
        if best[3] > 0:
            reason_parts.append(f"Verified={best[3]:.1f}/100")
            reason_parts.append(f"Combined={best[4]:.1f}/10")
        else:
            reason_parts.append("(no verified data yet)")
        reason_parts.append(
            f"— best across {len(scored)} adapter/model(s)"
        )
        return InferenceSelection(
            persona=persona,
            requirements=requirement,
            selected_adapter=best[0].adapter_id,
            selected_model=best[1],
            selection_reason=", ".join(reason_parts),
        )

    def _compute_score(
        self,
        caps: InferenceCapabilities,
        req: CapabilityRequirement,
    ) -> tuple[float, float, float]:
        if req.structured_output and not caps.supports_structured_output:
            return (-1.0, -1.0, -1.0)

        # Declared score
        declared = caps.declared_score
        if caps.is_local:
            declared += 0.5

        # Verified score (0-100)
        verified = caps.verified_score

        # Combined: declared is on 0-10 scale, verified is on 0-100 scale
        # verified_weight controls how much verified data influences the result
        combined = declared * (1 - _VERIFIED_WEIGHT) + (verified / 10) * _VERIFIED_WEIGHT
        combined = round(combined, 2)

        return (declared, verified, combined)

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
        model = kwargs.get("model") or (caps.models[0] if caps.models else "unknown")
        log = LLMCallLog(
            persona=persona,
            provider=adapter.adapter_id,
            model=model,
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
            logger.warning(
                "Backend call failed: %s/%s/%s — %s",
                step, persona.value, method_name, e,
            )
            raise

    def record_call_outcome(
        self,
        adapter_id: str,
        success: bool,
        latency_ms: int,
        structured_output_ok: bool = True,
        wisdom_contribution: float = 0.0,
    ) -> None:
        self._registry.record_outcome(
            adapter_id=adapter_id,
            success=success,
            latency_ms=latency_ms,
            structured_output_ok=structured_output_ok,
            wisdom_contribution=wisdom_contribution,
        )
