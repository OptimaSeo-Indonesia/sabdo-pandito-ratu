# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
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
