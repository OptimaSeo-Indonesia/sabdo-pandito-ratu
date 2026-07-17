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


@pytest.fixture
def sample_question() -> str:
    return "Should our startup pivot from B2C to B2B?"


@pytest.fixture
def sample_context() -> dict:
    return {
        "industry": "edtech",
        "region": "SEA",
        "company_stage": "seed",
        "metrics": {"mrr": 5000, "churn_rate": 0.12, "cac": 45, "ltv": 180},
    }
