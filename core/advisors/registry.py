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

from core.advisors.personas import default_profiles
from core.models import AdvisorPersona, AdvisorProfile


class AdvisorRegistry:
    def __init__(self):
        self._profiles: dict[AdvisorPersona, AdvisorProfile] = {
            p.persona: p for p in default_profiles()
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

    def remove(self, persona: AdvisorPersona) -> None:
        self._profiles.pop(persona, None)

    def set_provider(
        self, persona: AdvisorPersona, provider: str, model: str
    ) -> None:
        if persona in self._profiles:
            self._profiles[persona].provider = provider
            self._profiles[persona].model = model
