# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from openai import AsyncOpenAI

from core.models import Argument, Perspective
from providers.base import BaseAdvisor


class OpenAIAdvisor(BaseAdvisor):
    def __init__(
        self,
        advisor_id: str,
        model: str = "gpt-4-turbo",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
    ):
        super().__init__(advisor_id, model)
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI advisor. Analyze the question and provide a structured perspective.",
                },
                {"role": "user", "content": f"Question: {question}\nContext: {context}"},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        import json

        data = json.loads(content)
        return Perspective(
            advisor_id=self.advisor_id,
            stance=data.get("stance", "neutral"),
            summary=data.get("summary", ""),
            reasoning=data.get("reasoning", ""),
            confidence=data.get("confidence", 0.5),
            key_points=data.get("key_points", []),
        )

    async def generate_counter_argument(
        self, perspectives: list[Perspective]
    ) -> Argument:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Review the perspectives provided and offer a counter-argument.",
                },
                {
                    "role": "user",
                    "content": f"Perspectives: {[p.model_dump() for p in perspectives]}",
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        import json

        data = json.loads(content)
        return Argument(
            advisor_id=self.advisor_id,
            claim=data.get("claim", ""),
            evidence=data.get("evidence", ""),
            reasoning=data.get("reasoning", ""),
        )

    async def judge(
        self, arguments: list[Argument], question: str
    ) -> dict:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a neutral judge. Evaluate the arguments and produce a final verdict.",
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}",
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        import json

        return json.loads(content)
