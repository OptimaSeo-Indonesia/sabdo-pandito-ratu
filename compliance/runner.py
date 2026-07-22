"""
Sabdo Compliance Test Runner

Language-agnostic compliance testing via JSON interchange.
Reads test_*_input.json → runs verification → compares with test_*_expected.json.
"""

import json
import os
import sys
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ─── Standalone verification (same algorithm as examples/minimal_verification.py) ───

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

@dataclass
class ProvenanceRecord:
    claim_id: str
    evidence_id: str
    match_type: str = "keyword"
    match_score: float = 0.0
    verified_at: str = ""

@dataclass
class VerificationResult:
    claim_id: str
    status: str
    support_ratio: float = 0.0
    provenance: list[dict] = field(default_factory=list)
    matched_evidence: list[str] = field(default_factory=list)
    unmatched_evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]\w+", text.lower())
    return set(w for w in words if len(w) > 2)

def compute_confidence(support_ratio: float, total_evidence: int) -> float:
    if total_evidence == 0:
        return 0.1
    base = support_ratio * 0.8 + min(total_evidence / 5, 1.0) * 0.2
    return round(min(max(base, 0.0), 1.0), 2)

def verify_claims(claims: list[dict], evidence: list[dict]) -> list[dict]:
    if not evidence:
        return [
            asdict(VerificationResult(
                claim_id=c["id"],
                status=str(VerificationStatus.UNSUPPORTED),
                support_ratio=0.0,
                matched_evidence=[],
                unmatched_evidence=[],
                confidence=0.1,
            ))
            for c in claims
        ]

    evidence_tokens = [tokenize(e["text"]) for e in evidence]
    results: list[dict] = []

    for claim in claims:
        claim_tokens = tokenize(claim.get("text", ""))
        if not claim_tokens:
            results.append(asdict(VerificationResult(
                claim_id=claim["id"],
                status=str(VerificationStatus.UNSUPPORTED),
                support_ratio=0.0,
                matched_evidence=[],
                unmatched_evidence=[],
                confidence=0.1,
            )))
            continue

        provenance: list[ProvenanceRecord] = []
        matched_refs: list[str] = []
        unmatched_refs: list[str] = []

        for i, ev_tokens in enumerate(evidence_tokens):
            overlap = claim_tokens & ev_tokens
            if len(overlap) >= 2:
                score = round(len(overlap) / len(claim_tokens), 2)
                provenance.append(ProvenanceRecord(
                    claim_id=claim["id"],
                    evidence_id=evidence[i]["id"],
                    match_type=str(MatchType.KEYWORD),
                    match_score=score,
                    verified_at=now_iso(),
                ))
                matched_refs.append(evidence[i].get("source_ref", evidence[i].get("text", "")))
            else:
                unmatched_refs.append(evidence[i].get("source_ref", evidence[i].get("text", "")))

        support_ratio = round(len(provenance) / len(evidence), 2) if evidence else 0.0
        conf = claim.get("confidence", 0.5)

        if len(provenance) >= 1:
            status = VerificationStatus.VERIFIED
        elif conf < 0.3:
            status = VerificationStatus.UNSUPPORTED
        else:
            status = VerificationStatus.UNCERTAIN

        confidence = compute_confidence(support_ratio, len(evidence))

        results.append(asdict(VerificationResult(
            claim_id=claim["id"],
            status=str(status),
            support_ratio=support_ratio,
            provenance=[asdict(p) for p in provenance],
            matched_evidence=matched_refs,
            unmatched_evidence=unmatched_refs,
            confidence=confidence,
        )))

    return results


# ─── Compliance Runner ───────────────────────────────────────────

TEST_DIR = os.path.join(os.path.dirname(__file__), "tests")


def find_test_cases() -> list[str]:
    """Find all test case prefixes by looking for *_input.json."""
    seen: set[str] = set()
    for f in sorted(os.listdir(TEST_DIR)):
        if f.endswith("_input.json"):
            seen.add(f.replace("_input.json", ""))
    return sorted(seen)


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def run_test(test_prefix: str, verbose: bool = False) -> tuple[bool, str]:
    input_path = os.path.join(TEST_DIR, f"{test_prefix}_input.json")
    expected_path = os.path.join(TEST_DIR, f"{test_prefix}_expected.json")

    if not os.path.exists(input_path):
        return False, f"MISSING: {test_prefix}_input.json"

    data = load_json(input_path)
    expected = load_json(expected_path) if os.path.exists(expected_path) else {}

    results = verify_claims(data.get("claims", []), data.get("evidence", []))
    expected_results = expected.get("results", [])

    if len(results) != len(expected_results):
        return (
            False,
            f"Result count mismatch: got {len(results)}, expected {len(expected_results)}",
        )

    for i, (got, exp) in enumerate(zip(results, expected_results)):
        if got["claim_id"] != exp.get("claim_id", got["claim_id"]):
            return False, (
                f"Result {i}: claim_id mismatch: got {got['claim_id']}, "
                f"expected {exp.get('claim_id', '(missing)')}"
            )
        exp_status = exp.get("status")
        if exp_status and got["status"] != exp_status:
            return False, (
                f"Claim {got['claim_id']}: status={got['status']}, "
                f"expected {exp_status}"
            )
        exp_matched = exp.get("matched_evidence", [])
        if exp_matched and set(got["matched_evidence"]) != set(exp_matched):
            return False, (
                f"Claim {got['claim_id']}: matched={got['matched_evidence']}, "
                f"expected {exp_matched}"
            )

    if verbose:
        print(f"\n  Results for {test_prefix}:")
        for r in results:
            print(f"    [{r['claim_id']}] {r['status']}  "
                  f"ratio={r['support_ratio']}  conf={r['confidence']}")

    return True, ""


def main() -> int:
    tests = find_test_cases()

    if not tests:
        print("ERROR: No test cases found in compliance/tests/")
        return 1

    verbose = "-v" in sys.argv
    passed = 0
    failed = 0

    print(f"Sabdo Compliance Test Suite")
    print(f"{'=' * 60}")

    for test in tests:
        ok, msg = run_test(test, verbose=verbose)
        if ok:
            print(f"  ✓ {test}")
            passed += 1
        else:
            print(f"  ✗ {test}: {msg}")
            failed += 1

    print(f"{'=' * 60}")
    print(f"  Total: {len(tests)}  Passed: {passed}  Failed: {failed}")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
