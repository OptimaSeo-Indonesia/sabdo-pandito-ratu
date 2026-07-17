# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import logging
from collections import defaultdict

from core.inference.adapter import InferenceAdapter, InferenceCapabilities, VerifiedCapability
from inference.adapters.anthropic import AnthropicAdapter
from inference.adapters.ollama import OllamaAdapter
from inference.adapters.openai_compat import OpenAICompatibleAdapter

logger = logging.getLogger(__name__)

_ADAPTER_CLASSES = [
    OpenAICompatibleAdapter,
    AnthropicAdapter,
    OllamaAdapter,
]


class InferenceRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, InferenceAdapter] = {}
        self._verified: dict[str, VerifiedCapability] = defaultdict(VerifiedCapability)
        self._discover()

    def _discover(self) -> None:
        for cls in _ADAPTER_CLASSES:
            try:
                adapter = cls()
                caps = adapter.capabilities
                aid = adapter.adapter_id
                if aid in self._verified:
                    caps.verified = self._verified[aid]
                logger.info(
                    "Discovered adapter '%s': %d model(s), declared=%.1f, verified=%.1f",
                    aid, len(caps.models),
                    caps.declared_score, caps.verified_score,
                )
                self._adapters[aid] = adapter
            except Exception as exc:
                logger.debug("Skipping adapter %s: %s", cls.__name__, exc)

    def register(self, adapter: InferenceAdapter) -> None:
        aid = adapter.adapter_id
        if aid in self._verified:
            adapter.capabilities.verified = self._verified[aid]
        self._adapters[aid] = adapter

    def get(self, adapter_id: str) -> InferenceAdapter | None:
        return self._adapters.get(adapter_id)

    def list_available(self) -> list[InferenceAdapter]:
        return [a for a in self._adapters.values() if a.capabilities.available]

    def list_all(self) -> list[InferenceAdapter]:
        return list(self._adapters.values())

    def list_capabilities(self) -> list[tuple[str, InferenceCapabilities]]:
        return [(aid, a.capabilities) for aid, a in self._adapters.items()]

    def record_outcome(
        self,
        adapter_id: str,
        success: bool,
        latency_ms: int,
        structured_output_ok: bool = True,
        wisdom_contribution: float = 0.0,
    ) -> None:
        v = self._verified[adapter_id]
        old_total = v.total_calls
        v.total_calls += 1
        v.success_rate = (
            (v.success_rate * old_total + (100.0 if success else 0.0))
            / v.total_calls
        )
        v.avg_latency_ms = (
            (v.avg_latency_ms * old_total + latency_ms) / v.total_calls
        )
        if structured_output_ok:
            v.structured_output_success_rate = (
                (v.structured_output_success_rate * old_total + 100.0)
                / v.total_calls
            )
        else:
            v.structured_output_success_rate = (
                (v.structured_output_success_rate * old_total) / v.total_calls
            )
        v.avg_wisdom_contribution = (
            (v.avg_wisdom_contribution * old_total + wisdom_contribution)
            / v.total_calls
        )
        if adapter_id in self._adapters:
            self._adapters[adapter_id].capabilities.verified = v
