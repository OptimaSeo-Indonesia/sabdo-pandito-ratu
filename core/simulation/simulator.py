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

from core.models import (
    AdvisorResponse,
    ScenarioAssumption,
    ScenarioExploration,
)


class ScenarioExplorer:
    HORIZONS = ["6 months", "2 years", "5 years", "10 years"]

    def explore(
        self,
        question: str,
        advisor_responses: list[AdvisorResponse],
        decision: str,
    ) -> list[ScenarioExploration]:
        scenarios: list[ScenarioExploration] = []

        for horizon in self.HORIZONS:
            for bias in ["optimistic", "pessimistic", "most_likely"]:
                scenario = self._build_scenario(
                    horizon, decision, advisor_responses, bias
                )
                scenarios.append(scenario)

        return scenarios

    def _build_scenario(
        self,
        horizon: str,
        decision: str,
        advisor_responses: list[AdvisorResponse],
        bias: str,
    ) -> ScenarioExploration:
        assumptions = self._generate_assumptions(horizon, bias, advisor_responses)

        base_prob = self._base_probability(advisor_responses, bias)
        horizon_factor = self._horizon_confidence(horizon)
        probability = round(base_prob * horizon_factor, 2)

        uncertainty = self._uncertainty_level(horizon, bias)
        positives = self._positive_outcomes(horizon, bias)
        negatives = self._negative_outcomes(horizon, bias)
        net = self._net_impact(advisor_responses, horizon, bias)

        return ScenarioExploration(
            scenario_name=f"{bias}_{horizon.replace(' ', '_')}",
            time_horizon=horizon,
            probability=probability,
            assumptions=assumptions,
            uncertainty_level=uncertainty,
            positive_outcomes=positives,
            negative_outcomes=negatives,
            net_impact=net,
        )

    def _generate_assumptions(
        self, horizon: str, bias: str, responses: list[AdvisorResponse]
    ) -> list[ScenarioAssumption]:
        assumptions = [
            ScenarioAssumption(
                description="Existing market conditions remain relatively stable",
                confidence=0.7 if "6 months" in horizon else 0.3,
            ),
        ]
        if bias == "optimistic":
            assumptions.append(
                ScenarioAssumption(
                    description="Positive adoption trends continue",
                    confidence=0.6,
                )
            )
        elif bias == "pessimistic":
            assumptions.append(
                ScenarioAssumption(
                    description="Adverse conditions materialize",
                    confidence=0.5,
                )
            )
        return assumptions

    def _base_probability(
        self, responses: list[AdvisorResponse], bias: str
    ) -> float:
        positive = sum(1 for r in responses if r.confidence > 0.6)
        negative = sum(1 for r in responses if r.confidence < 0.4)
        base = 0.5 + (positive - negative) * 0.05
        if bias == "optimistic":
            base = min(base + 0.15, 0.95)
        elif bias == "pessimistic":
            base = max(base - 0.15, 0.05)
        return max(0.0, min(1.0, base))

    def _horizon_confidence(self, horizon: str) -> float:
        if "10 years" in horizon:
            return 0.50
        elif "5 years" in horizon:
            return 0.65
        elif "2 years" in horizon:
            return 0.80
        return 0.90

    def _uncertainty_level(self, horizon: str, bias: str) -> str:
        if "10 years" in horizon:
            return "high"
        elif "5 years" in horizon and bias != "most_likely":
            return "high"
        elif "5 years" in horizon:
            return "medium"
        elif "2 years" in horizon and bias == "pessimistic":
            return "medium"
        return "low"

    def _positive_outcomes(self, horizon: str, bias: str) -> list[str]:
        outcomes = [f"Decision creates measurable value in {horizon}"]
        if bias in ("optimistic", "most_likely"):
            outcomes.append("Early indicators validate the decision direction")
            if "10 years" in horizon:
                outcomes.append("Strategic advantages compound over time")
        return outcomes

    def _negative_outcomes(self, horizon: str, bias: str) -> list[str]:
        outcomes = [f"Unforeseen consequences may emerge in {horizon}"]
        if bias in ("pessimistic", "most_likely"):
            outcomes.append("Initial costs or disruption occur before benefits")
            if "10 years" in horizon:
                outcomes.append("Predictive confidence is inherently limited")
        return outcomes

    def _net_impact(
        self, responses: list[AdvisorResponse], horizon: str, bias: str
    ) -> float:
        positive = sum(1 for r in responses if r.confidence > 0.6)
        negative = sum(1 for r in responses if r.confidence < 0.4)
        raw = positive - negative
        factor = self._horizon_confidence(horizon)
        bias_mod = {"optimistic": 1.5, "pessimistic": -1.5, "most_likely": 0.0}[
            bias
        ]
        net = (raw * factor * 2) + bias_mod
        return round(max(-10, min(10, net)), 1)
