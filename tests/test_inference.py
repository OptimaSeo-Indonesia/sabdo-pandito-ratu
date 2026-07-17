# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.inference.adapter import InferenceAdapter, InferenceCapabilities
from core.inference.registry import InferenceRegistry
from core.inference.selection import InferenceSelectionEngine
from core.models import (
    AdvisorPersona,
    CapabilityRequirement,
)


class FakeAdapter(InferenceAdapter):
    def __init__(self, adapter_id: str = "fake") -> None:
        super().__init__(adapter_id)

    def _default_id(self) -> str:
        return "fake"

    @property
    def capabilities(self) -> InferenceCapabilities:
        return InferenceCapabilities(
            supports_structured_output=True,
            supports_streaming=True,
            supports_tools=True,
            context_window=128000,
            models=["fake-model-v1"],
            is_local=False,
        )

    async def generate_perspective(self, **kwargs):
        from core.models import Perspective
        return Perspective(advisor_id="fake")

    async def generate_counter_argument(self, **kwargs):
        from core.models import Argument
        return Argument(advisor_id="fake")

    async def judge(self, **kwargs):
        return {"decision": "proceed", "confidence": 0.8}


def test_inference_capabilities_defaults():
    caps = InferenceCapabilities()
    assert caps.available is False
    assert caps.supports_structured_output is False


def test_inference_capabilities_available():
    caps = InferenceCapabilities(models=["test-model"])
    assert caps.available is True


def test_inference_registry_empty():
    registry = InferenceRegistry()
    available = registry.list_available()
    # Should have Ollama adapter at minimum (always available)
    assert isinstance(available, list)


def test_inference_registry_register():
    registry = InferenceRegistry()
    adapter = FakeAdapter("test-adapter")
    registry.register(adapter)
    gotten = registry.get("test-adapter")
    assert gotten is not None
    assert gotten.adapter_id == "test-adapter"


def test_inference_registry_list_capabilities():
    registry = InferenceRegistry()
    adapter = FakeAdapter("caps-test")
    registry.register(adapter)
    caps_list = registry.list_capabilities()
    ids = [aid for aid, _ in caps_list]
    assert "caps-test" in ids


def test_selection_engine_no_requirement():
    registry = InferenceRegistry()
    adapter = FakeAdapter("sel-test")
    registry.register(adapter)
    engine = InferenceSelectionEngine(registry=registry)
    selection = engine.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(),
    )
    assert selection.selected_adapter != ""
    assert selection.selected_model != ""


def test_selection_engine_match_score():
    registry = InferenceRegistry()
    adapter = FakeAdapter("score-test")
    registry.register(adapter)
    engine = InferenceSelectionEngine(registry=registry)
    selection = engine.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(structured_output=True),
    )
    assert selection.selection_reason != ""


def test_selection_engine_structured_output_required():
    registry = InferenceRegistry()

    class NoStructAdapter(FakeAdapter):
        @property
        def capabilities(self) -> InferenceCapabilities:
            return InferenceCapabilities(
                supports_structured_output=False,
                models=["no-struct-model"],
            )

    registry.register(NoStructAdapter("no-struct"))
    engine = InferenceSelectionEngine(registry=registry)

    adapter = FakeAdapter("with-struct")
    registry.register(adapter)

    selection = engine.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(structured_output=True),
    )
    # Should prefer the adapter with structured output
    assert selection.selected_adapter == "with-struct"
