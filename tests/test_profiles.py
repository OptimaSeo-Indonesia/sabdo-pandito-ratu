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

from core.principles.profiles import (
    PRINCIPLE_PROFILES,
    PrincipleProfileManager,
    PrincipleWeights,
)


def test_default_profiles_available():
    assert "balanced" in PRINCIPLE_PROFILES
    assert "public_policy" in PRINCIPLE_PROFILES
    assert "startup" in PRINCIPLE_PROFILES
    assert "healthcare" in PRINCIPLE_PROFILES
    assert "personal" in PRINCIPLE_PROFILES


def test_weights_normalize_to_one():
    weights = PrincipleWeights()
    normalized = weights.normalized()
    total = sum(normalized.values())
    assert round(total, 2) == 1.0


def test_profile_manager_get():
    mgr = PrincipleProfileManager()
    profile = mgr.get("public_policy")
    assert profile.name == "Public Policy"
    assert profile.weights.fairness == 0.30
    assert profile.weights.transparency == 0.30


def test_profile_manager_default_to_balanced():
    mgr = PrincipleProfileManager()
    profile = mgr.get("nonexistent")
    assert profile.name == "Balanced Decision"


def test_profile_manager_list():
    mgr = PrincipleProfileManager()
    profiles = mgr.list()
    assert len(profiles) == 5


def test_healthcare_profile_emphasizes_human_impact():
    mgr = PrincipleProfileManager()
    profile = mgr.get("healthcare")
    assert profile.weights.human_impact == 0.35
    assert profile.weights.sustainability == 0.10


def test_startup_profile_emphasizes_accountability():
    mgr = PrincipleProfileManager()
    profile = mgr.get("startup")
    assert profile.weights.accountability == 0.30


def test_apply_weights_modifies_evaluations():
    from core.models import PrincipleEvaluation

    mgr = PrincipleProfileManager()
    evals = [
        PrincipleEvaluation(
            principle="fairness", score=8.0, weight=0.20, rationale="Test"
        ),
        PrincipleEvaluation(
            principle="sustainability",
            score=7.0,
            weight=0.20,
            rationale="Test",
        ),
    ]
    result = mgr.apply_weights("public_policy", evals)
    fairness = [e for e in result if e.principle == "fairness"][0]
    sustainability = [e for e in result if e.principle == "sustainability"][0]
    assert fairness.weight == 0.30
    assert sustainability.weight == 0.15
