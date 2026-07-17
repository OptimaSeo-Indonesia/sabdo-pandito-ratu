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
        provider="custom",
        model="custom-model",
    )
    registry.register(new)
    gotten = registry.get(AdvisorPersona.DEVILS_ADVOCATE)
    assert gotten is not None
    assert gotten.name == "Custom"
    registry.remove(AdvisorPersona.DEVILS_ADVOCATE)
    assert registry.get(AdvisorPersona.DEVILS_ADVOCATE) is None


def test_set_provider():
    registry = AdvisorRegistry()
    registry.set_provider(
        AdvisorPersona.ECONOMIC, provider="ollama", model="llama3"
    )
    profile = registry.get(AdvisorPersona.ECONOMIC)
    assert profile is not None
    assert profile.provider == "ollama"
    assert profile.model == "llama3"


def test_default_profiles_have_all_fields():
    profiles = default_profiles()
    for p in profiles:
        assert p.name
        assert p.description
        assert p.system_prompt
        assert p.provider
        assert p.model
        assert p.priority_weights
