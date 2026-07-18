# Sabdo Pandito Ratu

**Open-Source Deliberation Engine — Transparent, Multi-Perspective Decision Intelligence**

Sabdo Pandito Ratu is an open-source deliberation engine that replaces single-model AI answers with structured, multi-perspective decision-making. It orchestrates a council of AI advisor personas, evaluates arguments against ethical principles, explores consequences across time horizons, reflects on blind spots, and produces explainable verdicts — not as a chatbot, but as a digital judge.

---

## Why Sabdo Pandito Ratu?

Organizations today face a critical problem: multiple LLMs produce multiple answers, but there is no standard way to reconcile conflicting outputs, weigh evidence, or produce a verifiable final decision.

- **Bias is amplified**, not reduced, when relying on a single model.
- **Majority voting is naive** — it ignores argument quality, domain expertise, and ethical alignment.
- **Decisions are opaque** — there is no chain of reasoning that humans can inspect or challenge.
- **Vendor lock-in** makes evaluation infrastructure non-portable.

Sabdo Pandito Ratu solves this by acting as a **digital Resi (sage)** — a system that hears all advisors, detects conflicts, evaluates principles, explores consequences, reflects on its own reasoning, and delivers a reasoned verdict.

## What Makes This Different from LLM Orchestration?

Tools like LangChain, LlamaIndex, and AI gateways route prompts to models. Sabdo Pandito Ratu does something fundamentally different:

| Capability | LLM Orchestrator | Sabdo Pandito Ratu |
|---|---|---|
| **Core function** | Route prompts → collect responses | Synthesize structured judgment |
| **Works without LLM?** | No — useless without models | **Yes** — full pipeline runs on heuristics, scoring algorithms, rule-based conflict detection |
| **What is "good"?** | Undefined — returns whatever the model says | Measured — WisdomScore (6 dimensions), ethical alignment (5 profiles) |
| **Conflict handling** | None — returns raw outputs | Systematic — 5 conflict types detected and resolved |
| **Transparency** | Black box — "the model said so" | Full audit trail — every step logged, reproducible |
| **Decision ownership** | The LLM | The **process** — LLMs are just advisors, not deciders |

---

## Philosophy

The name is rooted in Javanese wisdom:

| Term | Meaning |
|------|---------|
| **Sabdo** | Word, decree, or decision |
| **Pandito** | Wisdom, deep consideration, sage-like judgment |
| **Ratu** | Authority, the sovereign power to decide |

Together, **Sabdo Pandito Ratu** embodies the ideal of a wise sovereign who makes decisions not by whim, but through deliberate, multi-perspective consultation — a principle perfectly suited for AI-mediated decision-making.

### Core Tenets

1. **Provider Agnostic** — No vendor lock-in. Any AI model that exposes an API can participate.
2. **Human Understandable** — Every decision must be explainable in plain language.
3. **Open Source First** — Community extensible, auditable, and forkable.
4. **Modular Architecture** — Every intelligence component (advisors, evaluators, memory) is replaceable.
5. **Production Quality** — Tests, logging, observability, and documentation from day one.

---

## Use Cases

| Domain | Example |
|--------|---------|
| **Business Strategy** | "Should we pivot our product roadmap?" |
| **Policy Analysis** | "What are the trade-offs of regulation X?" |
| **Technical Design** | "Which architecture best meets our scalability requirements?" |
| **Risk Assessment** | "Evaluate the risk profile of this investment decision." |
| **Ethical Review** | "Does this AI feature introduce fairness concerns?" |
| **Research** | "Synthesize conflicting findings across these 5 papers." |
| **Compliance** | "Does this workflow comply with GDPR and CCPA?" |
| **Personal** | "Should I accept this job offer or start my own company?" |

---

## Architecture

Sabdo Pandito Ratu implements a **9-step deliberation pipeline** organized into 6 layers:

