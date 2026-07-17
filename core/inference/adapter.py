# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from core.models import Argument, Perspective


class InferenceCapabilities(BaseModel):
    supports_structured_output: bool = False
    supports_streaming: bool = False
    supports_tools: bool = False
    context_window: int = 0
    models: list[str] = Field(default_factory=list)
    is_local: bool = False

    @property
    def available(self) -> bool:
        return len(self.models) > 0


class InferenceAdapter(ABC):
    def __init__(self, adapter_id: str = "") -> None:
        self.adapter_id = adapter_id or self._default_id()

    @abstractmethod
    def _default_id(self) -> str:
        ...

    @property
    @abstractmethod
    def capabilities(self) -> InferenceCapabilities:
        ...

    @abstractmethod
    async def generate_perspective(
        self,
        advisor_id: str,
        system_prompt: str,
        question: str,
        context: dict,
        model: str | None = None,
    ) -> Perspective:
        ...

    @abstractmethod
    async def generate_counter_argument(
        self,
        advisor_id: str,
        system_prompt: str,
        perspectives: list[Perspective],
        model: str | None = None,
    ) -> Argument:
        ...

    @abstractmethod
    async def judge(
        self,
        system_prompt: str,
        arguments: list[Argument],
        question: str,
        model: str | None = None,
    ) -> dict:
        ...
