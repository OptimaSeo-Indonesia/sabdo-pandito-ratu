# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import json
import os
from pathlib import Path

from core.advisors.personas import default_profiles
from core.models import AdvisorPersona, AdvisorProfile


def load_profiles_from_json(path: str | Path) -> list[AdvisorProfile]:
    """Load advisor profiles from a JSON file. Supports YAML-like JSON config."""
    path = Path(path)
    with open(path) as f:
        data = json.load(f)
    profiles = []
    for item in data if isinstance(data, list) else data.get("advisors", []):
        persona_str = item.pop("persona")
        persona = AdvisorPersona(persona_str)
        profiles.append(AdvisorProfile(persona=persona, **item))
    return profiles


def load_profiles_from_yaml(path: str | Path) -> list[AdvisorProfile]:
    """Load advisor profiles from a YAML file (requires PyYAML)."""
    import yaml
    path = Path(path)
    with open(path) as f:
        data = yaml.safe_load(f)
    profiles = []
    for item in data if isinstance(data, list) else data.get("advisors", []):
        persona_str = item.pop("persona")
        persona = AdvisorPersona(persona_str)
        profiles.append(AdvisorProfile(persona=persona, **item))
    return profiles


def load_profiles_from_env() -> list[AdvisorProfile] | None:
    """Load advisor profiles from SABDO_ADVISOR_CONFIG env var (JSON file path)."""
    config_path = os.getenv("SABDO_ADVISOR_CONFIG")
    if not config_path:
        return None
    path = Path(config_path)
    if not path.exists():
        return None
    if path.suffix in (".yaml", ".yml"):
        return load_profiles_from_yaml(path)
    return load_profiles_from_json(path)


class AdvisorRegistry:
    def __init__(self):
        profiles = default_profiles()
        # Override with external config if available
        external = load_profiles_from_env()
        if external:
            profiles = external
        self._profiles: dict[AdvisorPersona, AdvisorProfile] = {
            p.persona: p for p in profiles
        }

    def list_active(self) -> list[AdvisorProfile]:
        return [p for p in self._profiles.values() if p.active]

    def get(self, persona: AdvisorPersona) -> AdvisorProfile | None:
        return self._profiles.get(persona)

    def get_by_personas(
        self, personas: list[AdvisorPersona]
    ) -> list[AdvisorProfile]:
        return [self._profiles[p] for p in personas if p in self._profiles]

    def register(self, profile: AdvisorProfile) -> None:
        self._profiles[profile.persona] = profile

    def load_file(self, path: str | Path) -> int:
        """Load profiles from a JSON or YAML file. Returns count of profiles loaded."""
        path = Path(path)
        if path.suffix in (".yaml", ".yml"):
            profiles = load_profiles_from_yaml(path)
        else:
            profiles = load_profiles_from_json(path)
        for p in profiles:
            self._profiles[p.persona] = p
        return len(profiles)

    def remove(self, persona: AdvisorPersona) -> None:
        self._profiles.pop(persona, None)

    def update_requirements(
        self, persona: AdvisorPersona, requirements: dict
    ) -> None:
        if persona in self._profiles:
            from core.models import CapabilityRequirement
            self._profiles[persona].capability_requirements = CapabilityRequirement(**requirements)
