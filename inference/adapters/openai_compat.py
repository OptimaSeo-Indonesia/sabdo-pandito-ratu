# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import json
import os

from openai import AsyncOpenAI

from core.inference.adapter import InferenceAdapter, InferenceCapabilities
from core.models import Argument, Perspective


class OpenAICompatibleAdapter(InferenceAdapter):
    def __init__(self, adapter_id: str = "") -> None:
        self._api_key = os.getenv("OPENAI_API_KEY", "")
        self._base_url = os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        if self._api_key:
            self._client = AsyncOpenAI(
                api_key=self._api_key, base_url=self._base_url
            )
        super().__init__(adapter_id)

    def _default_id(self) -> str:
        return "openai_compatible"

    @property
    def capabilities(self) -> InferenceCapabilities:
        if not self._api_key:
            return InferenceCapabilities()
        return InferenceCapabilities(
            supports_structured_output=True,
            supports_streaming=True,
            supports_tools=True,
            context_window=128000,
            models=["gpt-4o", "gpt-4o-mini"],
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
        model = model or "gpt-4o"
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Question: {question}\nContext: {context}",
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
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
        model = model or "gpt-4o"
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Perspectives: {[p.model_dump() for p in perspectives]}",
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
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
        model = model or "gpt-4o"
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}",
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)
