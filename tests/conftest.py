# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
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
