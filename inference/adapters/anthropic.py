# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import json
import os

from anthropic import AsyncAnthropic

from core.inference.adapter import InferenceAdapter, InferenceCapabilities
from core.models import Argument, Perspective


class AnthropicAdapter(InferenceAdapter):
    def __init__(self, adapter_id: str = "") -> None:
        self._api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self._base_url = os.getenv(
            "ANTHROPIC_BASE_URL", "https://api.anthropic.com"
        )
        if self._api_key:
            self._client = AsyncAnthropic(
                api_key=self._api_key, base_url=self._base_url
            )
        super().__init__(adapter_id)

    def _default_id(self) -> str:
        return "anthropic"

    @property
    def capabilities(self) -> InferenceCapabilities:
        if not self._api_key:
            return InferenceCapabilities()
        return InferenceCapabilities(
            supports_structured_output=True,
            supports_streaming=True,
            supports_tools=True,
            context_window=200000,
            models=["claude-3-5-sonnet", "claude-3-haiku"],
            is_local=False,
        )

    async def generate_perspective(
        self,
        advisor_id: str,
        system_prompt: str,
        question: str,
        context: dict,
        model: str | None = None,
    ) -> Perspective:
        model = model or "claude-3-5-sonnet"
        response = await self._client.messages.create(
            model=model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\nContext: {context}\n\n"
                        f"Respond in JSON with keys: stance, summary, reasoning, confidence, key_points"
                    ),
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
        data = json.loads(content)
        return Perspective(
            advisor_id=advisor_id,
            stance=data.get("stance", "neutral"),
            summary=data.get("summary", ""),
            reasoning=data.get("reasoning", ""),
            confidence=data.get("confidence", 0.5),
            key_points=data.get("key_points", []),
        )

    async def generate_counter_argument(
        self,
        advisor_id: str,
        system_prompt: str,
        perspectives: list[Perspective],
        model: str | None = None,
    ) -> Argument:
        model = model or "claude-3-5-sonnet"
        response = await self._client.messages.create(
            model=model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Perspectives: {[p.model_dump() for p in perspectives]}\n\n"
                        f"Respond with JSON: claim, evidence, reasoning"
                    ),
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
        data = json.loads(content)
        return Argument(
            advisor_id=advisor_id,
            persona=data.get("persona", advisor_id),
            claim=data.get("claim", ""),
            evidence=data.get("evidence", ""),
            reasoning=data.get("reasoning", ""),
        )

    async def judge(
        self,
        system_prompt: str,
        arguments: list[Argument],
        question: str,
        model: str | None = None,
    ) -> dict:
        model = model or "claude-3-5-sonnet"
        response = await self._client.messages.create(
            model=model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}\n\n"
                        f"Respond with JSON: decision, confidence, summary, reasoning"
                    ),
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
        return json.loads(content)
