# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from core.models import Argument, Perspective


class VerifiedCapability(BaseModel):
    structured_output_success_rate: float = Field(default=0.0, ge=0, le=100)
    avg_latency_ms: float = Field(default=0.0, ge=0)
    success_rate: float = Field(default=0.0, ge=0, le=100)
    total_calls: int = 0
    avg_wisdom_contribution: float = Field(default=0.0, ge=0, le=10)


class InferenceCapabilities(BaseModel):
    # ── Declared (claimed by the adapter) ────────────────────────
    supports_structured_output: bool = False
    supports_streaming: bool = False
    supports_tools: bool = False
    context_window: int = 0
    models: list[str] = Field(default_factory=list)
    is_local: bool = False

    # ── Verified (proven through benchmarks) ─────────────────────
    verified: VerifiedCapability = Field(default_factory=VerifiedCapability)

    @property
    def available(self) -> bool:
        return len(self.models) > 0

    @property
    def declared_score(self) -> float:
        score = 0.0
        if self.supports_structured_output:
            score += 2.0
        if self.supports_streaming:
            score += 1.0
        if self.supports_tools:
            score += 1.0
        ctx = min(self.context_window / 32000, 1.0)
        score += ctx * 3.0
        return round(score, 2)

    @property
    def verified_score(self) -> float:
        if self.verified.total_calls == 0:
            return 0.0
        components = (
            self.verified.structured_output_success_rate * 0.3
            + (100 - min(self.verified.avg_latency_ms / 20, 100)) * 0.2
            + self.verified.success_rate * 0.3
            + self.verified.avg_wisdom_contribution * 10 * 0.2
        )
        return round(components, 2)


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

    async def generate_counter_argument(
        self,
        advisor_id: str,
        system_prompt: str,
        perspectives: list[Perspective],
        model: str | None = None,
    ) -> Argument:
        raise NotImplementedError(f"{self.adapter_id} does not implement generate_counter_argument")

    async def judge(
        self,
        system_prompt: str,
        arguments: list[Argument],
        question: str,
        model: str | None = None,
    ) -> dict:
        raise NotImplementedError(f"{self.adapter_id} does not implement judge")
