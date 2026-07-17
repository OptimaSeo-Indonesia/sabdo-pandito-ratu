# System Architecture Document

## Sabdo Pandito Ratu — Decision Intelligence Framework v1

---

## 1. Architecture Overview

Sabdo Pandito Ratu is organized into **6 layers** that transform a user question into an explainable decision. Each layer has a distinct responsibility and can be extended independently.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                           │
│  ┌────────────────────┐  ┌──────────────────┐  ┌────────────────┐   │
│  │  Next.js Web App   │  │   REST API       │  │  CLI / SDK     │   │
│  └────────────────────┘  └──────────────────┘  └────────────────┘   │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  1. ADVISOR INTELLIGENCE LAYER                                       │
│                                                                      │
│  ┌────────────────────┐  ┌──────────────────────────────────────┐   │
│  │  Context Analyzer   │  │      Advisor Council                  │   │
│  │  (domain, gaps,     │  │  ┌────────┐ ┌────────┐ ┌────────┐  │   │
│  │   stakeholders)     │  │  │Rational│ │Human-  │ │Economic│  │   │
│  └────────────────────┘  │  │Analyst │ │itarian │ │        │  │   │
│                          │  └────────┘ └────────┘ └────────┘  │   │
│                          │  ┌────────┐ ┌────────┐ ┌────────┐  │   │
│                          │  │ Legal   │ │Devil's │ │Long-   │  │   │
│                          │  │         │ │Advocate│ │Term    │  │   │
│                          │  └────────┘ └────────┘ └────────┘  │   │
│                          └──────────────────────────────────────┘   │
│  Key files: core/advisors/evaluation.py, core/advisors/personas.py  │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  2. DELIBERATION LAYER                                               │
│                                                                      │
│  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │ Argument Collector│───▶│  Conflict        │───▶│  Reflection   │  │
│  │ (structured args) │    │  Resolver        │    │  (meta-check) │  │
│  └──────────────────┘    └──────────────────┘    └───────────────┘  │
│                                                                      │
│  Key files: core/deliberation/graph.py, core/deliberation/reflection.py│
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  3. DHARMA LAYER (Principle Engine)                                  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Principle Evaluation                                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │Fairness  │  │Trans-    │  │Sustain-  │  │Human     │   │   │
│  │  │          │  │parency   │  │ability   │  │Impact    │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  │  ┌──────────┐                                                │   │
│  │  │Account-  │  Principle Profile Manager                     │   │
│  │  │ability   │  ├── balanced    ├── startup                   │   │
│  │  └──────────┘  ├── healthcare  ├── public_policy             │   │
│  │                └── personal                                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Key files: core/principles/engine.py, core/principles/profiles.py  │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  4. CONSEQUENCE LAYER                                                │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Scenario Exploration                                        │   │
│  │                                                              │   │
│  │  6 months     2 years      5 years      10 years             │   │
│  │  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐               │   │
│  │  │Opt.  │    │Opt.  │    │Opt.  │    │Opt.  │               │   │
│  │  │Pess. │    │Pess. │    │Pess. │    │Pess. │               │   │
│  │  │ML    │    │ML    │    │ML    │    │ML    │               │   │
│  │  └──────┘    └──────┘    └──────┘    └──────┘               │   │
│  │                                                              │   │
│  │  Each scenario tracks: assumptions, uncertainty_level,       │   │
│  │  positive/negative outcomes, net_impact                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Key files: core/simulation/simulator.py                           │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  5. JUDGMENT LAYER                                                   │
│                                                                      │
│  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │  WisdomScorer    │───▶│  Verdict          │───▶│  Decision     │  │
│  │  (6 dimensions)  │    │  Generator        │    │  Report       │  │
│  └──────────────────┘    └──────────────────┘    └───────────────┘  │
│                                                                      │
│  Wisdom dimensions: Evidence Quality, Perspective Diversity,         │
│  Ethical Alignment, Long-Term Impact, Uncertainty Handling,          │
│  Reversibility                                                       │
│                                                                      │
│  Key files: core/evaluation/scorer.py, core/explainability/reporter.py│
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│  6. COLLECTIVE MEMORY LAYER                                          │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  CollectiveWisdomMemory                                       │   │
│  │                                                              │   │
│  │  Case: { problem, context, arguments,                        │   │
│  │          decision, outcome, lessons }                         │   │
│  │                                                              │   │
│  │  Features: save, find_similar, record_outcome, get_stats     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Key files: core/memory/store.py                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Deliberation Pipeline (9 Steps)

The core of the system is a **LangGraph state machine** defined in `core/deliberation/graph.py`. Each step is a node in the graph that reads from and writes to a shared `DeliberationState` object.

