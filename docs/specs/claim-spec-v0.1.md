# Sabdo Claim Specification v0.1

**Status:** Draft
**Last updated:** 2026-07-22
**Reference implementation:** `core/models.py :: Claim`, `core/verification/engine.py`

---

## 1. Purpose

Define the fundamental unit of deliberation: a **Claim** is a single assertion made by an advisor during the deliberation process. Claims are the atomic unit that flows through evidence verification, conflict resolution, and wisdom scoring.

---

## 2. Status

This specification is **Draft**. It is subject to change based on implementation experience. Once at least two independent implementations pass the compliance test suite, this will be promoted to **Experimental**.

---

## 3. Core Objects

### 3.1 Claim

A Claim represents a single assertion extracted from an advisor's response.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID v4) | yes | Globally unique identifier |
| `text` | string | yes | The assertion text |
| `source_advisor_id` | string | yes | Identifier of the originating advisor |
| `source_persona` | string (enum) | yes | The advisor persona that produced this claim |
| `confidence` | float [0, 1] | yes | Self-reported confidence of the source advisor |
| `extracted_entities` | array[string] | no | Key entities extracted from the claim text |
| `parent_response_id` | string | no | ID of the parent advisor response |

**Persona enum values:** `rational_analyst`, `humanitarian`, `economic`, `legal`, `devils_advocate`, `long_term_strategist`

**Constraints:**
- `id` MUST be a valid UUID v4
- `text` MUST NOT be empty
- `confidence` MUST be in range [0.0, 1.0]

### 3.2 Evidence

Evidence is a piece of information that can support or refute a Claim.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID v4) | yes | Globally unique identifier |
| `text` | string | yes | The evidence text |
| `source_ref` | string | no | A reference citation or URL for the evidence |
| `source_type` | string (enum) | yes | Category of the evidence source |
| `provider` | string | no | The advisor or system that provided this evidence |
| `timestamp` | datetime (ISO 8601) | yes | When the evidence was recorded |

**Source type enum values:** `data_source`, `advisor_reasoning`, `external`

**Constraints:**
- `id` MUST be a valid UUID v4
- `text` MUST NOT be empty
- `timestamp` MUST be in ISO 8601 UTC format

### 3.3 VerificationStatus

The status of a Claim after verification against available Evidence.

| Value | Description |
|-------|-------------|
| `verified` | Claim is supported by at least one piece of evidence with sufficient keyword overlap |
| `unsupported` | No evidence available, or claim confidence is too low to warrant uncertain status |
| `contradicted` | Claim directly contradicts another verified claim (reserved for future use) |
| `uncertain` | Evidence exists but overlap is insufficient for full verification |

### 3.4 ProvenanceRecord

Links a Claim to the Evidence that supports it.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `claim_id` | string (UUID) | yes | The verified claim ID |
| `evidence_id` | string (UUID) | yes | The matching evidence ID |
| `match_type` | string (enum) | yes | How the match was determined |
| `match_score` | float [0, 1] | yes | Confidence of the match |
| `verified_at` | datetime (ISO 8601) | yes | When verification occurred |

**Match type enum values:** `keyword`, `semantic`, `llm_assisted`

**Constraints:**
- `match_score` MUST be in range [0.0, 1.0]
- `claim_id` and `evidence_id` MUST reference existing Claim and Evidence objects

### 3.5 VerificationResult

The complete output of verifying a single Claim.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `claim_id` | string (UUID) | yes | The verified claim ID |
| `status` | VerificationStatus | yes | Verification outcome |
| `support_ratio` | float [0, 1] | yes | Proportion of evidence that matched this claim |
| `provenance` | array[ProvenanceRecord] | no | Evidence provenance chain |
| `matched_evidence` | array[string] | no | References to evidence that matched |
| `unmatched_evidence` | array[string] | no | References to evidence that did not match |
| `confidence` | float [0, 1] | yes | Computed confidence (combines support ratio + evidence volume) |

**Constraints:**
- `support_ratio` MUST be in range [0.0, 1.0]
- `confidence` MUST be in range [0.0, 1.0]
- If `status` is `verified`, at least one `ProvenanceRecord` SHOULD exist

---

## 4. Verification Algorithm (Reference)

The reference implementation uses a keyword-overlap approach:

1. Tokenize claim text: extract lowercase words matching `[a-zA-Z]\w+`, filter to length > 2
2. Tokenize each evidence text using the same method
3. For each claim-evidence pair, compute `len(claim_tokens & evidence_tokens)`
4. If overlap >= 2 and at least one evidence matches → `verified`
5. If no evidence available → `unsupported`
6. Otherwise → `uncertain`
7. `support_ratio` = `matched_evidence_count / total_evidence_count`
8. `confidence` = `support_ratio * 0.8 + min(total_evidence / 5, 1.0) * 0.2`

Future implementations may replace this with semantic or LLM-assisted approaches, as long as the output format conforms to this specification.

---

## 5. Serialization

All objects MUST be serializable to JSON.

### 5.1 Claim JSON Example

```json
{
  "id": "6c456a54-1234-5678-9abc-def012345678",
  "text": "Solar panels reduce carbon emissions by 40%.",
  "source_advisor_id": "ra_001",
  "source_persona": "rational_analyst",
  "confidence": 0.85,
  "extracted_entities": ["solar", "panels", "reduce", "carbon", "emissions"],
  "parent_response_id": "ra_001"
}
```

### 5.2 Evidence JSON Example

```json
{
  "id": "c04bdbbf-9876-5432-1fed-cba098765432",
  "text": "IEA Renewables 2025 report",
  "source_ref": "IEA Renewables 2025 report",
  "source_type": "data_source",
  "provider": "ra_001",
  "timestamp": "2026-07-22T10:30:00Z"
}
```

### 5.3 VerificationResult JSON Example

```json
{
  "claim_id": "6c456a54-1234-5678-9abc-def012345678",
  "status": "verified",
  "support_ratio": 0.5,
  "provenance": [
    {
      "claim_id": "6c456a54-...",
      "evidence_id": "c04bdbbf-...",
      "match_type": "keyword",
      "match_score": 0.83,
      "verified_at": "2026-07-22T10:30:05Z"
    }
  ],
  "matched_evidence": ["IEA Renewables 2025 report"],
  "unmatched_evidence": [],
  "confidence": 0.82
}
```

---

## 6. Compliance

An implementation is **Sabdo Claim Specification v0.1 compliant** if:

1. It can produce `Claim`, `Evidence`, `ProvenanceRecord`, and `VerificationResult` objects conforming to the field types and constraints above
2. All objects serialize to valid JSON as specified
3. It passes the Sabdo Compliance Test Suite for Claim Specification

---

## 7. Future Considerations

- Semantic matching via embeddings (planned for v0.2)
- LLM-assisted verification (planned for v0.2)
- Cross-referencing claims across deliberations (planned for v0.3)
- Support for multiple evidence types (quantitative, qualitative, statistical)
