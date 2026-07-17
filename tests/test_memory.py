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

import pytest

from core.memory.store import CollectiveWisdomMemory
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    DeliberationState,
    WisdomScore,
)


@pytest.mark.asyncio
async def test_memory_save_and_stats():
    memory = CollectiveWisdomMemory()
    state = DeliberationState(question="Test question")
    state.advisor_responses = [
        AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test",
            reasoning="Test",
            confidence=0.8,
        )
    ]
    state.wisdom_score = WisdomScore(
        evidence_quality=80,
        perspective_diversity=70,
        ethical_alignment=85,
        long_term_impact=75,
        uncertainty_handling=60,
        reversibility=90,
    )
    await memory.save_session(state)

    stats = await memory.get_stats()
    assert stats["total_cases"] == 1
    assert stats["avg_confidence"] >= 0


@pytest.mark.asyncio
async def test_memory_record_outcome():
    memory = CollectiveWisdomMemory()
    state = DeliberationState(question="Test")
    await memory.save_session(state)

    stats_before = await memory.get_stats()
    stats_before["cases_with_outcomes"] == 0

    cases = await memory.find_similar_cases("Test")
    if cases:
        await memory.record_outcome(
            case_id=cases[0].case_id,
            outcome="Successful",
            outcome_score=8.0,
            lessons=["Lesson 1", "Lesson 2"],
        )

    stats_after = await memory.get_stats()
    assert stats_after["total_cases"] == 1


@pytest.mark.asyncio
async def test_find_similar_cases():
    memory = CollectiveWisdomMemory()
    state1 = DeliberationState(question="Should we expand to Asia?")
    state2 = DeliberationState(question="Should we expand to Europe?")
    state3 = DeliberationState(question="What color should the logo be?")

    await memory.save_session(state1)
    await memory.save_session(state2)
    await memory.save_session(state3)

    similar = await memory.find_similar_cases("Should we expand to Asia?", top_k=5)
    assert len(similar) >= 1


@pytest.mark.asyncio
async def test_empty_memory_stats():
    memory = CollectiveWisdomMemory()
    stats = await memory.get_stats()
    assert stats["total_cases"] == 0
    assert stats["avg_confidence"] == 0
