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

from fastapi import APIRouter

from core.advisors.registry import AdvisorRegistry

router = APIRouter(tags=["advisors"])


@router.get("/advisors")
async def list_advisors():
    registry = AdvisorRegistry()
    active = registry.list_active()
    return {
        "advisors": [
            {
                "persona": p.persona.value,
                "name": p.name,
                "description": p.description,
                "provider": p.provider,
                "model": p.model,
                "active": p.active,
            }
            for p in active
        ]
    }


@router.get("/advisors/{persona}")
async def get_advisor(persona: str):
    from core.models import AdvisorPersona

    try:
        p_enum = AdvisorPersona(persona)
    except ValueError:
        return {"error": f"Unknown persona: {persona}"}
    registry = AdvisorRegistry()
    profile = registry.get(p_enum)
    if not profile:
        return {"error": "Advisor not found"}
    return {
        "persona": profile.persona.value,
        "name": profile.name,
        "description": profile.description,
        "system_prompt": profile.system_prompt,
        "provider": profile.provider,
        "model": profile.model,
        "priority_weights": profile.priority_weights,
        "active": profile.active,
    }
