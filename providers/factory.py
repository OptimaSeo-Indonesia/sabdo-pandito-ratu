# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

from core.models import ModelSelection
from core.llm.provider_registry import ProviderRegistry
from providers.anthropic.adapter import AnthropicAdvisor
from providers.ollama.adapter import OllamaAdvisor
from providers.openai.adapter import OpenAIAdvisor


class AdvisorFactory:
    def __init__(self, provider_registry: ProviderRegistry) -> None:
        self._provider_registry = provider_registry

    def create(self, selection: ModelSelection, advisor_id: str) -> object:
        api_key, base_url = self._provider_registry.get_credentials(
            selection.selected_provider
        )
        match selection.selected_provider:
            case "openai" | "openrouter":
                return OpenAIAdvisor(
                    advisor_id=advisor_id,
                    model=selection.selected_model,
                    api_key=api_key,
                    base_url=base_url,
                )
            case "anthropic":
                return AnthropicAdvisor(
                    advisor_id=advisor_id,
                    model=selection.selected_model,
                    api_key=api_key,
                    base_url=base_url,
                )
            case "ollama":
                return OllamaAdvisor(
                    advisor_id=advisor_id,
                    model=selection.selected_model,
                    base_url=base_url,
                )
            case _:
                msg = f"Unsupported provider: {selection.selected_provider}"
                raise ValueError(msg)
