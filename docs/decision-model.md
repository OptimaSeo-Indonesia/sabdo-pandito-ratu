# Decision Model

## How Sabdo Pandito Ratu Makes Decisions

This document explains the core decision-making mechanism of Sabdo Pandito Ratu — the **WisdomScore**, **Reflection Layer**, **Principle Profiles**, and how a final verdict is constructed from raw deliberation data.

---

## 1. The Deliberation Pipeline

Every decision passes through 9 sequential stages:

```
Question → Context → Perspectives → Arguments → Conflicts
    → Principles → Scenarios → Reflection → Wisdom Score → Verdict
```

Each stage transforms the `DeliberationState` (defined in `core/models.py`) and contributes to the final decision.

---

## 2. WisdomScore

The WisdomScore is the central quantitative measure of decision quality. It is **not** a simple average — it weighs 6 distinct dimensions that capture different aspects of decision quality.

### Formula

```
WisdomScore(overall) =
    0.25 × EvidenceQuality
  + 0.15 × PerspectiveDiversity
  + 0.20 × EthicalAlignment
  + 0.15 × LongTermImpact
  + 0.15 × UncertaintyHandling
  + 0.10 × Reversibility
```

All dimensions are normalized to 0-100.

### Dimension Definitions

#### Evidence Quality (Weight: 0.25)

**What it measures:** The strength and reliability of data supporting the decision.

**Computation** (from `core/evaluation/scorer.py:_score_evidence_quality`):
```python
score = (avg_confidence * 60) + (data_source_ratio * 40)
```

- `avg_confidence`: Average confidence across all advisor responses
- `data_source_ratio`: Proportion of advisors that provided explicit data sources

**Interpretation:**
- > 80: Strong empirical foundation
- 60-80: Adequate evidence, some gaps
- < 60: Limited evidence, decisions should be treated as preliminary

#### Perspective Diversity (Weight: 0.15)

**What it measures:** How many distinct viewpoints were represented in the deliberation.

**Computation** (from `core/evaluation/scorer.py:_score_perspective_diversity`):
```python
diversity = min(unique_personas / total_personas * 100, 100)
bonus = min(len(conflicts) * 5, 20)
score = min(diversity + bonus, 100)
```

- Rewards having all 6 personas represented
- Bonuses for detected conflicts (disagreement signals healthy diversity)
- Penalty for missing perspectives (flagged by Reflection layer)

**Interpretation:**
- > 80: Full council with meaningful disagreement
- 50-80: Partial council or limited disagreement
- < 50: Insufficient perspective diversity

#### Ethical Alignment (Weight: 0.20)

**What it measures:** How well the decision aligns with 5 ethical principles.

**Computation** (from `core/evaluation/scorer.py:_score_ethical_alignment`):
```python
weighted_sum = sum(e.score * e.weight for e in evaluations)
max_possible = 10 * sum(e.weight for e in evaluations)
score = (weighted_sum / max_possible) * 100
```

- Each principle is scored 0-10 by the Principle Engine
- Weights come from the selected principle profile (see Section 4)

**Interpretation:**
- > 80: Strong ethical alignment across all principles
- 60-80: Moderate alignment, some principles need attention
- < 60: Significant ethical concerns — default should be "do not proceed"

#### Long-Term Impact (Weight: 0.15)

**What it measures:** Projected outcomes over extended time horizons.

**Computation** (from `core/evaluation/scorer.py:_score_long_term_impact`):
```python
avg_net = average(net_impact of "10 years" scenarios)
score = ((avg_net + 10) / 20) * 100
```

- Uses 10-year horizon scenarios only (most strategic)
- net_impact ranges from -10 (catastrophic) to +10 (transformative)

**Interpretation:**
- > 70: Strong positive projected trajectory
- 40-70: Neutral or mixed long-term outlook
- < 40: Negative projected trajectory

#### Uncertainty Handling (Weight: 0.15)

