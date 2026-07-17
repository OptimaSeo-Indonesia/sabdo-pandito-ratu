# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import logging

from core.inference.adapter import InferenceAdapter, InferenceCapabilities
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
        self._discover()

    def _discover(self) -> None:
        for cls in _ADAPTER_CLASSES:
            try:
                adapter = cls()
                caps = adapter.capabilities
                logger.info(
                    "Discovered adapter '%s': %d model(s), structured=%s, local=%s",
                    adapter.adapter_id,
                    len(caps.models),
                    caps.supports_structured_output,
                    caps.is_local,
                )
                self._adapters[adapter.adapter_id] = adapter
            except Exception as exc:
                logger.debug("Skipping adapter %s: %s", cls.__name__, exc)

    def register(self, adapter: InferenceAdapter) -> None:
        self._adapters[adapter.adapter_id] = adapter

    def get(self, adapter_id: str) -> InferenceAdapter | None:
        return self._adapters.get(adapter_id)

    def list_available(self) -> list[InferenceAdapter]:
        return [a for a in self._adapters.values() if a.capabilities.available]

    def list_all(self) -> list[InferenceAdapter]:
        return list(self._adapters.values())

    def list_capabilities(self) -> list[tuple[str, InferenceCapabilities]]:
        return [(aid, a.capabilities) for aid, a in self._adapters.items()]
