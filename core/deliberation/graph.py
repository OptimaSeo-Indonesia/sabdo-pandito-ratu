# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from langgraph.graph import END, StateGraph

from core.advisors.evaluation import AdvisorEvaluator
from core.advisors.registry import AdvisorRegistry
from core.deliberation.reflection import ReflectionNode
from core.evaluation.scorer import WisdomScorer
from core.explainability.reporter import ExplainabilityReporter
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Argument,
    Conflict,
    ConflictType,
    ContextAnalysis,
    DeliberationState,
    SessionStatus,
)
from core.principles.engine import PrincipleEngine
from core.principles.profiles import PrincipleProfileManager
from core.simulation.simulator import ScenarioExplorer


class DeliberationGraph:
    def __init__(
        self,
        registry: AdvisorRegistry | None = None,
        evaluator: AdvisorEvaluator | None = None,
        principle_engine: PrincipleEngine | None = None,
        profile_manager: PrincipleProfileManager | None = None,
        simulator: ScenarioExplorer | None = None,
        reflection: ReflectionNode | None = None,
        scorer: WisdomScorer | None = None,
        reporter: ExplainabilityReporter | None = None,
    ):
        self.registry = registry or AdvisorRegistry()
        self.evaluator = evaluator or AdvisorEvaluator()
        self.principles = principle_engine or PrincipleEngine()
        self.profiles = profile_manager or PrincipleProfileManager()
        self.simulator = simulator or ScenarioExplorer()
        self.reflection = reflection or ReflectionNode()
        self.scorer = scorer or WisdomScorer()
        self.reporter = reporter or ExplainabilityReporter()
        self.graph = self._build()

    def _build(self) -> StateGraph:
        workflow = StateGraph(DeliberationState)

        workflow.add_node("analyze_context", self._step_analyze_context)
        workflow.add_node("generate_perspectives", self._step_perspectives)
        workflow.add_node("collect_arguments", self._step_arguments)
        workflow.add_node("resolve_conflicts", self._step_conflicts)
        workflow.add_node("evaluate_principles", self._step_principles)
        workflow.add_node("explore_scenarios", self._step_scenarios)
        workflow.add_node("reflect", self._step_reflection)
        workflow.add_node("score_wisdom", self._step_scoring)
        workflow.add_node("generate_verdict", self._step_verdict)

        workflow.set_entry_point("analyze_context")
        workflow.add_edge("analyze_context", "generate_perspectives")
        workflow.add_edge("generate_perspectives", "collect_arguments")
        workflow.add_edge("collect_arguments", "resolve_conflicts")
        workflow.add_edge("resolve_conflicts", "evaluate_principles")
        workflow.add_edge("evaluate_principles", "explore_scenarios")
        workflow.add_edge("explore_scenarios", "reflect")
        workflow.add_edge("reflect", "score_wisdom")
        workflow.add_edge("score_wisdom", "generate_verdict")
        workflow.add_edge("generate_verdict", END)

        return workflow.compile()

    async def _step_analyze_context(self, state: DeliberationState) -> dict:
        return {
            "status": SessionStatus.ANALYZING_CONTEXT,
            "context_analysis": ContextAnalysis(
                domain="general",
                stakes="unknown",
                affected_stakeholders=["primary", "secondary"],
                time_sensitivity="moderate",
                key_constraints=[],
                data_gaps=[],
            ).model_dump(),
        }

    async def _step_perspectives(self, state: DeliberationState) -> dict:
        responses: list[AdvisorResponse] = []
        active = self.registry.list_active()

        for profile in active:
            evaluation = self.evaluator.evaluate(
                persona=profile.persona,
                question=state.question,
                context=state.context,
            )
            response = AdvisorResponse(
                advisor_id=f"{profile.persona.value}",
                persona=profile.persona,
                stance="neutral",
                summary=evaluation.argument,
                reasoning=(
                    f"Criterion scores: "
                    f"{', '.join(f'{c.name}={c.score}' for c in evaluation.criteria)}"
                ),
                confidence=round(evaluation.overall_score / 10, 2),
                key_points=[c.rationale for c in evaluation.criteria[:3]],
                data_sources=[],
                assumptions=[],
            )
            responses.append(response)

        return {
            "status": SessionStatus.GENERATING_PERSPECTIVES,
            "advisor_responses": [r.model_dump() for r in responses],
        }

    async def _step_arguments(self, state: DeliberationState) -> dict:
        arguments: list[Argument] = []
        for resp in state.advisor_responses:
            arg = Argument(
                advisor_id=resp.advisor_id if hasattr(resp, 'advisor_id') else resp.get('advisor_id', ''),
                persona=resp.persona if hasattr(resp, 'persona') else resp.get('persona'),
                claim=resp.summary if hasattr(resp, 'summary') else resp.get('summary', ''),
                evidence="",
                reasoning=resp.reasoning if hasattr(resp, 'reasoning') else resp.get('reasoning', ''),
                supports_stance=resp.stance if hasattr(resp, 'stance') else resp.get('stance'),
            )
            arguments.append(arg)
        return {
            "status": SessionStatus.COLLECTING_ARGUMENTS,
            "arguments": [a.model_dump() for a in arguments],
        }

    async def _step_conflicts(self, state: DeliberationState) -> dict:
        conflicts: list[Conflict] = []
        responses = state.advisor_responses

        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                r1, r2 = responses[i], responses[j]
                r1_p = r1.persona if hasattr(r1, 'persona') else AdvisorPersona(r1.get('persona'))
                r2_p = r2.persona if hasattr(r2, 'persona') else AdvisorPersona(r2.get('persona'))
                r1_s = r1.stance if hasattr(r1, 'stance') else r1.get('stance', '')
                r2_s = r2.stance if hasattr(r2, 'stance') else r2.get('stance', '')
                if r1_s != r2_s:
                    conflicts.append(
                        Conflict(
                            type=ConflictType.EXPLICIT_CONFLICT,
                            description=(
                                f"{r1_p.value} ({r1_s}) conflicts with "
                                f"{r2_p.value} ({r2_s})"
                            ),
                            between_personas=[r1_p, r2_p],
                            root_cause="Different value priorities and evaluation frameworks",
                        )
                    )

        return {
            "status": SessionStatus.RESOLVING_CONFLICTS,
            "conflicts": [c.model_dump() for c in conflicts],
        }

    async def _step_principles(self, state: DeliberationState) -> dict:
        from core.models import AdvisorResponse as AR
        responses = [AR(**r) if isinstance(r, dict) else r for r in state.advisor_responses]
        evaluations = self.principles.evaluate(
            question=state.question,
            context=state.context,
            advisor_responses=responses,
            conflicts=state.conflicts,
        )
        profile_name = state.context.get("principle_profile", "balanced") if isinstance(state.context, dict) else "balanced"
        evaluations = self.profiles.apply_weights(profile_name, evaluations)
        return {
            "status": SessionStatus.EVALUATING_PRINCIPLES,
            "principle_evaluations": [e.model_dump() for e in evaluations],
        }

    async def _step_scenarios(self, state: DeliberationState) -> dict:
        from core.models import AdvisorResponse as AR
        responses = [AR(**r) if isinstance(r, dict) else r for r in state.advisor_responses]
        decision = self._extract_tentative_decision(state)
        scenarios = self.simulator.explore(
            question=state.question,
            advisor_responses=responses,
            decision=decision,
        )
        return {
            "status": SessionStatus.EXPLORING_SCENARIOS,
            "scenarios": [s.model_dump() for s in scenarios],
        }

    async def _step_reflection(self, state: DeliberationState) -> dict:
        result = self.reflection.reflect(state)
        return {
            "status": SessionStatus.REFLECTING,
            "reflection": result,
        }

    async def _step_scoring(self, state: DeliberationState) -> dict:
        from core.models import AdvisorResponse as AR
        responses = [AR(**r) if isinstance(r, dict) else r for r in state.advisor_responses]
        state.advisor_responses = responses
        wisdom = self.scorer.compute(state)
        scores = self.scorer.compute_advisor_scores(responses)
        return {
            "status": SessionStatus.SCORING,
            "wisdom_score": wisdom.model_dump(),
            "scores": scores,
        }

    async def _step_verdict(self, state: DeliberationState) -> dict:
        verdict = self.reporter.build_verdict(state)
        return {
            "status": SessionStatus.COMPLETED,
            "verdict": verdict.model_dump(),
        }

    def _extract_tentative_decision(self, state: DeliberationState) -> str:
        stances = [
            r.stance if hasattr(r, 'stance') else r.get('stance', '')
            for r in state.advisor_responses
        ]
        yes_count = sum(1 for s in stances if s in ("yes", "cautious_yes"))
        no_count = sum(1 for s in stances if s in ("no", "cautious_no"))
        if yes_count > no_count:
            return "proceed"
        elif no_count > yes_count:
            return "do_not_proceed"
        return "further_analysis_needed"

    async def run(self, initial_state: DeliberationState) -> DeliberationState:
        result = await self.graph.ainvoke(initial_state)
        return result
