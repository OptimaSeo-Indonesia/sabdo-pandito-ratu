# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import logging
import re
from typing import Protocol

from core.models import (
    AdvisorResponse,
    Claim,
    Contradiction,
    Evidence,
    ProvenanceRecord,
    VerificationResult,
    VerificationStatus,
)

logger = logging.getLogger(__name__)


class EvidenceVerifier(Protocol):
    def verify(
        self,
        claims: list[Claim],
        evidence: list[Evidence],
    ) -> list[VerificationResult]:
        ...

    def extract_claims(
        self,
        responses: list[AdvisorResponse],
    ) -> list[Claim]:
        ...

    def extract_evidence(
        self,
        responses: list[AdvisorResponse],
    ) -> list[Evidence]:
        ...

    def detect_contradictions(
        self,
        results: list[VerificationResult],
    ) -> list[Contradiction]:
        ...


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]\w+", text.lower())
    return set(w for w in words if len(w) > 2)


def _compute_confidence(
    support_ratio: float,
    total_evidence: int,
) -> float:
    if total_evidence == 0:
        return 0.1
    base = support_ratio * 0.8 + min(total_evidence / 5, 1.0) * 0.2
    return round(min(max(base, 0.0), 1.0), 2)


class StructuralEvidenceVerifier:
    def extract_claims(
        self,
        responses: list[AdvisorResponse],
    ) -> list[Claim]:
        claims: list[Claim] = []
        for resp in responses:
            if resp.summary:
                claims.append(Claim(
                    text=resp.summary,
                    source_advisor_id=resp.advisor_id,
                    source_persona=resp.persona,
                    confidence=resp.confidence,
                    extracted_entities=list(_tokenize(resp.summary)),
                    parent_response_id=resp.advisor_id,
                ))
            for i, kp in enumerate(resp.key_points):
                claims.append(Claim(
                    text=kp,
                    source_advisor_id=resp.advisor_id,
                    source_persona=resp.persona,
                    confidence=resp.confidence,
                    extracted_entities=list(_tokenize(kp)),
                    parent_response_id=resp.advisor_id,
                ))
        return claims

    def extract_evidence(
        self,
        responses: list[AdvisorResponse],
    ) -> list[Evidence]:
        evidence: list[Evidence] = []
        for resp in responses:
            for src in resp.data_sources:
                evidence.append(Evidence(
                    text=src,
                    source_ref=src,
                    source_type="data_source",
                    provider=resp.advisor_id,
                ))
        return evidence

    def verify(
        self,
        claims: list[Claim],
        evidence: list[Evidence],
    ) -> list[VerificationResult]:
        if not evidence:
            return [
                VerificationResult(
                    claim_id=c.id,
                    status=VerificationStatus.UNSUPPORTED,
                    support_ratio=0.0,
                    confidence=0.1,
                )
                for c in claims
            ]

        evidence_tokens = [_tokenize(e.text) for e in evidence]
        results: list[VerificationResult] = []

        for claim in claims:
            claim_tokens = _tokenize(claim.text)
            if not claim_tokens:
                results.append(VerificationResult(
                    claim_id=claim.id,
                    status=VerificationStatus.UNSUPPORTED,
                    support_ratio=0.0,
                    confidence=0.1,
                ))
                continue

            matched: list[ProvenanceRecord] = []
            matched_refs: list[str] = []
            unmatched_refs: list[str] = []

            for i, ev_tokens in enumerate(evidence_tokens):
                overlap = claim_tokens & ev_tokens
                if len(overlap) >= 2:
                    score = round(len(overlap) / len(claim_tokens), 2)
                    matched.append(ProvenanceRecord(
                        claim_id=claim.id,
                        evidence_id=evidence[i].id,
                        match_type="keyword",
                        match_score=score,
                    ))
                    matched_refs.append(evidence[i].source_ref)
                else:
                    unmatched_refs.append(evidence[i].source_ref)

            support_ratio = round(len(matched) / len(evidence), 2) if evidence else 0.0

            if len(matched) >= 1:
                status = VerificationStatus.VERIFIED
            elif claim.confidence < 0.3:
                status = VerificationStatus.UNSUPPORTED
            else:
                status = VerificationStatus.UNCERTAIN

            confidence = _compute_confidence(support_ratio, len(evidence))

            results.append(VerificationResult(
                claim_id=claim.id,
                status=status,
                support_ratio=support_ratio,
                provenance=matched,
                matched_evidence=matched_refs,
                unmatched_evidence=unmatched_refs,
                confidence=confidence,
            ))

        return results

    def detect_contradictions(
        self,
        results: list[VerificationResult],
    ) -> list[Contradiction]:
        return []
