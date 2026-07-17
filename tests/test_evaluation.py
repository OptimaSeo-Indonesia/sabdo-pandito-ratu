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

from core.advisors.evaluation import AdvisorEvaluator, CRITERIA_DEFINITIONS
from core.models import AdvisorPersona


def test_evaluator_has_all_personas():
    assert len(CRITERIA_DEFINITIONS) == 6


def test_evaluator_get_criteria():
    evaluator = AdvisorEvaluator()
    criteria = evaluator.get_criteria(AdvisorPersona.RATIONAL_ANALYST)
    assert len(criteria) == 4


def test_evaluator_economic_has_five_criteria():
    evaluator = AdvisorEvaluator()
    criteria = evaluator.get_criteria(AdvisorPersona.ECONOMIC)
    assert len(criteria) == 5


def test_evaluator_returns_evaluation():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.HUMANITARIAN,
        question="Test question",
        context={},
    )
    assert result.persona == AdvisorPersona.HUMANITARIAN
    assert len(result.criteria) == 4
    assert result.argument


def test_evaluation_has_concerns():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.DEVILS_ADVOCATE,
        question="Test",
        context={},
    )
    assert isinstance(result.concerns, list)


def test_evaluation_score_range():
    evaluator = AdvisorEvaluator()
    result = evaluator.evaluate(
        persona=AdvisorPersona.RATIONAL_ANALYST,
        question="Test",
        context={},
    )
    assert 0 <= result.overall_score <= 10