### Step-by-Step

| Step | Node | Layer | Input | Output | Description |
|------|------|-------|-------|--------|-------------|
| 1 | `analyze_context` | Advisor Intelligence | question, context | `ContextAnalysis` | Identifies domain, stakes, stakeholders, time sensitivity, data gaps |
| 2 | `generate_perspectives` | Advisor Intelligence | context analysis | `list[AdvisorResponse]` | Invokes each active advisor persona with its criteria matrix |
| 3 | `collect_arguments` | Deliberation | perspectives | `list[Argument]` | Structures raw responses into claim + evidence + reasoning |
| 4 | `resolve_conflicts` | Deliberation | arguments | `list[Conflict]` | Pairwise comparison of stances, classifies conflict types |
| 5 | `evaluate_principles` | Dharma | conflicts, perspectives | `list[PrincipleEvaluation]` | Scores 5 principles, applies profile-based weights |
| 6 | `explore_scenarios` | Consequence | principles, tentative decision | `list[ScenarioExploration]` | Generates 12 scenarios with assumptions and uncertainty |
| 7 | `reflect` | Deliberation | all prior output | `Reflection` | Meta-check: coverage, consistency, red flags, adjusts confidence |
| 8 | `score_wisdom` | Judgment | reflection | `WisdomScore` | Computes 6-dimension wisdom score + per-advisor scores |
| 9 | `generate_verdict` | Judgment | wisdom score | `Verdict` | Produces final decision + structured report |

### State Schema

The `DeliberationState` (defined in `core/models.py`) is a Pydantic model that flows through all 9 nodes:

```python
class DeliberationState(BaseModel):
    session_id: UUID
    question: str
    context: dict
    status: SessionStatus
    context_analysis: ContextAnalysis | None
    advisor_responses: list[AdvisorResponse]
    arguments: list[Argument]
    conflicts: list[Conflict]
    principle_evaluations: list[PrincipleEvaluation]
    scenarios: list[ScenarioExploration]
    wisdom_score: WisdomScore | None
    reflection: dict | None
    scores: dict[str, float]
    verdict: Verdict | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None
```

---

## 3. Layer Details

### 3.1 Advisor Intelligence Layer

**Purpose:** Represent diverse decision-making perspectives through structured persona profiles.

**Components:**
- **AdvisorRegistry** (`core/advisors/registry.py`) — In-memory registry of 6 default personas
- **AdvisorEvaluator** (`core/advisors/evaluation.py`) — Criteria-based evaluation framework

Each persona has a **criteria matrix** that replaces free-form opinion with structured assessment:

| Persona | Criteria | Weights |
|---------|----------|---------|
| Rational Analyst | data_quality, logical_coherence, probability_assessment, evidence_basis | 0.30/0.30/0.20/0.20 |
| Humanitarian | human_dignity, fairness_distribution, vulnerable_populations, well_being | 0.30/0.25/0.25/0.20 |
| Economic | cost_impact, revenue_impact, resource_allocation, market_effect, financial_risk | 0.25/0.25/0.20/0.15/0.15 |
| Legal | compliance, liability, regulatory_risk, contractual_obligations | 0.30/0.25/0.25/0.20 |
| Devil's Advocate | edge_cases, assumption_challenge, failure_modes, unintended_consequences | 0.30/0.25/0.25/0.20 |
| Long-Term Strategist | systemic_impact, horizon_viability, adaptability, legacy_effect | 0.30/0.30/0.20/0.20 |

### 3.2 Dharma Layer (Principle Engine)

**Purpose:** Evaluate decisions against universal ethical principles with context-aware weighting.

**5 Principles:**

| Principle | Weight (Balanced) | Description |
|-----------|-------------------|-------------|
| Fairness | 0.20 | Distributes benefits and burdens equitably |
| Transparency | 0.20 | Decision process and reasoning are open to scrutiny |
| Sustainability | 0.20 | Preserves long-term viability across dimensions |
| Human Impact | 0.20 | Direct and indirect effects on human well-being |
| Accountability | 0.20 | Decision-makers can be held responsible for outcomes |

**Configurable Profiles:**

| Profile | Emphasis |
|---------|----------|
| `balanced` | Equal weight across all principles (default) |
| `public_policy` | Fairness (0.30) + Transparency (0.30) |
| `startup` | Sustainability (0.30) + Accountability (0.30) |
| `healthcare` | Human Impact (0.35) + Fairness (0.25) |
| `personal` | Human Impact (0.30) + Transparency (0.25) |

### 3.3 Consequence Layer

