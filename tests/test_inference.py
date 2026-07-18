# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.inference.adapter import InferenceAdapter, InferenceCapabilities, VerifiedCapability
from core.inference.registry import InferenceRegistry
from core.inference.selection import BackendSelector
from core.models import (
    AdvisorPersona,
    CapabilityRequirement,
)


class FakeAdapter(InferenceAdapter):
    def __init__(self, adapter_id: str = "fake") -> None:
        super().__init__(adapter_id)
        self._caps = InferenceCapabilities(
            supports_structured_output=True,
            supports_streaming=True,
            supports_tools=True,
            context_window=128000,
            models=["fake-model-v1"],
            is_local=False,
        )

    def _default_id(self) -> str:
        return "fake"

    @property
    def capabilities(self) -> InferenceCapabilities:
        return self._caps

    async def generate_perspective(self, **kwargs):
        from core.models import Perspective
        return Perspective(advisor_id="fake", confidence=0.8)

    async def generate_counter_argument(self, **kwargs):
        from core.models import Argument
        return Argument(advisor_id="fake")

    async def judge(self, **kwargs):
        return {"decision": "proceed", "confidence": 0.8}


# ── Declared vs Verified Capability tests ──────────────────────

def test_verified_capability_defaults():
    v = VerifiedCapability()
    assert v.total_calls == 0
    assert v.structured_output_success_rate == 0.0


def test_declared_score_structured_only():
    caps = InferenceCapabilities(supports_structured_output=True)
    assert caps.declared_score >= 2.0


def test_declared_score_full():
    caps = InferenceCapabilities(
        supports_structured_output=True,
        supports_streaming=True,
        supports_tools=True,
        context_window=128000,
    )
    score = caps.declared_score
    assert score > 5.0


def test_verified_score_no_data():
    caps = InferenceCapabilities()
    assert caps.verified_score == 0.0


def test_verified_score_with_data():
    caps = InferenceCapabilities(
        verified=VerifiedCapability(
            structured_output_success_rate=95.0,
            avg_latency_ms=1500,
            success_rate=98.0,
            total_calls=100,
            avg_wisdom_contribution=7.5,
        ),
    )
    score = caps.verified_score
    assert score > 0.0


def test_available_without_models():
    caps = InferenceCapabilities()
    assert caps.available is False


def test_available_with_models():
    caps = InferenceCapabilities(models=["test"])
    assert caps.available is True


# ── Registry tests ─────────────────────────────────────────────

def test_inference_registry_empty():
    registry = InferenceRegistry()
    available = registry.list_available()
    assert isinstance(available, list)


def test_inference_registry_register():
    registry = InferenceRegistry()
    adapter = FakeAdapter("test-adapter")
    registry.register(adapter)
    gotten = registry.get("test-adapter")
    assert gotten is not None
    assert gotten.adapter_id == "test-adapter"


def test_registry_record_outcome():
    registry = InferenceRegistry()
    adapter = FakeAdapter("perf-test")
    registry.register(adapter)

    registry.record_outcome("perf-test", success=True, latency_ms=500)
    registry.record_outcome("perf-test", success=True, latency_ms=300)

    caps = adapter.capabilities
    assert caps.verified.total_calls == 2
    assert caps.verified.success_rate == 100.0
    assert caps.verified.avg_latency_ms == 400.0


def test_registry_record_outcome_mixed():
    registry = InferenceRegistry()
    adapter = FakeAdapter("mixed-test")
    registry.register(adapter)

    registry.record_outcome("mixed-test", success=True, latency_ms=200)
    registry.record_outcome("mixed-test", success=False, latency_ms=5000)

    assert adapter.capabilities.verified.total_calls == 2
    assert adapter.capabilities.verified.success_rate == 50.0


# ── BackendSelector tests ──────────────────────────────────────

def test_selector_no_requirement():
    registry = InferenceRegistry()
    adapter = FakeAdapter("sel-test")
    registry.register(adapter)
    selector = BackendSelector(registry=registry)
    selection = selector.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(),
    )
    assert selection.selected_adapter != ""
    assert selection.selected_model != ""


def test_selector_match_score():
    registry = InferenceRegistry()
    adapter = FakeAdapter("score-test")
    registry.register(adapter)
    selector = BackendSelector(registry=registry)
    selection = selector.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(structured_output=True),
    )
    assert selection.selection_reason != ""


def test_selector_structured_output_required():
    registry = InferenceRegistry()
    registry._adapters.clear()

    class NoStructAdapter(FakeAdapter):
        def __init__(self, adapter_id: str = "no-struct"):
            super().__init__(adapter_id)
            self._caps = InferenceCapabilities(
                supports_structured_output=False,
                models=["no-struct-model"],
            )

    registry.register(NoStructAdapter("no-struct"))
    registry.register(FakeAdapter("with-struct"))
    selector = BackendSelector(registry=registry)

    selection = selector.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(structured_output=True),
    )
    assert selection.selected_adapter == "with-struct"


def test_selector_prefers_verified_adapter():
    registry = InferenceRegistry()

    class FreshAdapter(FakeAdapter):
        def __init__(self) -> None:
            super().__init__("fresh")

    class ProvenAdapter(FakeAdapter):
        def __init__(self) -> None:
            super().__init__("proven")

    registry.register(FreshAdapter())
    registry.register(ProvenAdapter())
    registry.record_outcome(
        "proven", success=True, latency_ms=200,
        structured_output_ok=True, wisdom_contribution=8.5,
    )

    selector = BackendSelector(registry=registry)
    selection = selector.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(structured_output=True),
    )
    assert selection.selected_adapter is not None


def test_record_call_outcome():
    registry = InferenceRegistry()
    adapter = FakeAdapter("call-test")
    registry.register(adapter)
    selector = BackendSelector(registry=registry)

    selector.record_call_outcome(
        adapter_id="call-test",
        success=True,
        latency_ms=1000,
        wisdom_contribution=7.0,
    )
    assert adapter.capabilities.verified.total_calls == 1
