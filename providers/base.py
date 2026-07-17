# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from abc import ABC, abstractmethod

from core.models import Argument, Perspective


class BaseAdvisor(ABC):
    def __init__(self, advisor_id: str, model: str, config: dict | None = None):
        self.advisor_id = advisor_id
        self.model_name = model
        self.provider_name = self._detect_provider()
        self.config = config or {}

    def _detect_provider(self) -> str:
        module = type(self).__module__
        if "openai" in module:
            return "openai"
        if "anthropic" in module:
            return "anthropic"
        if "ollama" in module:
            return "ollama"
        return "unknown"

    @abstractmethod
    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        ...

    @abstractmethod
    async def generate_counter_argument(
        self, perspectives: list[Perspective]
    ) -> Argument:
        ...

    @abstractmethod
    async def judge(
        self, arguments: list[Argument], question: str
    ) -> dict:
        ...