**What it measures:** How transparent the deliberation is about what it doesn't know.

**Computation** (from `core/evaluation/scorer.py:_score_uncertainty`):
```python
penalty = data_gaps * 5 + uncertainty_mentions * 3
score = max(100 - penalty, 0)
```

- Data gaps are identified in the Context Analysis step
- Uncertainty mentions are flagged by the Reflection layer

**Interpretation:**
- > 80: Well-calibrated uncertainty disclosure
- 50-80: Some gaps acknowledged but not fully accounted for
- < 50: Significant unaddressed uncertainty

#### Reversibility (Weight: 0.10)

**What it measures:** How easily the decision can be undone if it proves wrong.

**Computation** (from `core/evaluation/scorer.py:_score_reversibility`):
```python
irreversible_signals = count of "irreversible", "permanent", etc.
score = max(100 - irreversible_signals * 15, 10)
```

- Penalized when advisors use language indicating permanent consequences

**Interpretation:**
- > 80: Decision is reversible or adjustable
- 50-80: Partially reversible with some sunk costs
- < 50: Largely irreversible — requires higher confidence threshold

### Example WisdomScore

```
Dimension                Raw Score  Weight  Contribution
Evidence Quality         82         0.25    20.5
Perspective Diversity    78         0.15    11.7
Ethical Alignment        73         0.20    14.6
Long-Term Impact         80         0.15    12.0
Uncertainty Handling     65         0.15     9.8
Reversibility            70         0.10     7.0
                                       ─────────
                       OVERALL         75.6 / 100
```

---

## 3. Reflection Layer

The Reflection layer (`core/deliberation/reflection.py`) performs a meta-cognitive check before the final verdict. It is one of the key differentiators of Sabdo Pandito Ratu.

### Four Checks

#### 3.1 Perspective Coverage

```
Question: "Are all 6 advisor personas represented?"
If missing: ⚠ "{persona} perspective was not consulted"
If >2 missing: ⚠ "Deliberation may lack diversity"
```

#### 3.2 Argument Consistency

```
Question: "Is there genuine debate, or is the council uncertain?"
Healthy: "Healthy disagreement detected: Rational vs Humanitarian"
Warning: "No strong stance detected — council may lack conviction"
```

#### 3.3 Principle Alignment

```
Question: "Are any principles scoring below acceptable thresholds?"
Red flag (<5.0): "Principle 'fairness' scores 4/10 — below threshold"
Monitor (5-7):  "Principle 'sustainability' at 6/10 — adequate"
```

#### 3.4 Uncertainty Disclosure

```
Question: "Are data gaps properly reflected in confidence?"
Penalty: -0.05 per data gap (max -0.15)
```

### Confidence Adjustment

After the 4 checks, the Reflection node computes an adjusted confidence:

```python
adjustment = 0.0
adjustment -= 0.05 * len(missing_perspectives)   # max -0.15
adjustment -= 0.08 * len(consistency_issues)      # max -0.24
adjustment -= 0.05 * len(data_gaps)               # max -0.15
adjustment = clamp(adjustment, -0.50, +0.10)
final_confidence = base_confidence + adjustment
```

---

## 4. Principle Profiles

Sabdo Pandito Ratu does **not** impose a single universal value system. Instead, it provides configurable principle weight profiles (`core/principles/profiles.py`).

### Profile Definitions

| Profile | Fairness | Transparency | Sustainability | Human Impact | Accountability | Best For |
|---------|----------|--------------|----------------|--------------|----------------|----------|
| `balanced` | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | General decisions |
| `public_policy` | 0.30 | 0.30 | 0.15 | 0.15 | 0.10 | Regulations, governance |
| `startup` | 0.10 | 0.15 | 0.30 | 0.15 | 0.30 | Business, entrepreneurship |
| `healthcare` | 0.25 | 0.20 | 0.10 | 0.35 | 0.10 | Medical, health policy |
| `personal` | 0.15 | 0.25 | 0.20 | 0.30 | 0.10 | Individual life decisions |

