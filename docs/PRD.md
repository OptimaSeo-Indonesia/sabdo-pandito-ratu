# Product Requirements Document

## Sabdo Pandito Ratu — Decision Intelligence Framework v1

---

## 1. Product Vision

Sabdo Pandito Ratu aims to become **the open-source decision intelligence layer between humans and AI models**. It enables organizations and individuals to move from single-model interactions to structured, multi-perspective deliberation — producing decisions that are more objective, transparent, auditable, and ethically grounded than any single AI can provide.

---

## 2. Target Audience

| Persona | Description | Primary Need |
|---------|-------------|--------------|
| **Decision Maker** | Executive, founder, or manager facing strategic choices | Multi-perspective analysis, risk assessment, explainable recommendations |
| **Policy Analyst** | Evaluates regulatory and compliance scenarios | Evidence-weighted recommendations, principle-based evaluation |
| **Researcher** | Synthesizes findings across multiple sources | Structured argument comparison, scenario exploration |
| **AI Safety Researcher** | Studies alignment, bias, and decision transparency | Audit trail, conflict detection, reflection mechanisms |
| **AI/ML Engineer** | Builds and maintains AI infrastructure | Model evaluation, bias detection, extensible architecture |
| **OSS Contributor** | Extends the platform with new advisors, evaluators, or providers | Modular plugin architecture, clear protocols |

---

## 3. User Stories

### MVP (v0.1 — Completed)

| ID | Story | Acceptance Criteria |
|----|-------|-------------------|
| US-1 | As a user, I can submit a question and receive structured perspectives from multiple AI advisor personas. | 6 personas generate criteria-based evaluations; responses include stance, confidence, key points |
| US-2 | As a user, I can see conflicts between advisor perspectives identified and classified. | Conflicts detected via pairwise stance comparison; types include explicit_conflict, value_tradeoff, nuance_difference |
| US-3 | As a user, I can see my question evaluated against ethical principles. | 5 principles scored (0-10) with rationale and concerns; weights configurable via profile |
| US-4 | As a user, I can explore possible decision outcomes across multiple time horizons. | 12 scenarios generated (4 horizons × 3 biases); each with assumptions, uncertainty level, net impact |
| US-5 | As a user, I can receive a final verdict with supporting reasoning and recommendations. | Verdict includes: decision, confidence, wisdom score, key factors, supporting/opposing arguments, recommendations |
| US-6 | As a user, I can view a reflection that checks for blind spots in the deliberation. | Reflection checks perspective coverage, argument consistency, principle alignment, uncertainty disclosure |
| US-7 | As a user, I can see which wisdom dimensions contributed to the final score. | 6-dimension WisdomScore reported: evidence quality, perspective diversity, ethical alignment, long-term impact, uncertainty handling, reversibility |
| US-8 | As a developer, I can integrate the engine via REST API. | Endpoints: POST /deliberate, GET /deliberate/{id}/report, GET /advisors |

### Post-MVP (v0.2+)

| ID | Story |
|----|-------|
| US-9 | As a user, I can compare the deliberation result against a single LLM answer to evaluate added value. |
| US-10 | As a user, I can provide feedback on decision outcomes to improve future weighting. |
| US-11 | As a user, I can retrieve past decisions and view their recorded outcomes and lessons learned. |
| US-12 | As a user, I can configure which principle profile to use (balanced, public_policy, startup, healthcare, personal). |
| US-13 | As a user, I can generate a PDF/printable decision report. |
| US-14 | As a user, I can add custom advisor personas with domain-specific criteria. |

---

## 4. Functional Requirements

### FR-1: Advisor Council

| Requirement | Description |
|-------------|-------------|
| FR-1.1 | System must support 6 default advisor personas: Rational Analyst, Humanitarian, Economic, Legal, Devil's Advocate, Long-Term Strategist |
| FR-1.2 | Each persona must have a structured evaluation criteria matrix (not free-form prompting) |
| FR-1.3 | Each persona may use a different AI provider and model |
| FR-1.4 | Advisors must be configurable via YAML/JSON without code changes |
| FR-1.5 | Persona registry must support adding, removing, and updating profiles |

### FR-2: Principle Engine

| Requirement | Description |
|-------------|-------------|
| FR-2.1 | System must evaluate decisions against 5 principles: fairness, transparency, sustainability, human impact, accountability |
| FR-2.2 | Principle weights must be configurable via named profiles |
| FR-2.3 | Profiles must include: balanced, public_policy, startup, healthcare, personal |
| FR-2.4 | Each principle evaluation must include a score (0-10), rationale, and concerns |

### FR-3: Scenario Exploration

| Requirement | Description |
|-------------|-------------|
| FR-3.1 | System must generate scenarios across 4 time horizons: 6 months, 2 years, 5 years, 10 years |
| FR-3.2 | Each horizon must be explored with 3 biases: optimistic, pessimistic, most_likely |
| FR-3.3 | Each scenario must document its underlying assumptions and uncertainty level |
| FR-3.4 | Terminology must use "exploration" not "prediction" |

### FR-4: Reflection

| Requirement | Description |
|-------------|-------------|
| FR-4.1 | System must check perspective coverage — which persona viewpoints are missing |
| FR-4.2 | System must flag principles scoring below 5.0 as red flags |
| FR-4.3 | System must adjust confidence based on data gaps and missing perspectives |

### FR-5: Wisdom Scoring

| Requirement | Description |
|-------------|-------------|
| FR-5.1 | System must compute a multi-dimensional WisdomScore with at least 6 dimensions |
| FR-5.2 | Overall score must be a weighted combination of all dimensions |
| FR-5.3 | Per-advisor scores must be reported alongside the overall score |

### FR-6: Decision Report

| Requirement | Description |
|-------------|-------------|
| FR-6.1 | System must produce both structured JSON and human-readable text reports |
| FR-6.2 | Report must include: council composition, conflicts, principle evaluations, scenario explorations, reflection notes, wisdom score, recommendations |
| FR-6.3 | Report must be auditable — every input and intermediate step must be traceable |

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Latency | Full deliberation complete within 60 seconds (with real LLM calls) |
| NFR-2 | Extensibility | New advisor persona in < 50 lines of code |
| NFR-3 | Test Coverage | > 85% unit + integration test coverage |
| NFR-4 | Observability | Structured logs, OpenTelemetry traces, Prometheus metrics |
| NFR-5 | Security | API keys via env/secret vault, no credential leak |
| NFR-6 | Data Privacy | User questions not sent to untrusted providers without consent |
| NFR-7 | Portability | Runs fully with `docker compose up` |

---

## 6. Constraints

| Constraint | Description |
|------------|-------------|
| C-1 | AI provider adapters must be stateless — all state lives in the DeliberationState |
| C-2 | Principle weights must be adjustable without code changes |
| C-3 | All intermediate deliberation data must be preservable for audit |
| C-4 | The system must work without internet access (using local models via Ollama) |

---

## 7. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Wisdom Score variance | > 20% between different decisions | Standard deviation of overall scores across test cases |
| Conflict detection rate | > 80% of real conflicts identified | Human evaluation of test cases |
| Principle coverage | All 5 principles scorable | % of deliberations with complete principle evaluations |
| Decision diversity | Different profiles produce different verdicts | Compare verdicts across 5 principle profiles on same question |
| Reflection impact | > 30% of cases have at least one reflection note | % of deliberations with non-empty reflection |
