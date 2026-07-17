# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2026 OptimaSeo Indonesia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json

import httpx

from core.models import Argument, Perspective
from providers.base import BaseAdvisor


class OllamaAdvisor(BaseAdvisor):
    def __init__(
        self,
        advisor_id: str,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
    ):
        super().__init__(advisor_id, model)
        self.base_url = base_url.rstrip("/")

    async def _call(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "{}")

    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        prompt = (
            f"You are an AI advisor. Analyze this question and provide a structured perspective in JSON.\n"
            f"Question: {question}\nContext: {context}\n\n"
            f'Respond with valid JSON: {{"stance": "...", "summary": "...", "reasoning": "...", "confidence": 0.0-1.0, "key_points": [...]}}'
        )
        content = await self._call(prompt)
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
        prompt = (
            f"Review these perspectives and offer a counter-argument in JSON.\n"
            f"Perspectives: {[p.model_dump() for p in perspectives]}\n\n"
            f'Respond with valid JSON: {{"claim": "...", "evidence": "...", "reasoning": "..."}}'
        )
        content = await self._call(prompt)
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
        prompt = (
            f"You are a neutral judge. Evaluate the arguments and produce a final verdict in JSON.\n"
            f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}\n\n"
            f'Respond with valid JSON: {{"decision": "...", "confidence": 0.0-1.0, "summary": "...", "reasoning": "..."}}'
        )
        content = await self._call(prompt)
        return json.loads(content)
