# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.llm.config import LLMConfig
from core.llm.model_registry import ModelRegistry
from core.llm.provider_registry import ProviderRegistry
from core.llm.selection import ModelSelectionEngine
from core.models import (
    AdvisorPersona,
    CapabilityRequirement,
    ModelMetadata,
)


def test_config_from_env():
    config = LLMConfig.from_env()
    assert config.openai is not None
    assert config.ollama is not None


def test_config_list_available():
    config = LLMConfig.from_env()
    available = config.list_available()
    assert isinstance(available, list)


def test_model_registry_initialization():
    registry = ModelRegistry()
    all_models = registry.list_all()
    assert len(all_models) > 0


def test_model_registry_get_known():
    registry = ModelRegistry()
    model = registry.get("gpt-4o")
    assert model is not None
    assert model.provider == "openai"
    assert model.capability.reasoning == 9


def test_model_registry_get_unknown():
    registry = ModelRegistry()
    model = registry.get("nonexistent-model")
    assert model is None


def test_model_registry_register_custom():
    registry = ModelRegistry()
    custom = ModelMetadata(
        id="custom-model",
        provider="custom",
        display_name="Custom Model",
        context_window=4096,
    )
    registry.register(custom)
    gotten = registry.get("custom-model")
    assert gotten is not None
    assert gotten.provider == "custom"


def test_model_registry_list_by_provider():
    registry = ModelRegistry()
    openai_models = registry.list_by_provider("openai")
    assert len(openai_models) >= 2
    assert all(m.provider == "openai" for m in openai_models)


def test_model_registry_match():
    registry = ModelRegistry()
    req = CapabilityRequirement(
        reasoning=9,
        structured_output=True,
        ethical_reasoning=7,
        numerical_reasoning=9,
    )
    scored = registry.match(req)
    assert len(scored) > 0
    # Best match should be at least 7/10
    best, score = scored[0]
    assert score >= 7.0


def test_model_registry_match_structured_output_required():
    from core.models import ModelCapability
    registry = ModelRegistry()
    registry.register(
        ModelMetadata(
            id="no-struct",
            provider="ollama",
            display_name="No Struct",
            context_window=4096,
            capability=ModelCapability(structured_output=False),
        )
    )
    req = CapabilityRequirement(structured_output=True)
    scored = registry.match(req)
    no_struct = [s for m, s in scored if m.id == "no-struct"]
    if no_struct:
        assert no_struct[0] == -1.0


def test_provider_registry_config():
    config = LLMConfig()
    provider_reg = ProviderRegistry(config)
    assert provider_reg.config is not None


def test_provider_registry_list_empty():
    config = LLMConfig()
    provider_reg = ProviderRegistry(config)
    available = provider_reg.list_available()
    assert isinstance(available, list)


def test_selection_engine_initialization():
    engine = ModelSelectionEngine()
    assert engine.selection_policy == "capability_first"


def test_selection_engine_set_policy():
    engine = ModelSelectionEngine()
    engine.set_policy("cost_first")
    assert engine.selection_policy == "cost_first"


def test_selection_engine_invalid_policy():
    engine = ModelSelectionEngine()
    try:
        engine.set_policy("invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_selection_returns_model_with_ollama():
    engine = ModelSelectionEngine()
    # Ollama is always available (no API key needed)
    selection = engine.select(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(reasoning=8),
    )
    # Should select an ollama model since it's the only available provider
    assert selection.selected_provider == "ollama"
    assert selection.selected_model != ""
    assert selection.selection_reason != ""


def test_selection_select_with_failover():
    engine = ModelSelectionEngine()
    selection = engine.select_with_failover(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        requirement=CapabilityRequirement(reasoning=8),
        failed_model="gpt-4o",
    )
    assert selection.fallback_occurred
    assert selection.fallback_from == "gpt-4o"