### How Profiles Affect Decisions

The principle profile is selected by passing `principle_profile` in the deliberation context:

```python
context = {
    "principle_profile": "public_policy"
}
```

The profile determines:
1. **Which principles are weighted most heavily** in the Ethical Alignment dimension
2. **How the final verdict weighs ethical concerns** against other factors

Example — same question, different profiles:
- `startup` profile might recommend "proceed" on a high-risk high-reward decision
- `public_policy` profile on the same question might recommend "proceed with caution"

---

## 5. Verdict Generation

The final verdict (`core/explainability/reporter.py`) is generated after all 9 pipeline stages complete.

### Decision Rules

The verdict decision is determined by weighted stance analysis:

```python
yes_weight = sum(advisor.confidence for advisors with "yes" or "cautious_yes" stance)
no_weight  = sum(advisor.confidence for advisors with "no" or "cautious_no" stance)

if yes_weight > no_weight * 1.5:
    decision = "Proceed with recommended course of action"
elif yes_weight >= no_weight:
    decision = "Proceed with caution — monitor key risk factors"
elif no_weight > yes_weight * 1.5:
    decision = "Do not proceed — risks outweigh benefits"
else:
    decision = "Defer decision — requires additional data"
```

### Decision Report Sections

A complete decision report includes:

1. **Case Information** — session_id, question, domain
2. **Verdict** — decision, confidence, overall wisdom score, dimension scores
3. **Council Composition** — each advisor's persona, stance, confidence, summary
4. **Conflicts** — type, between which personas, description, root cause
5. **Principle Evaluations** — each principle's score, weight, rationale, concerns
6. **Scenario Explorations** — 12 scenarios with assumptions, uncertainty, net impact
7. **Reflection** — missing perspectives, consistency issues, confidence adjustment
8. **Reasoning** — key factors, supporting arguments, opposing arguments, conflict resolution
9. **Uncertainties & Data Gaps**
10. **Alternatives Considered**
11. **Recommendations**

### Human-Readable Summary

The `ExplainabilityReporter.generate_summary()` method produces a formatted text report:

```
============================================================
  SABDO PANDITO RATU — DECISION REPORT
============================================================

  DECISION: Proceed with recommended course of action
  CONFIDENCE: 78%
  WISDOM SCORE: 76/100

  DIMENSION SCORES:
    Evidence Quality : 82/100
    Perspective Div. : 78/100
    Ethical Alignment: 73/100
    Long-Term Impact : 80/100
    Uncertainty Hdl. : 65/100
    Reversibility    : 70/100

------------------------------------------------------------
  PRINCIPLE EVALUATION
------------------------------------------------------------
  fairness         ███████░░░ 7.5/10
  transparency     ████████░░ 8.0/10
  sustainability   ███████░░░ 7.0/10
  human_impact     ██████░░░░ 6.5/10
  accountability   ████████░░ 8.0/10

------------------------------------------------------------
  RECOMMENDATIONS
------------------------------------------------------------
  → Validate key assumptions with empirical data
  → Establish clear metrics to monitor outcomes
  → Set review checkpoints at regular intervals
```

---

## 6. Decision Quality Principles

1. **No single number tells the whole story** — The 6-dimension WisdomScore is always reported alongside the individual dimensions, not as a single aggregate.

2. **Confidence is not certainty** — The confidence score reflects the council's assessment, adjusted for known gaps by the Reflection layer. It should never be interpreted as a probability of being correct.

3. **Ethics are contextual** — The same decision may be evaluated differently under different principle profiles. The profile selection should be transparent and deliberate.

4. **Predictions are explorations** — Scenario outcomes are explicitly labeled as explorations with documented assumptions and uncertainty levels, never as predictions.

5. **Every decision is a case** — All deliberations are stored in the Collective Wisdom Memory, creating a growing repository of decision intelligence that improves with use.
