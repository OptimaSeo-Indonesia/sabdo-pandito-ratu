# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

from core.llm.config import LLMConfig


class ProviderRegistry:
    def __init__(self, config: LLMConfig) -> None:
        self._config = config

    @property
    def config(self) -> LLMConfig:
        return self._config

    def list_available(self) -> list[str]:
        return self._config.list_available()

    def is_available(self, provider: str) -> bool:
        return provider in self.list_available()

    def get_credentials(self, provider: str) -> tuple[str, str]:
        match provider:
            case "openai":
                return (self._config.openai.api_key, self._config.openai.base_url)
            case "anthropic":
                return (self._config.anthropic.api_key, self._config.anthropic.base_url)
            case "google":
                return (self._config.google.api_key, self._config.google.base_url)
            case "openrouter":
                return (self._config.openrouter.api_key, self._config.openrouter.base_url)
            case "ollama":
                return ("", self._config.ollama.base_url)
            case _:
                return ("", "")
