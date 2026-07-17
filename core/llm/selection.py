# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import logging
import time as time_module

from core.llm.config import LLMConfig
from core.llm.model_registry import ModelRegistry
from core.llm.provider_registry import ProviderRegistry
from core.models import (
    AdvisorPersona,
    CapabilityRequirement,
    LLMCallLog,
    ModelSelection,
)

logger = logging.getLogger(__name__)


class ModelSelectionEngine:
    def __init__(
        self,
        model_registry: ModelRegistry | None = None,
        provider_registry: ProviderRegistry | None = None,
        llm_config: LLMConfig | None = None,
    ) -> None:
        self.model_registry = model_registry or ModelRegistry()
        self.provider_registry = (
            provider_registry or ProviderRegistry(llm_config or LLMConfig.from_env())
        )
        self._selection_policy: str = "capability_first"

    @property
    def selection_policy(self) -> str:
        return self._selection_policy

    def set_policy(self, policy: str) -> None:
        allowed = ["capability_first", "cost_first", "latency_first", "local_first"]
        if policy not in allowed:
            msg = f"Unknown policy '{policy}'. Allowed: {allowed}"
            raise ValueError(msg)
        self._selection_policy = policy

    def select(
        self,
        persona: AdvisorPersona,
        requirement: CapabilityRequirement,
    ) -> ModelSelection:
        scored = self.model_registry.match(requirement)

        available = self.provider_registry.list_available()
        if not available:
            return ModelSelection(
                persona=persona,
                requirements=requirement,
                selected_model="",
                selected_provider="",
                selection_reason="No providers available. Configure API keys in .env",
            )

        candidates = [
            (m, s) for m, s in scored if m.provider in available
        ]
        if not candidates:
            fallback = [
                (m, s) for m, s in scored if m.provider in (
                    "openai", "anthropic", "google", "openrouter", "ollama"
                )
            ]
            candidates = [(m, s) for m, s in fallback if m.provider in available] or [
                (m, s) for m, s in scored if not m.is_local
            ]

        candidates = self._apply_policy(candidates)
        if not candidates:
            return ModelSelection(
                persona=persona,
                requirements=requirement,
                selected_model="",
                selected_provider="",
                selection_reason="No matching model found for given requirements",
            )

        best_model, best_score = candidates[0]
        return ModelSelection(
            persona=persona,
            requirements=requirement,
            selected_model=best_model.id,
            selected_provider=best_model.provider,
            selection_reason=(
                f"Capability score {best_score}/10 — "
                f"best match across {len(candidates)} available model(s)"
            ),
        )

    def select_with_failover(
        self,
        persona: AdvisorPersona,
        requirement: CapabilityRequirement,
        failed_model: str | None = None,
    ) -> ModelSelection:
        scored = self.model_registry.match(requirement)
        available = self.provider_registry.list_available()

        candidates = [
            (m, s) for m, s in scored
            if m.provider in available and m.id != failed_model
        ]
        candidates = self._apply_policy(candidates)

        if not candidates:
            base = self.select(persona, requirement)
            base.fallback_occurred = bool(failed_model)
            base.fallback_from = failed_model
            base.selection_reason = (
                f"No fallback available after {failed_model} failed. "
                f"Used original selection."
            )
            return base

        fallback_model, fallback_score = candidates[0]
        return ModelSelection(
            persona=persona,
            requirements=requirement,
            selected_model=fallback_model.id,
            selected_provider=fallback_model.provider,
            selection_reason=(
                f"Fallback after {failed_model} failure. "
                f"Selected {fallback_model.id} (capability score {fallback_score}/10)"
            ),
            fallback_occurred=True,
            fallback_from=failed_model,
        )

    def _apply_policy(
        self,
        candidates: list[tuple["ModelMetadata", float]],
    ) -> list[tuple["ModelMetadata", float]]:
        match self._selection_policy:
            case "cost_first":
                candidates.sort(
                    key=lambda x: (-x[0].capability.cost_efficiency, -x[1])
                )
            case "latency_first":
                latency_order = {"low": 0, "medium": 1, "high": 2}
                candidates.sort(
                    key=lambda x: (
                        latency_order.get(x[0].latency, 99),
                        -x[1],
                    )
                )
            case "local_first":
                candidates.sort(
                    key=lambda x: (not x[0].is_local, -x[1])
                )
            case _:
                candidates.sort(key=lambda x: -x[1])
        return candidates

    async def call_with_logging(
        self,
        persona: AdvisorPersona,
        step: str,
        adapter,
        method_name: str,
        *args,
        **kwargs,
    ) -> tuple:
        log = LLMCallLog(
            persona=persona,
            provider=getattr(adapter, "provider_name", "unknown"),
            model=getattr(adapter, "model_name", "unknown"),
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
            logger.warning("LLM call failed: %s/%s/%s — %s", step, persona.value, method_name, e)
            raise
