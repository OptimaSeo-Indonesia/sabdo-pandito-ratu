# Development Roadmap

## Sabdo Pandito Ratu — v0.1 to v1.0

---

## Completed Phases

### P0: Foundation ✓

| Component | Status | Description |
|-----------|--------|-------------|
| Project scaffolding | ✓ | Monorepo, directory structure, Docker Compose |
| Configuration | ✓ | pyproject.toml, .env.example, settings |
| CI/CD | ✓ | GitHub Actions: lint, typecheck, test |
| Pre-commit hooks | ✓ | ruff, mypy, standard hooks |

### P1: Deliberation Core ✓

| Component | Status | Description |
|-----------|--------|-------------|
| LangGraph pipeline | ✓ | 9-node sequential state machine |
| Context analyzer | ✓ | Domain, stakeholders, data gaps identification |
| Advisor system | ✓ | 6 persona profiles with registry |
| Argument collector | ✓ | Structured argument generation |
| Conflict resolver | ✓ | Pairwise stance comparison, conflict classification |
| Reflection node | ✓ | Meta-cognitive check: coverage, consistency, red flags |

### P2: Wisdom Framework ✓

| Component | Status | Description |
|-----------|--------|-------------|
| Principle engine | ✓ | 5 ethical principles with scoring |
| Principle profiles | ✓ | 5 configurable weight profiles |
| Scenario explorer | ✓ | 12 scenarios (4 horizons × 3 biases) |
| Wisdom scorer | ✓ | 6-dimension scoring with weighted formula |
| Verdict generator | ✓ | Decision rules + structured verdict |

### P3: Memory Intelligence ✓

| Component | Status | Description |
|-----------|--------|-------------|
| Collective Wisdom Memory | ✓ | Case storage, outcome tracking, similarity search |
| Decision report | ✓ | Structured JSON + human-readable text |
| Explainability | ✓ | Full audit trail from question to verdict |

---

## Current Status

All core deliberation components are implemented and tested (64 tests, 84% coverage). The system can run a complete 9-step deliberation pipeline using simulated advisor evaluations.

**What works today:**
- Full 9-step LangGraph pipeline end-to-end
- 6 advisor personas with criteria-based evaluation
- Conflict detection and classification
- Principle evaluation with 5 configurable profiles
- 12-scenario exploration with assumptions tracking
- Reflection with perspective coverage and consistency checks
- 6-dimension wisdom scoring
- Structured decision report generation
- In-memory collective wisdom case storage
- REST API endpoints (deliberate, advisors, sessions)
- WebSocket streaming for real-time progress
- Next.js frontend with live session tracking and report visualization

**Not yet connected (planned next):**
- Real LLM provider calls (OpenAI, Anthropic adapters need API keys; Ollama is local-only)
- Database persistence (PostgreSQL + pgvector)
- User authentication and multi-tenancy

---

## Future Phases

### P4: Evaluation & Benchmarking (Next)

**Goal:** Prove that Sabdo Pandito Ratu produces better decisions than a single LLM.

| Task | Deliverable |
|------|-------------|
| Decision benchmark dataset | 20+ test cases across domains |
| Single LLM baseline | Compare verdict from GPT-4/Claude alone vs deliberation |
| Conflict detection accuracy | Human evaluation of detected conflicts |
| Principle coverage test | Verify all 5 principles are evaluable on all cases |
| Reflection quality metric | % of cases where reflection catches genuine blind spots |
| Public decision reports | Publish 3+ example reports on GitHub |

### P5: Production Platform

**Goal:** Make the system deployable and usable by external users.

| Task | Deliverable |
|------|-------------|
| Database integration | PostgreSQL + pgvector for persistent storage |
| User authentication | API key management, JWT-based auth |
| Multi-user support | Session isolation, user-specific case history |
| Rate limiting | Redis-backed rate limiter per API key |
| Dashboard | Decision history, advisor performance metrics |
| PDF report export | Downloadable decision reports |

### P6: Community Intelligence

**Goal:** Build a community around shared decision intelligence.

| Task | Deliverable |
|------|-------------|
| Shared case repository | Public database of anonymized decisions |
| Community advisors | Plugin system for custom advisor personas |
| Decision comparison | Side-by-side comparison of different profiles |
| Feedback loop | Outcome tracking with automated weight tuning |
| API marketplace | Third-party integration support |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LLM provider API changes | Medium | High | Generic HTTP adapters; protocol-based abstraction |
| Deliberation too slow with real LLMs | High | Medium | Parallel advisor calls; streaming responses |
| Low-quality LLM responses | Medium | High | Response schema validation; criteria-based extraction |
| Principle weights contested | High | Low | Configurable profiles; no universal values imposed |
| Scenario exploration dismissed as fake | Medium | Medium | Transparent assumptions + uncertainty levels; no prediction claims |
