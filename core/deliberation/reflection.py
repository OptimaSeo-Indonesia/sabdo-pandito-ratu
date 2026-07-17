from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Conflict,
    DeliberationState,
    PrincipleEvaluation,
)


class ReflectionResult:
    def __init__(self) -> None:
        self.consistency_issues: list[str] = []
        self.missing_perspectives: list[str] = []
        self.confidence_adjustment: float = 0.0
        self.reflection_notes: list[str] = []

    def to_dict(self) -> dict:
        return {
            "consistency_issues": self.consistency_issues,
            "missing_perspectives": self.missing_perspectives,
            "confidence_adjustment": self.confidence_adjustment,
            "reflection_notes": self.reflection_notes,
        }


class ReflectionNode:
    """
    Before the final verdict, the system reflects:
    - Are the arguments internally consistent?
    - Are there perspectives that should have been represented but weren't?
    - Does the principle evaluation align with the arguments?
    - Is there sufficient coverage of the problem space?
    """

    ALL_PERSONAS = list(AdvisorPersona)

    def reflect(self, state: DeliberationState) -> dict:
        result = ReflectionResult()

        self._check_perspective_coverage(state, result)
        self._check_argument_consistency(state, result)
        self._check_principle_alignment(state, result)
        self._check_uncertainty_disclosure(state, result)
        self._compute_confidence_adjustment(result)

        return {
            "reflection": result.to_dict(),
            "adjusted_confidence": max(
                0.0,
                min(
                    1.0,
                    self._base_confidence(state) + result.confidence_adjustment,
                ),
            ),
        }

    def _check_perspective_coverage(
        self, state: DeliberationState, result: ReflectionResult
    ) -> None:
        represented = {r.persona for r in state.advisor_responses}
        missing = [p for p in self.ALL_PERSONAS if p not in represented]

        for p in missing:
            result.missing_perspectives.append(
                f"{p.value} perspective was not consulted. "
                f"Consider whether this omission biases the outcome."
            )

        if len(missing) > 2:
            result.reflection_notes.append(
                f"Warning: {len(missing)} of {len(self.ALL_PERSONAS)} "
                f"perspectives are missing. Deliberation may lack diversity."
            )

    def _check_argument_consistency(
        self, state: DeliberationState, result: ReflectionResult
    ) -> None:
        stances = [(r.persona.value, r.stance) for r in state.advisor_responses]
        yes_count = sum(1 for _, s in stances if s in ("yes", "cautious_yes"))
        no_count = sum(1 for _, s in stances if s in ("no", "cautious_no"))

        if yes_count > 0 and no_count > 0:
            yes_personas = [
                p for p, s in stances if s in ("yes", "cautious_yes")
            ]
            no_personas = [
                p for p, s in stances if s in ("no", "cautious_no")
            ]
            result.reflection_notes.append(
                f"Healthy disagreement detected: "
                f"{', '.join(yes_personas)} vs {', '.join(no_personas)}. "
                f"The conflict is legitimate and should be weighed carefully."
            )

        if yes_count == 0 and no_count == 0:
            result.reflection_notes.append(
                "No strong stance detected across advisors. "
                "The council may lack conviction or the question may be poorly framed."
            )

    def _check_principle_alignment(
        self, state: DeliberationState, result: ReflectionResult
    ) -> None:
        low_principles = [
            e
            for e in state.principle_evaluations
            if e.score < 5.0
        ]
        for e in low_principles:
            result.consistency_issues.append(
                f"Principle '{e.principle}' scores {e.score}/10 — "
                f"below the 5.0 threshold. This should be a red flag. {e.rationale}"
            )

        moderate = [
            e
            for e in state.principle_evaluations
            if 5.0 <= e.score < 7.0
        ]
        for e in moderate:
            result.reflection_notes.append(
                f"Principle '{e.principle}' at {e.score}/10 — "
                f"adequate but should be monitored."
            )

    def _check_uncertainty_disclosure(
        self, state: DeliberationState, result: ReflectionResult
    ) -> None:
        if state.context_analysis and state.context_analysis.data_gaps:
            result.reflection_notes.append(
                f"Data gaps identified: {len(state.context_analysis.data_gaps)}. "
                f"Decision confidence should reflect this uncertainty."
            )
            result.confidence_adjustment -= 0.05 * min(
                len(state.context_analysis.data_gaps), 3
            )

    def _compute_confidence_adjustment(
        self, result: ReflectionResult
    ) -> None:
        if result.missing_perspectives:
            result.confidence_adjustment -= 0.05 * min(
                len(result.missing_perspectives), 3
            )
        if result.consistency_issues:
            result.confidence_adjustment -= 0.08 * min(
                len(result.consistency_issues), 3
            )
        result.confidence_adjustment = round(
            max(-0.5, min(0.1, result.confidence_adjustment)), 3
        )

    def _base_confidence(self, state: DeliberationState) -> float:
        if not state.advisor_responses:
            return 0.0
        return sum(r.confidence for r in state.advisor_responses) / len(
            state.advisor_responses
        )
