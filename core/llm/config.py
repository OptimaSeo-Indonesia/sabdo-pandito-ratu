# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import os
from dataclasses import dataclass, field


@dataclass
class ProviderConfig:
    api_key: str = ""
    base_url: str = ""
    available: bool = False


@dataclass
class LLMConfig:
    openai: ProviderConfig = field(default_factory=ProviderConfig)
    anthropic: ProviderConfig = field(default_factory=ProviderConfig)
    google: ProviderConfig = field(default_factory=ProviderConfig)
    openrouter: ProviderConfig = field(default_factory=ProviderConfig)
    ollama: ProviderConfig = field(default_factory=ProviderConfig)

    @classmethod
    def from_env(cls) -> "LLMConfig":
        def _provider(
            key_var: str, url_var: str | None = None
        ) -> ProviderConfig:
            api_key = os.getenv(key_var, "")
            base_url = os.getenv(url_var, "") if url_var else ""
            return ProviderConfig(
                api_key=api_key,
                base_url=base_url,
                available=bool(api_key or url_var == "OLLAMA_BASE_URL"),
            )

        return cls(
            openai=_provider("OPENAI_API_KEY", "OPENAI_BASE_URL"),
            anthropic=_provider("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL"),
            google=_provider("GOOGLE_API_KEY", "GOOGLE_BASE_URL"),
            openrouter=_provider("OPENROUTER_API_KEY", "OPENROUTER_BASE_URL"),
            ollama=ProviderConfig(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                available=True,
            ),
        )

    def list_available(self) -> list[str]:
        return [
            name
            for name, cfg in [
                ("openai", self.openai),
                ("anthropic", self.anthropic),
                ("google", self.google),
                ("openrouter", self.openrouter),
                ("ollama", self.ollama),
            ]
            if cfg.available
        ]
