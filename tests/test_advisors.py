# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.advisors.personas import default_profiles
from core.advisors.registry import AdvisorRegistry
from core.models import AdvisorPersona


def test_registry_contains_all_personas():
    registry = AdvisorRegistry()
    active = registry.list_active()
    assert len(active) == 6


def test_registry_returns_active():
    registry = AdvisorRegistry()
    active = registry.list_active()
    assert all(a.active for a in active)


def test_registry_get_by_persona():
    registry = AdvisorRegistry()
    profile = registry.get(AdvisorPersona.RATIONAL_ANALYST)
    assert profile is not None
    assert profile.persona == AdvisorPersona.RATIONAL_ANALYST


def test_registry_get_by_personas():
    registry = AdvisorRegistry()
    personas = [AdvisorPersona.HUMANITARIAN, AdvisorPersona.ECONOMIC]
    profiles = registry.get_by_personas(personas)
    assert len(profiles) == 2


def test_registry_register_and_remove():
    registry = AdvisorRegistry()
    from core.models import AdvisorProfile

    new = AdvisorProfile(
        persona=AdvisorPersona.DEVILS_ADVOCATE,
        name="Custom",
        description="Custom",
        system_prompt="Custom prompt",
    )
    registry.register(new)
    gotten = registry.get(AdvisorPersona.DEVILS_ADVOCATE)
    assert gotten is not None
    assert gotten.name == "Custom"
    registry.remove(AdvisorPersona.DEVILS_ADVOCATE)
    assert registry.get(AdvisorPersona.DEVILS_ADVOCATE) is None


def test_update_requirements():
    registry = AdvisorRegistry()
    registry.update_requirements(
        AdvisorPersona.ECONOMIC,
        requirements={"reasoning": 10, "numerical_reasoning": 10},
    )
    profile = registry.get(AdvisorPersona.ECONOMIC)
    assert profile is not None
    assert profile.capability_requirements.reasoning == 10
    assert profile.capability_requirements.numerical_reasoning == 10


def test_default_profiles_have_all_fields():
    profiles = default_profiles()
    for p in profiles:
        assert p.name
        assert p.description
        assert p.system_prompt
        assert p.capability_requirements is not None
        assert p.priority_weights