**Purpose:** Explore possible outcomes without claiming prediction.

The `ScenarioExplorer` generates **12 scenarios** per deliberation:

- **4 time horizons**: 6 months, 2 years, 5 years, 10 years
- **3 biases per horizon**: optimistic, pessimistic, most_likely
- Each scenario includes: assumptions (with confidence scores), uncertainty level (low/medium/high), positive/negative outcomes, net impact score

### 3.4 Reflection Layer

**Purpose:** Meta-cognitive check before final verdict.

The `ReflectionNode` performs 4 checks:
1. **Perspective coverage** — Are any of the 6 personas missing?
2. **Argument consistency** — Is there healthy disagreement or no strong stance?
3. **Principle alignment** — Are any principles scoring below 5.0 (red flag)?
4. **Uncertainty disclosure** — Are data gaps properly accounted for?

Adjusts final confidence based on findings.

### 3.5 Judgment Layer

**Purpose:** Compute wisdom score and generate final verdict.

**WisdomScore** consists of 6 dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Evidence Quality | 0.25 | Strength of supporting data and reasoning |
| Perspective Diversity | 0.15 | Range of viewpoints represented |
| Ethical Alignment | 0.20 | Score across all 5 ethical principles |
| Long-Term Impact | 0.15 | Projected outcomes across 10-year horizon |
| Uncertainty Handling | 0.15 | How well data gaps and risks are acknowledged |
| Reversibility | 0.10 | Ability to undo or adjust the decision |

### 3.6 Collective Memory Layer

**Purpose:** Learn from past decisions.

The `CollectiveWisdomMemory` stores structured cases:

```python
class DecisionCase(BaseModel):
    case_id: str
    question: str
    domain: str
    verdict: str
    confidence: float
    wisdom_score: WisdomScore | None
    outcome: str | None         # recorded after the fact
    outcome_score: float | None # -10 to 10
    lessons_learned: list[str]
    created_at: datetime
    reviewed_at: datetime | None
```

Supports: `save_session`, `record_outcome`, `find_similar_cases`, `get_stats`.

---

## 4. Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| API Framework | FastAPI | Async, type-safe, auto OpenAPI docs |
| AI Orchestration | LangGraph | State machine for multi-step AI workflows |
| Data Validation | Pydantic v2 | Runtime type safety across all layers |
| Database | PostgreSQL 16 | ACID-compliant, reliable storage |
| Vector Search | pgvector | Semantic search for similar cases |
| Cache / Queue | Redis | Rate limiting, session cache |
| Frontend | Next.js 14 | SSR, React Server Components, TypeScript |
| Containerization | Docker Compose | Single-command local dev and deployment |
| Observability | OpenTelemetry | Vendor-neutral traces, metrics, logs |
| Testing | pytest + vitest | 64+ tests across all modules |

---

## 5. Data Flow

```
Client
  │ POST /api/v1/deliberate {question, context, config}
  ▼
FastAPI — validates request, creates session
  │
  ▼
DeliberationGraph.run(state)
  │
  ├── analyze_context ──────► ContextAnalysis
  ├── generate_perspectives ─► list[AdvisorResponse]  ──► AdvisorEvaluator
  ├── collect_arguments ─────► list[Argument]
  ├── resolve_conflicts ─────► list[Conflict]         ──► pairwise stance
  ├── evaluate_principles ───► list[PrincipleEvaluation] ──► PrincipleEngine + ProfileManager
  ├── explore_scenarios ─────► list[ScenarioExploration]  ──► ScenarioExplorer
  ├── reflect ───────────────► Reflection              ──► ReflectionNode
  ├── score_wisdom ──────────► WisdomScore             ──► WisdomScorer
  └── generate_verdict ──────► Verdict                 ──► ExplainabilityReporter
  │
  ▼
CollectiveWisdomMemory.save_session(state)
  │
  ▼
Response — verdict + report back to client
```

---

## 6. Error Handling

| Scenario | Strategy |
|----------|----------|
| Advisor timeout | Configurable per-provider; mark as unavailable |
| Partial advisor failure | Continue with remaining; note exclusion in report |
| All advisors fail | Return error with diagnostic information |
| Rate limiting | Exponential backoff with jitter |
| Database loss | Connection pool with retry and circuit breaker |

---

## 7. Security

| Concern | Implementation |
|---------|----------------|
| API Key Storage | Environment variables or mounted secrets |
| Provider Credentials | Vault integration (planned) |
| Input Sanitization | Pydantic validation on all endpoints |
| Rate Limiting | Redis-backed rate limiter |
| CORS | Strict origin configuration |
| Audit Trail | All deliberations logged immutably |