```
User Problem / Question
      │
      ▼
┌──────────────────────────────────────────────────────────────────┐
│  1. ADVISOR INTELLIGENCE LAYER                                    │
│                                                                   │
│     Context Analyzer ── identifies domain, stakeholders, gaps     │
│           │                                                      │
│     Advisor Council ── 6 personas with criteria-based evaluation  │
│       ├── Rational Analyst     → evidence, data, probabilities   │
│       ├── Humanitarian         → human impact, fairness, dignity │
│       ├── Economic             → cost, efficiency, sustainability│
│       ├── Legal                → compliance, liability, risk     │
│       ├── Devil's Advocate     → edge cases, failure modes       │
│       └── Long-Term Strategist → systemic effects, 10yr horizon  │
│                                                                   │
│  2. DELIBERATION LAYER                                            │
│                                                                   │
│     Argument Collector ── structure raw responses                 │
│           │                                                      │
│     Conflict Resolver ── detects 5 conflict types                │
│           │                                                      │
│  3. DHARMA LAYER (Principle Engine)                               │
│                                                                   │
│     Principle Evaluation ── 5 principles × configurable weights   │
│       ├── Fairness / Transparency / Sustainability               │
│       ├── Human Impact / Accountability                          │
│       └── Weight profiles: balanced, public_policy, startup,     │
│                            healthcare, personal                   │
│           │                                                      │
│  4. CONSEQUENCE LAYER                                             │
│                                                                   │
│     Scenario Exploration ── 12 scenarios (4 horizons × 3 biases) │
│       ├── 6 months / 2 years / 5 years / 10 years                │
│       ├── Optimistic / Pessimistic / Most Likely                 │
│       └── Each with assumptions + uncertainty level              │
│           │                                                      │
│  5. JUDGMENT LAYER                                                │
│                                                                   │
│     Reflection ── check coverage, consistency, red flags         │
│           │                                                      │
│     Wisdom Scoring ── 6-dimension score                          │
│       ├── Evidence Quality / Perspective Diversity               │
│       ├── Ethical Alignment / Long-Term Impact                   │
│       ├── Uncertainty Handling / Reversibility                   │
│           │                                                      │
│     Verdict Generation ── structured decision + report           │
│                                                                   │
│  6. COLLECTIVE MEMORY LAYER                                       │
│                                                                   │
│     Case Storage ── problem → arguments → outcome → lessons      │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
      │
      ▼
Decision Report (explainable, auditable)
```

### Core Modules

| Module | Responsibility |
|--------|----------------|
| **Advisor Council** | 6 persona profiles with criteria-based evaluation frameworks |
| **Inference Layer** | Vendor-agnostic adapter interface — selects best adapter per persona via capability matching |
| **Deliberation Engine** | 9-step LangGraph state machine orchestrating the full pipeline |
| **Dharma Layer** | Principle evaluation engine with configurable weight profiles |
| **Consequence Layer** | Multi-horizon scenario exploration with assumptions tracking |
| **Judgment Layer** | 6-dimension wisdom scoring + verdict generation |
| **Collective Memory** | Case-based storage with outcome tracking and similarity search |
| **Explainability** | Decision report generation (structured JSON + human-readable) |

---

## Roadmap

| Phase | Status | Focus |
|-------|--------|-------|
| P0 | ✓ Completed | Foundation: architecture, provider abstraction, advisor system |
| P1 | ✓ Completed | Deliberation core: LangGraph pipeline, conflict resolver, reflection node |
| P2 | ✓ Completed | Wisdom framework: principle engine, scenario exploration, wisdom scorer |
| P3 | ✓ Completed | Memory intelligence: collective wisdom case storage, database schema |
| P4 | 🔜 Next | Evaluation & benchmarking: decision datasets, comparison vs single LLM |
| P5 | 📅 Planned | Production platform: auth, multi-user, API access, dashboard |
| P6 | 📅 Planned | Community intelligence: shared cases, open decision repository |

See [docs/mvp-roadmap.md](docs/mvp-roadmap.md) for the detailed development plan.

---

## Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/your-org/sabdo-pandito-ratu.git
cd sabdo-pandito-ratu

# Create virtual environment and install
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests to verify the deliberation pipeline
python -m pytest tests/ -v
```

---

## Project Structure

```
sabdo-pandito-ratu/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── routes/       # REST + WebSocket endpoints
│   │   └── db/           # Alembic migrations + SQLAlchemy models
│   └── web/              # Next.js frontend
├── core/
│   ├── deliberation/     # 9-step LangGraph pipeline + Reflection + Analyzer
│   ├── advisors/         # Persona definitions, registry, evaluation
│   ├── inference/        # Backend selection + capability scoring
│   ├── principles/       # Dharma Layer — principle engine + profiles
│   ├── simulation/       # Consequence Layer — scenario exploration
│   ├── evaluation/       # Judgment Layer — 6-dimension wisdom scoring
│   ├── explainability/   # Decision report generation
│   └── memory/           # Collective Wisdom Memory
├── inference/
│   └── adapters/         # Inference adapter implementations
├── docs/                 # Documentation
│   ├── PRD.md
│   ├── architecture.md
│   ├── database-design.md
│   ├── api-design.md
│   ├── mvp-roadmap.md
│   └── decision-model.md
├── examples/             # Decision reports
├── tests/                # 81 tests across all modules
├── docker-compose.yml
└── README.md
```

---

## Learn More

| Document | Description |
|----------|-------------|
| [PRD](docs/PRD.md) | Product requirements, user stories, acceptance criteria |
| [Architecture](docs/architecture.md) | System architecture, layers, data flow |
| [Decision Model](docs/decision-model.md) | WisdomScore, Reflection, Principle Profiles — how verdicts are made |
| [API Design](docs/api-design.md) | REST + WebSocket API specification |
| [Database](docs/database-design.md) | PostgreSQL + pgvector schema (Alembic migrations ready) |
| [Roadmap](docs/mvp-roadmap.md) | Development roadmap with phases and milestones |

---

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.

Copyright (C) 2026 OptimaSeo Indonesia. All rights reserved under the GNU AGPL v3.
