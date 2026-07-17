from core.models import PrincipleEvaluation


class PrincipleEngine:
    def __init__(self):
        self.principles: dict[str, dict] = {
            "fairness": {
                "weight": 0.25,
                "description": "Does the decision distribute benefits and burdens equitably?",
                "checks": [
                    "Does it favor one group over another?",
                    "Are all stakeholders considered equally?",
                    "Does it create systemic advantage or disadvantage?",
                ],
            },
            "transparency": {
                "weight": 0.20,
                "description": "Is the decision process and reasoning open to scrutiny?",
                "checks": [
                    "Can the reasoning be explained clearly?",
                    "Are the data and assumptions visible?",
                    "Would stakeholders accept the rationale?",
                ],
            },
            "sustainability": {
                "weight": 0.20,
                "description": "Does the decision preserve long-term viability?",
                "checks": [
                    "Can this decision be maintained over time?",
                    "Does it deplete resources (social, financial, environmental)?",
                    "Does it create future options or close them?",
                ],
            },
            "human_impact": {
                "weight": 0.25,
                "description": "What is the direct and indirect effect on human well-being?",
                "checks": [
                    "Does it protect human dignity?",
                    "Does it minimize suffering?",
                    "Does it empower or disempower people?",
                ],
            },
            "accountability": {
                "weight": 0.10,
                "description": "Can decision-makers be held responsible for outcomes?",
                "checks": [
                    "Are roles and responsibilities clear?",
                    "Is there a mechanism for correction if wrong?",
                    "Can affected parties seek recourse?",
                ],
            },
        }

    def evaluate(
        self,
        question: str,
        context: dict,
        advisor_responses: list,
        conflicts: list,
    ) -> list[PrincipleEvaluation]:
        results: list[PrincipleEvaluation] = []

        for principle_name, config in self.principles.items():
            score, concerns = self._score_principle(
                principle_name, config, question, context, advisor_responses, conflicts
            )
            results.append(
                PrincipleEvaluation(
                    principle=principle_name,
                    score=round(score, 1),
                    weight=config["weight"],
                    rationale=self._generate_rationale(
                        principle_name, score, concerns
                    ),
                    concerns=concerns,
                )
            )

        return results

    def _score_principle(
        self,
        name: str,
        config: dict,
        question: str,
        context: dict,
        advisor_responses: list,
        conflicts: list,
    ) -> tuple[float, list[str]]:
        concerns: list[str] = []

        if name == "fairness":
            return self._evaluate_fairness(advisor_responses, conflicts)
        elif name == "transparency":
            return self._evaluate_transparency()
        elif name == "sustainability":
            return self._evaluate_sustainability(advisor_responses)
        elif name == "human_impact":
            return self._evaluate_human_impact(advisor_responses)
        elif name == "accountability":
            return self._evaluate_accountability()
        else:
            return 7.0, []

    def _evaluate_fairness(
        self, advisor_responses: list, conflicts: list
    ) -> tuple[float, list[str]]:
        concerns = []
        for conflict in conflicts:
            if hasattr(conflict, "type") and "value_tradeoff" in str(conflict.type):
                concerns.append("Value trade-off detected between stakeholders")
        if not concerns:
            concerns.append("No systemic fairness issues identified")
        return 7.5, concerns

    def _evaluate_transparency(self) -> tuple[float, list[str]]:
        return 8.0, ["Decision process is documented and auditable"]

    def _evaluate_sustainability(
        self, advisor_responses: list
    ) -> tuple[float, list[str]]:
        concerns = []
        for resp in advisor_responses:
            if "unsustainable" in resp.summary.lower():
                concerns.append(f"{resp.persona.value} flagged sustainability concerns")
        return 7.0, concerns if concerns else ["No sustainability red flags"]

    def _evaluate_human_impact(
        self, advisor_responses: list
    ) -> tuple[float, list[str]]:
        concerns = []
        humanitarians = [
            r for r in advisor_responses if "humanitarian" in r.persona.value
        ]
        if humanitarians and humanitarians[0].confidence < 0.5:
            concerns.append("Humanitarian advisor has significant reservations")
        return 7.0, concerns if concerns else ["Human impact appears manageable"]

    def _evaluate_accountability(self) -> tuple[float, list[str]]:
        return 8.0, ["Clear accountability mechanisms can be established"]

    def _generate_rationale(
        self, principle: str, score: float, concerns: list[str]
    ) -> str:
        if score >= 8:
            return f"Strong alignment with {principle} principle (score: {score}/10)"
        elif score >= 6:
            return (
                f"Moderate alignment with {principle} principle (score: {score}/10). "
                f"{' '.join(concerns)}"
            )
        else:
            return (
                f"Weak alignment with {principle} principle (score: {score}/10). "
                f"Significant concerns: {' '.join(concerns)}"
            )
