# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

import json
import os

import httpx

from core.inference.adapter import InferenceAdapter, InferenceCapabilities
from core.models import Argument, Perspective


class OllamaAdapter(InferenceAdapter):
    def __init__(self, adapter_id: str = "") -> None:
        self._base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._discovered_models: list[str] | None = None
        super().__init__(adapter_id)

    def _default_id(self) -> str:
        return "ollama"

    def _discover_models(self) -> None:
        if self._discovered_models is not None:
            return
        try:
            import httpx
            resp = httpx.get(f"{self._base_url}/api/tags", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                self._discovered_models = [
                    m["name"] for m in data.get("models", [])
                ]
        except Exception:
            pass

    @property
    def capabilities(self) -> InferenceCapabilities:
        return InferenceCapabilities(
            supports_structured_output=True,
            supports_streaming=False,
            supports_tools=False,
            context_window=8192,
            models=["llama3.1", "qwen2.5"],
            is_local=True,
        )

    async def _call(self, prompt: str, model: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "{}")

    async def generate_perspective(
        self,
        advisor_id: str,
        system_prompt: str,
        question: str,
        context: dict,
        model: str | None = None,
    ) -> Perspective:
        self._discover_models()
        models = self._discovered_models or ["llama3.1", "qwen2.5"]
        prompt = (
            f"{system_prompt}\n\n"
            f"Question: {question}\nContext: {context}\n\n"
            f'Respond with valid JSON: {{"stance": "...", "summary": "...", "reasoning": "...", "confidence": 0.0-1.0, "key_points": [...]}}'
        )
        content = await self._call(prompt, model)
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
        self._discover_models()
        models = self._discovered_models or ["llama3.1", "qwen2.5"]
        prompt = (
            f"{system_prompt}\n\n"
            f"Perspectives: {[p.model_dump() for p in perspectives]}\n\n"
            f'Respond with valid JSON: {{"claim": "...", "evidence": "...", "reasoning": "..."}}'
        )
        content = await self._call(prompt, model)
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
        self._discover_models()
        models = self._discovered_models or ["llama3.1", "qwen2.5"]
        prompt = (
            f"{system_prompt}\n\n"
            f"Question: {question}\nArguments: {[a.model_dump() for a in arguments]}\n\n"
            f'Respond with valid JSON: {{"decision": "...", "confidence": 0.0-1.0, "summary": "...", "reasoning": "..."}}'
        )
        content = await self._call(prompt, model)
        return json.loads(content)
