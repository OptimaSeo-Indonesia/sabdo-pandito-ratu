# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2025 OptimaSeo Indonesia
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

from anthropic import AsyncAnthropic

from core.models import Argument, Perspective
from providers.base import BaseAdvisor


class AnthropicAdvisor(BaseAdvisor):
    def __init__(
        self,
        advisor_id: str,
        model: str = "claude-3-opus-20240229",
        api_key: str = "",
        base_url: str = "https://api.anthropic.com",
    ):
        super().__init__(advisor_id, model)
        self.client = AsyncAnthropic(api_key=api_key, base_url=base_url)

    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="You are an AI advisor. Analyze the question and provide a structured perspective in JSON.",
            messages=[
                {
                    "role": "user",
                    "content": f"Question: {question}\nContext: {context}\n\nRespond in JSON with keys: stance, summary, reasoning, confidence, key_points",
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
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
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="Review the perspectives and offer a counter-argument in JSON.",
            messages=[
                {
                    "role": "user",
                    "content": f"Perspectives: {[p.model_dump() for p in perspectives]}\n\nRespond with JSON: claim, evidence, reasoning",
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
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
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="You are a neutral judge. Evaluate the arguments and produce a final verdict in JSON.",
            messages=[
                {
                    "role": "user",
                    "content": f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}\n\nRespond with JSON: decision, confidence, summary, reasoning",
                }
            ],
        )
        content = response.content[0].text if response.content else "{}"
        import json

        return json.loads(content)
