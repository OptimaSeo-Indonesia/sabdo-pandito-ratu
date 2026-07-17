# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    DeliberationState,
    Verdict,
)


def _to_responses(responses: list) -> list[AdvisorResponse]:
    return [
        AdvisorResponse(**r) if isinstance(r, dict) else r
        for r in responses
    ]


class ExplainabilityReporter:
    def build_verdict(self, state: DeliberationState) -> Verdict:
        decision, confidence = self._determine_decision(state)
        summary = self._build_summary(state, decision)

        return Verdict(
            decision=decision,
            confidence=confidence,
            wisdom_score=state.wisdom_score,
            summary=summary,
            principle_evaluations=state.principle_evaluations,
            scenarios=state.scenarios,
            reflection=state.reflection,
            key_factors=self._extract_key_factors(state),
            supporting_arguments=self._get_supporting(state),
            opposing_arguments=self._get_opposing(state),
            conflicts=[c.model_dump() for c in state.conflicts],
            conflict_resolution=self._resolve_conflicts(state),
            uncertainty_factors=self._get_uncertainties(state),
            alternatives=self._generate_alternatives(state),
            recommendations=self._generate_recommendations(state),
            scores=state.scores,
            model_selections=state.model_selections,
            llm_call_logs=state.llm_call_logs,
        )

    def generate_report(self, state: DeliberationState) -> dict:
        if not state.verdict:
            state.verdict = self.build_verdict(state)
        v = state.verdict

        report: dict = {
            "case": {
                "session_id": str(state.session_id),
                "question": state.question,
                "domain": (
                    state.context_analysis.domain if state.context_analysis else "general"
                ),
            },
            "verdict": {
                "decision": v.decision,
                "confidence": v.confidence,
                "wisdom_score": v.wisdom_score.model_dump() if v.wisdom_score else None,
                "overall_score": v.wisdom_score.overall if v.wisdom_score else None,
            },
            "council_composition": [
                {
                    "persona": r.persona.value,
                    "stance": r.stance,
                    "confidence": r.confidence,
                    "summary": r.summary,
                }
                for r in state.advisor_responses
            ],
            "conflicts": [
                {
                    "type": c.type.value,
                    "between": [p.value for p in c.between_personas],
                    "description": c.description,
                    "root_cause": c.root_cause,
                }
                for c in state.conflicts
            ],
            "principle_evaluations": [
                {
                    "principle": e.principle,
                    "score": e.score,
                    "weight": e.weight,
                    "rationale": e.rationale,
                    "concerns": e.concerns,
                }
                for e in v.principle_evaluations
            ],
            "scenario_explorations": [
                {
                    "name": s.scenario_name,
                    "horizon": s.time_horizon,
                    "probability": s.probability,
                    "assumptions": [a.model_dump() for a in s.assumptions],
                    "uncertainty_level": s.uncertainty_level,
                    "net_impact": s.net_impact,
                }
                for s in v.scenarios
            ],
            "reflection": v.reflection,
            "reasoning": {
                "key_factors": v.key_factors,
                "supporting": v.supporting_arguments,
                "opposing": v.opposing_arguments,
                "conflict_resolution": v.conflict_resolution,
            },
            "uncertainties": v.uncertainty_factors,
            "alternatives": v.alternatives,
            "recommendations": v.recommendations,
        }

        if v.model_selections:
            report["model_selections"] = [
                {
                    "persona": s.persona.value,
                    "selected_adapter": s.selected_adapter,
                    "selected_model": s.selected_model,
                    "selection_reason": s.selection_reason,
                    "fallback_occurred": s.fallback_occurred,
                    "fallback_from": s.fallback_from,
                }
                for s in v.model_selections
            ]

        if v.llm_call_logs:
            report["llm_call_logs"] = [
                {
                    "persona": l.persona.value,
                    "provider": l.provider,
                    "model": l.model,
                    "step": l.step,
                    "latency_ms": l.latency_ms,
                    "success": l.success,
                    "error_message": l.error_message,
                    "retry_count": l.retry_count,
                    "fallback_occurred": l.fallback_occurred,
                }
                for l in v.llm_call_logs
            ]

        return report

    def generate_summary(self, verdict: Verdict) -> str:
        parts = [
            "=" * 60,
            "  SABDO PANDITO RATU — DECISION REPORT",
            "=" * 60,
            "",
            f"  DECISION: {verdict.decision}",
            f"  CONFIDENCE: {verdict.confidence:.0%}",
        ]

        if verdict.model_selections:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  MODEL SELECTION")
            parts.append("-" * 60)
            for s in verdict.model_selections:
                parts.append(
                    f"  {s.persona.value:25s} → {s.selected_adapter}/{s.selected_model}"
                )
                if s.fallback_occurred:
                    parts.append(f"  {'':25s} ⚠ Fallback from {s.fallback_from}")
                parts.append(f"  {'':25s}   Reason: {s.selection_reason}")

        if verdict.wisdom_score:
            parts.append(f"  WISDOM SCORE: {verdict.wisdom_score.overall}/100")
            parts.append("")
            parts.append("  DIMENSION SCORES:")
            parts.append(
                f"    Evidence Quality : {verdict.wisdom_score.evidence_quality:.0f}/100"
            )
            parts.append(
                f"    Perspective Div. : {verdict.wisdom_score.perspective_diversity:.0f}/100"
            )
            parts.append(
                f"    Ethical Alignment: {verdict.wisdom_score.ethical_alignment:.0f}/100"
            )
            parts.append(
                f"    Long-Term Impact : {verdict.wisdom_score.long_term_impact:.0f}/100"
            )
            parts.append(
                f"    Uncertainty Hdl. : {verdict.wisdom_score.uncertainty_handling:.0f}/100"
            )
            parts.append(
                f"    Reversibility    : {verdict.wisdom_score.reversibility:.0f}/100"
            )

        parts.append("")
        parts.append("-" * 60)
        parts.append("  SUMMARY")
        parts.append("-" * 60)
        parts.append(f"  {verdict.summary}")

        if verdict.principle_evaluations:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  PRINCIPLE EVALUATION")
            parts.append("-" * 60)
            for e in verdict.principle_evaluations:
                bar = "█" * int(e.score) + "░" * (10 - int(e.score))
                parts.append(f"  {e.principle:20s} {bar} {e.score:.0f}/10")

        if verdict.reflection:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  REFLECTION")
            parts.append("-" * 60)
            notes = verdict.reflection.get("reflection_notes", [])
            for n in notes:
                parts.append(f"  • {n}")
            missing = verdict.reflection.get("missing_perspectives", [])
            for m in missing:
                parts.append(f"  ⚠ {m}")
            issues = verdict.reflection.get("consistency_issues", [])
            for iss in issues:
                parts.append(f"  ✗ {iss}")

        if verdict.recommendations:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  RECOMMENDATIONS")
            parts.append("-" * 60)
            for r in verdict.recommendations:
                parts.append(f"  → {r}")

        if verdict.uncertainty_factors:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  UNCERTAINTIES & DATA GAPS")
            parts.append("-" * 60)
            for u in verdict.uncertainty_factors:
                parts.append(f"  ⚠ {u}")

        if verdict.alternatives:
            parts.append("")
            parts.append("-" * 60)
            parts.append("  ALTERNATIVES CONSIDERED")
            parts.append("-" * 60)
            for a in verdict.alternatives:
                parts.append(f"  · {a}")

        parts.append("")
        parts.append("=" * 60)

        return "\n".join(parts)

    def _advisors(self, state: DeliberationState) -> list[AdvisorResponse]:
        return _to_responses(state.advisor_responses)

    def _determine_decision(self, state: DeliberationState) -> tuple[str, float]:
        advisors = self._advisors(state)
        if not advisors:
            return "Insufficient perspectives to reach a decision", 0.0

        avg_confidence = sum(
            r.confidence for r in advisors
        ) / len(advisors)

        if state.reflection:
            adj = state.reflection.get("adjusted_confidence")
            if adj is not None:
                avg_confidence = adj

        yes_weight = sum(
            r.confidence
            for r in advisors
            if r.stance in ("yes", "cautious_yes")
        )
        no_weight = sum(
            r.confidence
            for r in advisors
            if r.stance in ("no", "cautious_no")
        )

        total = yes_weight + no_weight
        if total == 0:
            return "Further analysis required", round(avg_confidence, 2)

        if yes_weight > no_weight * 1.5:
            return (
                "Proceed with recommended course of action",
                round(avg_confidence, 2),
            )
        elif yes_weight >= no_weight:
            return (
                "Proceed with caution — monitor key risk factors",
                round(avg_confidence, 2),
            )
        elif no_weight > yes_weight * 1.5:
            return (
                "Do not proceed — risks outweigh benefits",
                round(avg_confidence, 2),
            )
        else:
            return (
                "Defer decision — requires additional data and analysis",
                round(avg_confidence, 2),
            )

    def _build_summary(self, state: DeliberationState, decision: str) -> str:
        total = len(state.advisor_responses)
        conflicts = len(state.conflicts)
        principles_ok = sum(
            1 for e in state.principle_evaluations if e.score >= 7
        )
        total_principles = len(state.principle_evaluations)
        return (
            f"After consulting {total} advisor personas, "
            f"identifying {conflicts} key conflicts, "
            f"and evaluating {total_principles} ethical principles "
            f"({principles_ok}/{total_principles} score >= 7/10), "
            f"the council recommends: {decision}"
        )

    def _extract_key_factors(self, state: DeliberationState) -> list[str]:
        factors = []
        for r in state.advisor_responses:
            factors.extend(r.key_points[:2])
        return factors[:6]

    def _get_supporting(self, state: DeliberationState) -> list[dict]:
        return [
            {
                "persona": r.persona.value,
                "argument": r.summary,
                "confidence": r.confidence,
                "score": r.confidence * 100,
            }
            for r in state.advisor_responses
            if r.stance in ("yes", "cautious_yes")
        ]

    def _get_opposing(self, state: DeliberationState) -> list[dict]:
        return [
            {
                "persona": r.persona.value,
                "argument": r.summary,
                "confidence": r.confidence,
                "score": r.confidence * 100,
            }
            for r in state.advisor_responses
            if r.stance in ("no", "cautious_no")
        ]

    def _resolve_conflicts(self, state: DeliberationState) -> str:
        if not state.conflicts:
            return "No significant conflicts identified — council reaches consensus"
        resolutions = []
        for c in state.conflicts:
            resolution = (
                f"Conflict between {c.between_personas[0].value} and "
                f"{c.between_personas[1].value}: {c.root_cause}. "
                f"Resolved by seeking balanced approach."
            )
            resolutions.append(resolution)
        return " | ".join(resolutions)

    def _get_uncertainties(self, state: DeliberationState) -> list[str]:
        uncertainties = []
        if state.context_analysis:
            uncertainties.extend(state.context_analysis.data_gaps)
        for r in state.advisor_responses:
            for assumption in r.assumptions:
                uncertainties.append(f"Assumption from {r.persona.value}: {assumption}")
        return uncertainties[:5]

    def _generate_alternatives(self, state: DeliberationState) -> list[str]:
        return [
            "Phased approach — implement gradually with checkpoints",
            "Parallel track — run pilot before full commitment",
            "Status quo — maintain current course with adjustments",
        ]

    def _generate_recommendations(self, state: DeliberationState) -> list[str]:
        recommendations = [
            "Validate key assumptions with empirical data before committing",
            "Establish clear metrics to monitor decision outcomes",
            "Set review checkpoints at regular intervals",
        ]
        for e in state.principle_evaluations:
            if e.score < 6:
                recommendations.append(
                    f"Address {e.principle} concerns: {e.concerns[0] if e.concerns else 'review alignment'}"
                )
        if state.conflicts:
            recommendations.append(
                "Resolve identified value conflicts through stakeholder engagement"
            )
        return recommendations
