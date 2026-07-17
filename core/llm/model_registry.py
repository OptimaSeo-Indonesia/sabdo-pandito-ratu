# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

from core.models import ModelCapability, ModelMetadata


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, ModelMetadata] = {}
        self._register_known_models()

    def _register_known_models(self) -> None:
        known: list[ModelMetadata] = [
            # ── OpenAI ──────────────────────────────────────────
            ModelMetadata(
                id="gpt-4o",
                provider="openai",
                display_name="GPT-4o",
                context_window=128000,
                capability=ModelCapability(
                    reasoning=9,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=7,
                    numerical_reasoning=9,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=5,
                ),
                latency="low",
            ),
            ModelMetadata(
                id="gpt-4o-mini",
                provider="openai",
                display_name="GPT-4o Mini",
                context_window=128000,
                capability=ModelCapability(
                    reasoning=7,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=5,
                    numerical_reasoning=7,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=8,
                ),
                latency="low",
            ),
            ModelMetadata(
                id="o3-mini",
                provider="openai",
                display_name="o3 Mini",
                context_window=200000,
                capability=ModelCapability(
                    reasoning=10,
                    structured_output=True,
                    nuanced_language=False,
                    ethical_reasoning=4,
                    numerical_reasoning=10,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=7,
                ),
                latency="medium",
            ),
            # ── Anthropic ───────────────────────────────────────
            ModelMetadata(
                id="claude-3-5-sonnet",
                provider="anthropic",
                display_name="Claude 3.5 Sonnet",
                context_window=200000,
                capability=ModelCapability(
                    reasoning=9,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=9,
                    numerical_reasoning=7,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=4,
                ),
                latency="low",
            ),
            ModelMetadata(
                id="claude-3-haiku",
                provider="anthropic",
                display_name="Claude 3 Haiku",
                context_window=200000,
                capability=ModelCapability(
                    reasoning=6,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=7,
                    numerical_reasoning=5,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=9,
                ),
                latency="low",
            ),
            # ── Google ──────────────────────────────────────────
            ModelMetadata(
                id="gemini-2.0-flash",
                provider="google",
                display_name="Gemini 2.0 Flash",
                context_window=1048576,
                capability=ModelCapability(
                    reasoning=7,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=6,
                    numerical_reasoning=7,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=9,
                ),
                latency="low",
            ),
            ModelMetadata(
                id="gemini-2.5-pro",
                provider="google",
                display_name="Gemini 2.5 Pro",
                context_window=1048576,
                capability=ModelCapability(
                    reasoning=9,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=8,
                    numerical_reasoning=9,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=5,
                ),
                latency="medium",
            ),
            # ── OpenRouter ──────────────────────────────────────
            ModelMetadata(
                id="openrouter/auto",
                provider="openrouter",
                display_name="OpenRouter Auto",
                context_window=128000,
                capability=ModelCapability(
                    reasoning=7,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=6,
                    numerical_reasoning=7,
                    long_context=True,
                    high_reliability=True,
                    cost_efficiency=7,
                ),
                latency="medium",
            ),
            # ── Ollama (local) ──────────────────────────────────
            ModelMetadata(
                id="llama3.1",
                provider="ollama",
                display_name="Llama 3.1",
                context_window=8192,
                capability=ModelCapability(
                    reasoning=6,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=5,
                    numerical_reasoning=5,
                    long_context=False,
                    high_reliability=False,
                    cost_efficiency=10,
                ),
                latency="medium",
                is_local=True,
            ),
            ModelMetadata(
                id="qwen2.5",
                provider="ollama",
                display_name="Qwen 2.5",
                context_window=32768,
                capability=ModelCapability(
                    reasoning=7,
                    structured_output=True,
                    nuanced_language=True,
                    ethical_reasoning=6,
                    numerical_reasoning=7,
                    long_context=True,
                    high_reliability=False,
                    cost_efficiency=10,
                ),
                latency="medium",
                is_local=True,
            ),
        ]
        for m in known:
            self._models[m.id] = m

    def register(self, model: ModelMetadata) -> None:
        self._models[model.id] = model

    def get(self, model_id: str) -> ModelMetadata | None:
        return self._models.get(model_id)

    def list_all(self) -> list[ModelMetadata]:
        return list(self._models.values())

    def list_by_provider(self, provider: str) -> list[ModelMetadata]:
        return [m for m in self._models.values() if m.provider == provider]

    def match(self, requirement: "CapabilityRequirement") -> list[tuple[ModelMetadata, float]]:
        scored: list[tuple[ModelMetadata, float]] = []
        for model in self._models.values():
            score = self._compute_match(model, requirement)
            scored.append((model, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def _compute_match(
        self, model: ModelMetadata, req: "CapabilityRequirement"
    ) -> float:
        fields = [
            ("reasoning", req.reasoning, model.capability.reasoning),
            ("ethical_reasoning", req.ethical_reasoning, model.capability.ethical_reasoning),
            ("numerical_reasoning", req.numerical_reasoning, model.capability.numerical_reasoning),
        ]
        score = 0.0
        total_weight = 0.0
        for _name, req_val, cap_val in fields:
            if req_val > 0:
                weight = float(req_val)
                match_ratio = min(cap_val / max(req_val, 1), 1.0)
                score += weight * match_ratio
                total_weight += weight

        if req.structured_output and not model.capability.structured_output:
            return -1.0

        if req.nuanced_language and not model.capability.nuanced_language:
            score *= 0.5

        if req.long_context and not model.capability.long_context:
            score *= 0.3

        if req.high_reliability and not model.capability.high_reliability:
            score *= 0.6

        base = score / max(total_weight, 1) * 10 if total_weight > 0 else 5.0
        return round(base, 2)
