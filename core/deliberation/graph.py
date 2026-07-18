# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import logging
from datetime import datetime, timezone

from langgraph.graph import END, StateGraph

from core.advisors.evaluation import AdvisorEvaluator
from core.advisors.registry import AdvisorRegistry
from core.deliberation.analyzer import ContextAnalyzer
from core.deliberation.reflection import ReflectionNode
from core.evaluation.scorer import WisdomScorer
from core.explainability.reporter import ExplainabilityReporter
from core.inference.registry import InferenceRegistry
from core.inference.selection import BackendSelector
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Argument,
    Conflict,
    ConflictType,
    ContextAnalysis,
    DeliberationState,
    DeliberationStep,
    SessionStatus,
)
from core.principles.engine import PrincipleEngine
from core.principles.profiles import PrincipleProfileManager
from core.simulation.simulator import ScenarioExplorer

logger = logging.getLogger(__name__)

STEP_NAMES = [
    "analyze_context",
    "generate_perspectives",
    "collect_arguments",
    "resolve_conflicts",
    "evaluate_principles",
    "explore_scenarios",
    "reflect",
    "score_wisdom",
    "generate_verdict",
]


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
        inference_registry: InferenceRegistry | None = None,
        selection_engine: BackendSelector | None = None,
        analyzer: ContextAnalyzer | None = None,
        mode: str = "standard",
    ):
        if mode not in ("dry_run", "standard", "full_llm"):
            raise ValueError(f"Unknown mode '{mode}'. Use 'dry_run', 'standard', or 'full_llm'.")
        self.mode = mode
        self.registry = registry or AdvisorRegistry()
        self.evaluator = evaluator or AdvisorEvaluator()
        self.principles = principle_engine or PrincipleEngine()
        self.profiles = profile_manager or PrincipleProfileManager()
        self.simulator = simulator or ScenarioExplorer()
        self.reflection = reflection or ReflectionNode()
        self.scorer = scorer or WisdomScorer()
        self.reporter = reporter or ExplainabilityReporter()
        self.analyzer = analyzer or ContextAnalyzer()
        self._inference_registry = inference_registry or InferenceRegistry()
        self._selection_engine = selection_engine or BackendSelector(
            registry=self._inference_registry,
        )
        self._has_adapters = bool(self._inference_registry.list_available())
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

    def _track_step(self, state: DeliberationState, name: str) -> dict:
        now = datetime.now(timezone.utc)
        steps = list(state.steps)
        found = False
        for s in steps:
            if s.name == name:
                s.status = "completed"
                s.started_at = s.started_at or now
                s.completed_at = now
                found = True
                break
        if not found:
            step = DeliberationStep(name=name, status="completed", started_at=now, completed_at=now)
            steps.append(step)
        completed = len([s for s in steps if s.status == "completed"])
        return {
            "steps": [s.model_dump() for s in steps],
            "current_step": name if completed < 9 else None,
            "steps_completed": completed,
            "steps_total": 9,
            "events": list(state.events) + [
                {"type": "step_start", "step": name, "timestamp": now.isoformat()},
                {"type": "step_complete", "step": name, "timestamp": now.isoformat()},
            ],
        }

    async def _step_analyze_context(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "analyze_context")
        analysis = self.analyzer.analyze(state.question, state.context)
        return {
            **step_updates,
            "status": SessionStatus.ANALYZING_CONTEXT,
            "context_analysis": analysis.model_dump(),
        }

    async def _step_perspectives(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "generate_perspectives")
        responses: list[AdvisorResponse] = []
        active = self.registry.list_active()
        selections: list = []
        call_logs: list = []

        if self.mode == "dry_run":
            logger.info("Dry-run mode — zero LLM calls, pure algorithmic pipeline")
            for profile in active:
                self._fallback_response(profile, state, responses)
        elif self.mode == "full_llm" and not self._has_adapters:
            raise RuntimeError(
                "full_llm mode requires at least one inference adapter, but none are available."
            )
        elif self._has_adapters:
            for profile in active:
                selection = self._selection_engine.select(
                    persona=profile.persona,
                    requirement=profile.capability_requirements,
                )
                selections.append(selection)
                if not selection.selected_adapter:
                    if self.mode == "full_llm":
                        raise RuntimeError(
                            f"No adapter found for {profile.persona.value} in full_llm mode."
                        )
                    logger.warning(
                        "No adapter for %s, using simulated fallback",
                        profile.persona.value,
                    )
                    self._fallback_response(profile, state, responses)
                    continue
                try:
                    adapter = self._inference_registry.get(
                        selection.selected_adapter
                    )
                    if adapter is None:
                        if self.mode == "full_llm":
                            raise RuntimeError(
                                f"Adapter '{selection.selected_adapter}' not found in registry (full_llm mode)."
                            )
                        self._fallback_response(profile, state, responses)
                        continue
                    perspective, log = await self._selection_engine.call_with_logging(
                        persona=profile.persona,
                        step="perspective",
                        adapter=adapter,
                        method_name="generate_perspective",
                        advisor_id=profile.persona.value,
                        system_prompt=profile.system_prompt,
                        question=state.question,
                        context=state.context,
                        model=selection.selected_model,
                    )
                    responses.append(perspective)
                    call_logs.append(log)
                    self._selection_engine.record_call_outcome(
                        adapter_id=selection.selected_adapter,
                        success=True,
                        latency_ms=log.latency_ms or 0,
                        wisdom_contribution=perspective.confidence,
                    )
                except Exception as exc:
                    if self.mode == "full_llm":
                        raise
                    logger.warning(
                        "Inference call failed for %s, simulated fallback: %s",
                        profile.persona.value, exc,
                    )
                    self._selection_engine.record_call_outcome(
                        adapter_id=selection.selected_adapter,
                        success=False,
                        latency_ms=0,
                    )
                    self._fallback_response(profile, state, responses)
        else:
            logger.info("No inference adapters available — using simulated evaluations")
            for profile in active:
                self._fallback_response(profile, state, responses)

        return {
            **step_updates,
            "status": SessionStatus.GENERATING_PERSPECTIVES,
            "advisor_responses": [r.model_dump() for r in responses],
            "model_selections": [s.model_dump() for s in selections],
            "llm_call_logs": [l.model_dump() for l in call_logs],
        }

    def _fallback_response(
        self,
        profile,
        state: DeliberationState,
        responses: list[AdvisorResponse],
    ) -> None:
        evaluation = self.evaluator.evaluate(
            persona=profile.persona,
            question=state.question,
            context=state.context,
        )
        response = AdvisorResponse(
            advisor_id=f"{profile.persona.value}",
            persona=profile.persona,
            stance=evaluation.stance,
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

    async def _step_arguments(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "collect_arguments")
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
            **step_updates,
            "status": SessionStatus.COLLECTING_ARGUMENTS,
            "arguments": [a.model_dump() for a in arguments],
        }

    async def _step_conflicts(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "resolve_conflicts")
        conflicts: list[Conflict] = []
        responses = state.advisor_responses

        def _get(obj, attr, default=None):
            return getattr(obj, attr, None) if not isinstance(obj, dict) else obj.get(attr, default)

        # Step 1: Detect stance-based explicit conflicts
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                r1, r2 = responses[i], responses[j]
                r1_p = _get(r1, 'persona')
                r2_p = _get(r2, 'persona')
                r1_s = _get(r1, 'stance', '')
                r2_s = _get(r2, 'stance', '')
                if r1_s and r2_s and r1_s != r2_s:
                    is_yes1 = r1_s in ("yes", "cautious_yes")
                    is_yes2 = r2_s in ("yes", "cautious_yes")
                    is_no1 = r1_s in ("no", "cautious_no")
                    is_no2 = r2_s in ("no", "cautious_no")

                    if (is_yes1 and is_no2) or (is_no1 and is_yes2):
                        conflicts.append(Conflict(
                            type=ConflictType.EXPLICIT_CONFLICT,
                            description=(
                                f"{r1_p.value if hasattr(r1_p, 'value') else r1_p} ({r1_s}) "
                                f"conflicts with "
                                f"{r2_p.value if hasattr(r2_p, 'value') else r2_p} ({r2_s})"
                            ),
                            between_personas=[r1_p, r2_p],
                            root_cause="Opposing stances on the core question",
                        ))
                    elif not ((is_yes1 and is_yes2) or (is_no1 and is_no2)):
                        conflicts.append(Conflict(
                            type=ConflictType.NUANCE_DIFFERENCE,
                            description=(
                                f"{r1_p.value if hasattr(r1_p, 'value') else r1_p} ({r1_s}) vs "
                                f"{r2_p.value if hasattr(r2_p, 'value') else r2_p} ({r2_s})"
                            ),
                            between_personas=[r1_p, r2_p],
                            root_cause="Different degrees of certainty or caution",
                        ))

        # Step 2: Detect incompatible assumptions
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                r1, r2 = responses[i], responses[j]
                r1_assumptions = _get(r1, 'assumptions', [])
                r2_assumptions = _get(r2, 'assumptions', [])
                if r1_assumptions and r2_assumptions:
                    for a1 in r1_assumptions:
                        for a2 in r2_assumptions:
                            if self._assumptions_conflict(a1, a2):
                                r1_p = _get(r1, 'persona')
                                r2_p = _get(r2, 'persona')
                                conflicts.append(Conflict(
                                    type=ConflictType.INCOMPATIBLE_ASSUMPTION,
                                    description=f"Assumption conflict: \"{a1}\" vs \"{a2}\"",
                                    between_personas=[r1_p, r2_p],
                                    root_cause=f"Incompatible underlying assumptions",
                                ))

        # Step 3: Detect consensus (all same stance)
        stances = [_get(r, 'stance', '') for r in responses]
        unique_stances = set(s for s in stances if s)
        if len(unique_stances) == 1:
            conflicts.append(Conflict(
                type=ConflictType.CONSENSUS,
                description=f"All advisors agree: {list(unique_stances)[0]}",
                between_personas=[_get(r, 'persona') for r in responses],
                root_cause="Unified assessment across all perspectives",
            ))

        return {
            **step_updates,
            "status": SessionStatus.RESOLVING_CONFLICTS,
            "conflicts": [c.model_dump() for c in conflicts],
        }

    def _assumptions_conflict(self, a1: str, a2: str) -> bool:
        a1_lower = a1.lower()
        a2_lower = a2.lower()
        negation_pairs = [
            ("not", "is"), ("cannot", "can"), ("will not", "will"),
            ("should not", "should"), ("no need", "need"),
            ("low risk", "high risk"), ("expensive", "cheap"),
            ("fast", "slow"), ("short", "long"),
        ]
        for neg, pos in negation_pairs:
            if (neg in a1_lower and pos in a2_lower) or (pos in a1_lower and neg in a2_lower):
                return True
        return False

    async def _step_principles(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "evaluate_principles")
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

        # Detect value tradeoffs from principle evaluations
        updated_conflicts = [c.model_dump() if hasattr(c, 'model_dump') else c for c in state.conflicts]
        high_scores = [e for e in evaluations if e.score >= 7]
        low_scores = [e for e in evaluations if e.score < 5]
        if high_scores and low_scores:
            high_principles = ", ".join(e.principle for e in high_scores)
            low_principles = ", ".join(e.principle for e in low_scores)
            value_conflict = Conflict(
                type=ConflictType.VALUE_TRADEOFF,
                description=f"Tradeoff between {high_principles} (high) and {low_principles} (low)",
                between_personas=[AdvisorPersona.RATIONAL_ANALYST, AdvisorPersona.HUMANITARIAN],
                root_cause="Inherent value tension between competing ethical principles",
            )
            updated_conflicts.append(value_conflict.model_dump())

        return {
            **step_updates,
            "status": SessionStatus.EVALUATING_PRINCIPLES,
            "principle_evaluations": [e.model_dump() for e in evaluations],
            "conflicts": updated_conflicts,
        }

    async def _step_scenarios(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "explore_scenarios")
        from core.models import AdvisorResponse as AR
        responses = [AR(**r) if isinstance(r, dict) else r for r in state.advisor_responses]
        decision = self._extract_tentative_decision(state)
        scenarios = self.simulator.explore(
            question=state.question,
            advisor_responses=responses,
            decision=decision,
        )
        return {
            **step_updates,
            "status": SessionStatus.EXPLORING_SCENARIOS,
            "scenarios": [s.model_dump() for s in scenarios],
        }

    async def _step_reflection(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "reflect")
        result = self.reflection.reflect(state)
        return {
            **step_updates,
            "status": SessionStatus.REFLECTING,
            "reflection": result,
        }

    async def _step_scoring(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "score_wisdom")
        from core.models import AdvisorResponse as AR
        responses = [AR(**r) if isinstance(r, dict) else r for r in state.advisor_responses]
        state.advisor_responses = responses
        wisdom = self.scorer.compute(state)
        scores = self.scorer.compute_advisor_scores(responses)
        return {
            **step_updates,
            "status": SessionStatus.SCORING,
            "wisdom_score": wisdom.model_dump(),
            "scores": scores,
        }

    async def _step_verdict(self, state: DeliberationState) -> dict:
        step_updates = self._track_step(state, "generate_verdict")
        verdict = self.reporter.build_verdict(state)
        return {
            **step_updates,
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
