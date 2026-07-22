"""
Minimal reference implementation: Claim → Evidence → VerificationResult.

This file is self-contained (zero dependencies beyond Python stdlib).
Its purpose is to demonstrate the Sabdo Claim Specification v0.1
in a way that can be directly mapped to any programming language.

Usage:  python examples/minimal_verification.py
"""

import json
import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum


# ─── Enums ───────────────────────────────────────────────────────

class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNSUPPORTED = "unsupported"
    CONTRADICTED = "contradicted"
    UNCERTAIN = "uncertain"

    def __str__(self):
        return self.value


class MatchType(str, Enum):
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    LLM_ASSISTED = "llm_assisted"

    def __str__(self):
        return self.value


class SourceType(str, Enum):
    DATA_SOURCE = "data_source"
    ADVISOR_REASONING = "advisor_reasoning"
    EXTERNAL = "external"

    def __str__(self):
        return self.value


# ─── Core Objects ────────────────────────────────────────────────

@dataclass
class Claim:
    id: str
    text: str
    source_advisor_id: str
    source_persona: str
    confidence: float = 0.5
    extracted_entities: list[str] = field(default_factory=list)
    parent_response_id: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class Evidence:
    id: str
    text: str
    source_ref: str = ""
    source_type: str = "unknown"
    provider: str = ""
    timestamp: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class ProvenanceRecord:
    claim_id: str
    evidence_id: str
    match_type: str = "keyword"
    match_score: float = 0.0
    verified_at: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class VerificationResult:
    claim_id: str
    status: str
    support_ratio: float = 0.0
    provenance: list[dict] = field(default_factory=list)
    matched_evidence: list[str] = field(default_factory=list)
    unmatched_evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


# ─── Helper Functions ────────────────────────────────────────────

def new_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tokenize(text: str) -> set[str]:
    """Extract lowercase words of length > 2."""
    words = re.findall(r"[a-zA-Z]\w+", text.lower())
    return set(w for w in words if len(w) > 2)


def compute_confidence(support_ratio: float, total_evidence: int) -> float:
    if total_evidence == 0:
        return 0.1
    base = support_ratio * 0.8 + min(total_evidence / 5, 1.0) * 0.2
    return round(min(max(base, 0.0), 1.0), 2)


# ─── Verification Engine ─────────────────────────────────────────

def verify_claims(
    claims: list[Claim],
    evidence: list[Evidence],
) -> list[VerificationResult]:
    """
    Verify each claim against available evidence using keyword overlap.

    This is the reference algorithm described in the Sabdo Claim Spec v0.1.
    """
    if not evidence:
        return [
            VerificationResult(
                claim_id=c.id,
                status=str(VerificationStatus.UNSUPPORTED),
                support_ratio=0.0,
                confidence=0.1,
            )
            for c in claims
        ]

    evidence_tokens = [tokenize(e.text) for e in evidence]
    results: list[VerificationResult] = []

    for claim in claims:
        claim_tokens = tokenize(claim.text)
        if not claim_tokens:
            results.append(VerificationResult(
                claim_id=claim.id,
                status=str(VerificationStatus.UNSUPPORTED),
                support_ratio=0.0,
                confidence=0.1,
            ))
            continue

        provenance: list[ProvenanceRecord] = []
        matched_refs: list[str] = []
        unmatched_refs: list[str] = []

        for i, ev_tokens in enumerate(evidence_tokens):
            overlap = claim_tokens & ev_tokens
            if len(overlap) >= 2:
                score = round(len(overlap) / len(claim_tokens), 2)
                provenance.append(ProvenanceRecord(
                    claim_id=claim.id,
                    evidence_id=evidence[i].id,
                    match_type=str(MatchType.KEYWORD),
                    match_score=score,
                    verified_at=now_iso(),
                ))
                matched_refs.append(evidence[i].source_ref or evidence[i].text)
            else:
                unmatched_refs.append(evidence[i].source_ref or evidence[i].text)

        support_ratio = round(len(provenance) / len(evidence), 2) if evidence else 0.0

        if len(provenance) >= 1:
            status = VerificationStatus.VERIFIED
        elif claim.confidence < 0.3:
            status = VerificationStatus.UNSUPPORTED
        else:
            status = VerificationStatus.UNCERTAIN

        confidence = compute_confidence(support_ratio, len(evidence))

        results.append(VerificationResult(
            claim_id=claim.id,
            status=str(status),
            support_ratio=support_ratio,
            provenance=[asdict(p) for p in provenance],
            matched_evidence=matched_refs,
            unmatched_evidence=unmatched_refs,
            confidence=confidence,
        ))

    return results


# ─── Main ────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Sabdo Minimal Verification Example")
    print("=" * 60)

    # 1. Create claims from an advisor response
    claims = [
        Claim(
            id=new_id(),
            text="Solar power reduces carbon emissions significantly.",
            source_advisor_id="ra_001",
            source_persona="rational_analyst",
            confidence=0.85,
            extracted_entities=["solar", "power", "reduces", "carbon", "emissions"],
        ),
        Claim(
            id=new_id(),
            text="Solar costs dropped 90% in the last decade.",
            source_advisor_id="ra_001",
            source_persona="rational_analyst",
            confidence=0.92,
            extracted_entities=["solar", "costs", "dropped", "decade"],
        ),
        Claim(
            id=new_id(),
            text="The payback period for solar is under 5 years.",
            source_advisor_id="ra_001",
            source_persona="rational_analyst",
            confidence=0.78,
            extracted_entities=["payback", "period", "solar", "years"],
        ),
    ]

    # 2. Create evidence from data sources
    evidence = [
        Evidence(
            id=new_id(),
            text="IEA 2025: Solar power adoption reduces carbon emissions by 40%.",
            source_ref="IEA Renewables 2025 report",
            source_type=str(SourceType.DATA_SOURCE),
            provider="ra_001",
            timestamp=now_iso(),
        ),
        Evidence(
            id=new_id(),
            text="IRENA 2024: Solar PV costs declined by 90% since 2010.",
            source_ref="IRENA cost study 2024",
            source_type=str(SourceType.DATA_SOURCE),
            provider="ra_001",
            timestamp=now_iso(),
        ),
    ]

    # 3. Run verification
    results = verify_claims(claims, evidence)

    # 4. Print results
    print(f"\nClaims: {len(claims)}")
    for c in claims:
        print(f"  [{c.id[:8]}] {c.text}")

    print(f"\nEvidence: {len(evidence)}")
    for e in evidence:
        print(f"  [{e.id[:8]}] {e.source_ref}")

    print(f"\nVerification Results: {len(results)}")
    for r in results:
        print(f"  [{r.claim_id[:8]}] status={r.status}  "
              f"support_ratio={r.support_ratio}  "
              f"confidence={r.confidence}")
        if r.matched_evidence:
            for m in r.matched_evidence:
                print(f"           matched: {m[:60]}")

    # 5. Show JSON output
    print(f"\n{'=' * 60}")
    print("Sample JSON output (first result):")
    print(results[0].to_json())


if __name__ == "__main__":
    main()
