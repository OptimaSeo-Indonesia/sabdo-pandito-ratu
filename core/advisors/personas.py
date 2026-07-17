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

from core.models import (
    PERSONA_DESCRIPTIONS,
    PERSONA_SYSTEM_PROMPTS,
    AdvisorPersona,
    AdvisorProfile,
)


def default_profiles() -> list[AdvisorProfile]:
    return [
        AdvisorProfile(
            persona=AdvisorPersona.RATIONAL_ANALYST,
            name="Rational Analyst",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.RATIONAL_ANALYST],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.RATIONAL_ANALYST],
            provider="openai",
            model="gpt-4-turbo",
            priority_weights={"evidence": 0.4, "logic": 0.4, "data": 0.2},
        ),
        AdvisorProfile(
            persona=AdvisorPersona.HUMANITARIAN,
            name="Humanitarian Advisor",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.HUMANITARIAN],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.HUMANITARIAN],
            provider="anthropic",
            model="claude-3-opus-20240229",
            priority_weights={"human_impact": 0.5, "fairness": 0.3, "dignity": 0.2},
        ),
        AdvisorProfile(
            persona=AdvisorPersona.ECONOMIC,
            name="Economic Advisor",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.ECONOMIC],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.ECONOMIC],
            provider="openai",
            model="gpt-4-turbo",
            priority_weights={
                "cost_efficiency": 0.3,
                "sustainability": 0.3,
                "growth": 0.2,
                "risk": 0.2,
            },
        ),
        AdvisorProfile(
            persona=AdvisorPersona.LEGAL,
            name="Legal Advisor",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.LEGAL],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.LEGAL],
            provider="anthropic",
            model="claude-3-opus-20240229",
            priority_weights={
                "compliance": 0.4,
                "liability": 0.3,
                "regulation": 0.3,
            },
        ),
        AdvisorProfile(
            persona=AdvisorPersona.DEVILS_ADVOCATE,
            name="Devil's Advocate",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.DEVILS_ADVOCATE],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.DEVILS_ADVOCATE],
            provider="ollama",
            model="llama3",
            priority_weights={
                "edge_cases": 0.4,
                "assumptions": 0.3,
                "failure_modes": 0.3,
            },
        ),
        AdvisorProfile(
            persona=AdvisorPersona.LONG_TERM_STRATEGIST,
            name="Long-Term Strategist",
            description=PERSONA_DESCRIPTIONS[AdvisorPersona.LONG_TERM_STRATEGIST],
            system_prompt=PERSONA_SYSTEM_PROMPTS[AdvisorPersona.LONG_TERM_STRATEGIST],
            provider="anthropic",
            model="claude-3-opus-20240229",
            priority_weights={
                "systemic_impact": 0.3,
                "second_order": 0.3,
                "horizon_10y": 0.4,
            },
        ),
    ]
