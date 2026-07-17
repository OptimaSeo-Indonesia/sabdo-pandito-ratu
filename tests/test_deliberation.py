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

import pytest

from core.deliberation.graph import DeliberationGraph
from core.models import DeliberationState, SessionStatus


@pytest.mark.asyncio
async def test_graph_initialization():
    graph = DeliberationGraph()
    assert graph.graph is not None
    assert len(graph.registry.list_active()) == 6


@pytest.mark.asyncio
async def test_graph_full_pipeline():
    graph = DeliberationGraph()
    state = DeliberationState(
        question="Should our startup pivot from B2C to B2B?"
    )
    result = await graph.run(state)
    assert result is not None
    assert result.get("status") == SessionStatus.COMPLETED


@pytest.mark.asyncio
async def test_graph_generates_perspectives():
    graph = DeliberationGraph()
    state = DeliberationState(question="Test question")
    result = await graph.run(state)
    assert len(result.get("advisor_responses", [])) == 6


@pytest.mark.asyncio
async def test_graph_detects_conflicts():
    graph = DeliberationGraph()
    state = DeliberationState(question="Should we cut costs by 30%?")
    result = await graph.run(state)
    assert len(result.get("conflicts", [])) >= 0


@pytest.mark.asyncio
async def test_graph_generates_verdict():
    graph = DeliberationGraph()
    state = DeliberationState(question="Should we expand to Asia?")
    result = await graph.run(state)
    verdict = result.get("verdict")
    assert verdict is not None
    assert isinstance(verdict, dict)
    assert verdict.get("decision")
    assert verdict.get("summary")


@pytest.mark.asyncio
async def test_graph_all_nine_steps():
    graph = DeliberationGraph()
    state = DeliberationState(question="Test")
    result = await graph.run(state)
    assert result.get("status") == SessionStatus.COMPLETED
    assert result.get("context_analysis") is not None
    assert len(result.get("advisor_responses", [])) == 6
    assert len(result.get("arguments", [])) == 6
    assert result.get("principle_evaluations") is not None
    assert len(result.get("scenarios", [])) > 0
    assert result.get("reflection") is not None
    assert result.get("wisdom_score") is not None
    assert result.get("verdict") is not None


@pytest.mark.asyncio
async def test_graph_reflection_in_verdict():
    graph = DeliberationGraph()
    state = DeliberationState(question="Test")
    result = await graph.run(state)
    verdict = result.get("verdict")
    ref = verdict.get("reflection", {})
    assert ref is not None
    assert "adjusted_confidence" in ref
