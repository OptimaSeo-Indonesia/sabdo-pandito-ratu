# Development Roadmap

## Sabdo Pandito Ratu — Open Deliberation Operating System (OpenDOS)
### v0.1 → v1.0 → v2.0

**Design principle:**
> Everything must be explainable, replayable, and auditable.

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

## Status Saat Ini

Semua komponen inti deliberasi telah diimplementasikan dan diuji (96 tes lulus). Sistem dapat menjalankan pipa deliberasi 10 langkah lengkap menggunakan evaluasi penasihat simulasi. Irisan vertikal P3.5A (Klaim → Bukti → HasilVerifikasi) selesai dengan spesifikasi, implementasi referensi, contoh mandiri, dan rangkaian uji kepatuhan agnostik bahasa.

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

**Belum terhubung (direncanakan berikutnya):**
- Panggilan penyedia LLM nyata (adaptor OpenAI, Anthropic, DeepSeek, Gemini membutuhkan API key; Ollama hanya lokal)
- Persistensi basis data (PostgreSQL + pgvector)
- Autentikasi pengguna dan RBAC
- Platform evaluasi lintas model (lihat P4)
- Integrasi verifikasi bukti di pipa (P3.5A selesai — model inti, engine, rangkaian uji kepatuhan siap)
- Verifikasi berbantuan LLM (P3.5C)

---

## Future Phases

### P3.5: Trust & Auditability (Next)

**Goal:** Replace self-reported metrics with verified evidence, proper calibration, and cryptographically auditable reports.

**Estimate:** 10–14 weeks (split into 4 internal milestones)

**Dependency structure:**
```
                    ┌─────────────────────────────────────────────┐
                    │  P3.5A: Evidence Foundation (weeks 1–4)     │
                    │  ─────────────────────────────              │
                    │  • Evidence Verification                    │
                    │  • Lightweight Entity Graph                 │
                    │  • Observability (tracing + metrics)        │
                    └──────────────┬──────────────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
  ┌──────────────────────┐ ┌──────────────┐ ┌──────────────────┐
  │ P3.5B: Confidence    │ │ P3.5B: Bias  │ │ P3.5B: Calibration│
  │ Outcome Tracking     │ │ Detection    │ │ Dataset          │
  │ (weeks 3–6)          │ │ (weeks 3–6)  │ │ (weeks 3–6)      │
  └──────────┬───────────┘ └──────┬───────┘ └────────┬─────────┘
             │                    │                   │
             └────────────────────┼───────────────────┘
                                  ▼
                    ┌─────────────────────────────────────┐
                    │  P3.5C: Meta Deliberation           │
                    │  + Auto Dissent (weeks 5–8)         │
                    └────────────────┬────────────────────┘
                                     ▼
                    ┌─────────────────────────────────────┐
                    │  P3.5D: Audit + Versioning          │
                    │  (weeks 7–10)                       │
                    │  • Audit Report + Evidence Graph    │
                    │  • Decision Versioning              │
                    │  • WisdomScore v2                   │
                    └─────────────────────────────────────┘
```

---

#### P3.5A: Fondasi Bukti (minggu 1–4)

**Perubahan strategi (2026-07-22):** Prioritas diurutkan ulang untuk mengurangi risiko sebelum menambahkan fitur.
Lihat `docs/specs/protocol-design-principles.md` untuk konstitusi panduan.

| Prioritas lama | Prioritas baru |
|----------------|----------------|
| Fitur Verifikasi Bukti | Irisan vertikal Klaim→Bukti→HasilVerifikasi |
| Graf Entitas Ringan | Prinsip desain protokol |
| Observabilitas | Rangkaian uji kepatuhan agnostik bahasa |
| — | Percakapan dengan adopter |

**Hasil:** Irisan vertikal Klaim → Bukti → HasilVerifikasi yang lengkap dan dapat diimplementasikan, dengan uji kepatuhan agnostik bahasa.

**Definisi selesai:**
- [x] Spesifikasi untuk Klaim, Bukti, CatatanProvenans, HasilVerifikasi ditulis (`docs/specs/claim-spec-v0.1.md`)
- [x] Prinsip desain protokol ditulis (`docs/specs/protocol-design-principles.md`)
- [x] Implementasi referensi di core (`core/verification/engine.py`, `core/models.py`)
- [x] Contoh mandiri minimal (nol dependensi) (`examples/minimal_verification.py`)
- [x] Rangkaian uji kepatuhan (JSON in/out, agnostik bahasa) (`compliance/runner.py`)
- [x] 5 kasus uji lulus (dasar, tanpa bukti, overlap rendah, campuran, kosong)
- [x] Ringkasan untuk adopter disiapkan (`docs/adopter-brief.md`)
- [ ] **Validasi eksternal:** Setidaknya satu implementor independen menghasilkan Klaim→Bukti→HasilVerifikasi yang kompatibel dari spesifikasi saja
- [ ] **Umpan balik adopter:** Setidaknya 2 percakapan dengan calon adopter selesai

**Ditunda ke P3.5B:**
- Graf Entitas Ringan
- Observabilitas (Tracing + Metrik)
- Perbaikan deteksi kontradiksi

---

#### P3.5B: Confidence & Bias (weeks 3–6)

**Deliverable:** Calibrated confidence scores + bias-aware reflection.

##### 4. Confidence Calibration

**Files to create:**
- `core/deliberation/calibration.py` — `ConfidenceCalibrator` class

**Files to modify:**
- `core/deliberation/reflection.py` — replace `_compute_confidence_adjustment()` method with call to `ConfidenceCalibrator`
- `core/deliberation/graph.py` — pass calibrator to `ReflectionNode`
- `pyproject.toml` — add `scikit-learn>=1.3` dependency (for Platt scaling)
- `tests/test_calibration.py` — new test file

**Implementation approach:**
1. **Platt scaling:** Fit a logistic regression model on (base_confidence, evidence_ratio) → calibrated_confidence. Start with a hand-labeled seed dataset of 200 verdicts.
2. **Outcome tracking for calibration:** Add optional `outcome` field to `CaseMemory` in `CollectiveWisdomMemory`. Track `{ prediction, confidence, actual_outcome }` triplets. Use these to periodically re-fit calibration models. Without outcomes, calibration uses held-out synthetic data with known ground truth.
3. **Per-dimension calibration:** Calibrate each of the 6 WisdomScore dimensions independently.
4. **Bayesian calibration (optional):** For cases with sparse data, use Bayesian beta calibration instead of Platt scaling.

**Success criteria:**
- Calibrated probabilities are well-calibrated (Brier score < 0.1 on held-out test set)
- Outcome tracking captures ≥90% of user-reported outcomes
- Confidence does not degrade from current baseline (average confidence ±5%)

---

##### 5. Bias Detection

**Files to create:**
- `core/deliberation/bias.py` — `BiasDetector` class (stereotype, framing, representation, groupthink checks)

**Files to modify:**
- `core/deliberation/reflection.py` — integrate `BiasDetector` into `reflect()` method; emit `bias_flags` in reflection output
- `core/models.py` — add `BiasFlag { bias_type, severity, description, affected_personas }` model
- `tests/test_bias.py` — new test file

**Implementation approach:**
1. **Groupthink detection:** If all 6 advisor stances are identical AND confidence is uniformly high → flag as potential groupthink. Confidence penalty −0.15.
2. **Stereotype detection:** Pattern matching against known stereotype indicators. **Benchmark datasets for validation:** BBQ (Bias Benchmark for QA), StereoSet, CrowS-Pairs, MMLU Ethics, TruthfulQA. Run BiasDetector on these datasets to establish baseline precision/recall before production use.
3. **Framing detection:** Detect if the question/context uses loaded language that primes a particular stance. Compare advisor responses against neutral reframing.
4. **Representation check:** If all advisors rely on the same type of evidence (e.g., all quantitative, no qualitative), flag as evidence narrowness.

**Success criteria:**
- Detects synthetic groupthink in ≥70% of test cases
- Bias flags have ≥75% precision (human audit)
- Zero false positives on neutral cases
- Baseline established on BBQ/StereoSet before production deployment

---

##### 6. Auto-Create Dissenting Persona

**Files to create:**
- `core/advisors/dissent.py` — `DissentingPersonaFactory` class

**Files to modify:**
- `core/advisors/personas.py` — register dissenting persona as a dynamic persona (not in `default_profiles`)
- `core/advisors/registry.py` — add methods `spawn_dissenter()` and `remove_temporary()`
- `core/deliberation/graph.py` — after Bias Detection, if groupthink detected, call `registry.spawn_dissenter()` and re-run `generate_perspectives` for the dissenter only
- `tests/test_dissent.py` — new test file

**Implementation approach:**
1. **Dissenter prompt inversion:** Take the majority stance, invert it. Generate a system prompt that explicitly argues the counter-position.
2. **Dynamic persona:** The dissenter is not a fixed persona; it is constructed on-the-fly with priority weights flipped from the majority's inferred values.
3. **Re-deliberation:** Only re-run the dissenter through `generate_perspectives`, then re-run `collect_arguments` and `resolve_conflicts` with the new dissenter's output merged in.

**Success criteria:**
- Dissenter produces a coherent counter-argument in ≥90% of invocations
- Adding dissenter changes the final verdict stance in ≥30% of groupthink cases

---

#### P3.5C: Meta Deliberation (weeks 5–8)

**Deliverable:** Self-critiquing deliberation loop.

##### 7. Meta Deliberation

**Files to create:**
- `core/deliberation/meta.py` — `MetaDeliberator` class

**Files to modify:**
- `core/deliberation/graph.py` — add `meta_deliberation` step after `generate_verdict`; add re-deliberation loop logic
- `core/models.py` — add `MetaReview { quality_scores, re_deliberate, reason }` model; add `deliberation_round` counter
- `tests/test_meta.py` — new test file

**Implementation approach:**
1. **Quality scoring:** After verdict, compute 5 quality dimensions: advisor_diversity (0–1), evidence_strength (average evidence ratio), risk_coverage (% of scenario horizons explored), confidence_level (calibrated confidence), data_gap_ratio (gaps / total claims).
2. **Re-deliberation trigger:** If composite quality < threshold (configurable, default 0.6), increment `deliberation_round`. If rounds < 3, re-run from `generate_perspectives` with improved config (add dissenter, request more evidence, explore missing horizons).
3. **Loop guard:** Hard cap of 3 re-deliberations. After cap, force exit with best-yet verdict and a warning in the report.
4. **Timeline:** Each re-deliberation is logged as a new entry in the case timeline.

**Success criteria:**
- Meta Deliberation improves composite quality score by ≥15% on average
- ≥80% of re-deliberations produce a measurably better verdict (higher WisdomScore)
- ≥95% of cases terminate within 3 rounds (no infinite loops)

---

#### P3.5D: Audit & Versioning (weeks 7–10)

**Deliverable:** Cryptographically auditable decision trail with versioned outputs.

##### 8. Audit Report + Evidence Graph

**Files to create:**
- `core/explainability/audit.py` — `AuditReportBuilder` class
- `core/explainability/graph.py` — `EvidenceGraph` builder (verdict → facts → assumptions → risks → ethical values)

**Files to modify:**
- `core/explainability/reporter.py` — integrate `AuditReportBuilder` output into `generate_report()`
- `core/models.py` — add `AuditEntry { hash, prev_hash, timestamp, action, data }`; add `UncertaintyReport` model
- `apps/api/routes/deliberations.py` — add `GET /deliberate/{id}/audit` endpoint returning audit chain
- `apps/web/src/` — add Evidence Graph visualization component (D3.js or vis-network)

**Implementation approach:**
1. **Audit chain:** Each deliberation step produces an `AuditEntry` with SHA-256 hash of its data + previous step's hash. Store as linked list on state.
2. **Evidence Graph:** Build a directed graph: root = verdict → child = evidence clusters → grandchild = source claims, assumptions, risks → leaf = ethical values impacted. Uses the Entity Graph from P3.5A as backbone.
3. **Uncertainty Report:** Collect all `data_gaps` from `ContextAnalysis`, all `unsupported` claims from `EvidenceVerification`, and all `assumptions` from advisor responses. Compile into a single "What we do NOT know" section.
4. **Audit API:** `GET /deliberate/{id}/audit` → returns full audit chain (JSON). `GET /deliberate/{id}/audit/graph` → returns evidence graph nodes + edges.

**Success criteria:**
- Audit chain is cryptographically verifiable (any tampering breaks the hash chain)
- Evidence graph accurately represents all claims and their provenance
- Uncertainty Report captures ≥90% of known data gaps

---

##### 9. Decision Versioning

**Files to create:**
- `core/versioning/__init__.py`
- `core/versioning/manager.py` — `DecisionVersionManager` class

**Files to modify:**
- `core/models.py` — add `DecisionVersion { version_id, parent_id, inputs_hash, prompt_version, model_version, policy_version, evidence_version, timestamp }`
- `core/memory/store.py` — store version info alongside each case
- `apps/api/routes/deliberations.py` — add `GET /deliberate/{id}/versions` and `POST /deliberate/{id}/versions/rollback/{version}`

**Implementation approach:**
1. Each deliberation snapshot includes: input question hash, system prompt version, model version(s) for each advisor, policy/principle profile version, evidence verification version.
2. Version tree: parent → child relationships across re-deliberations. Enables precise replay: given a `version_id`, the exact same inputs produce the exact same output.
3. Rollback endpoint: retrieve a previous version's verdict and report without re-running.

**Success criteria:**
- Every deliberation produces a unique, reproducible version hash
- Rollback correctly restores the previous version's verdict
- Version tree correctly captures re-deliberation ancestry

---

##### 10. WisdomScore v2

**Files to modify:**
- `core/evaluation/scorer.py` — rewrite `_score_evidence_quality()` to use `EvidenceSupportRatio` and `EvidenceCoverage` from `EvidenceVerifier`
- `core/models.py` — update `WisdomScore` dimensions to include `evidence_support_ratio`, `evidence_coverage`, `unsupported_claim_ratio`
- `tests/test_scorer.py` — update tests for new dimension definitions

**Implementation approach:**
1. **Replace self-reported evidence:** Old: `evidence_quality = avg(advisor.confidence) * 0.6 + has_data_sources * 0.4`. New: `evidence_support_ratio = verified_claims / total_claims`.
2. **Add coverage metric:** `evidence_coverage = distinct_sources / total_claims`. A score of 1.0 means every claim has a unique source.
3. **Add unsupported ratio:** `unsupported_claim_ratio = unsupported_claims / total_claims`. Lower is better. Inverted for scoring.

**Success criteria:**
- New evidence dimensions are more predictive of human-judged evidence quality than old self-reported metric (correlation > 0.6)
- Backward compatibility: old verdicts can be re-scored without error

**P3.5 Definition of Done:**
- [ ] All 10 tasks complete with passing tests
- [ ] Pipeline test: deliberation with evidence verification adds <15% latency overhead
- [ ] Audit chain test: hash verification passes on 100 random deliberation states
- [ ] Calibration test: Brier score < 0.1 on held-out test set
- [ ] Versioning test: exact replay produces identical output
- [ ] Observability: all pipeline nodes have span traces

---

### P3.8: Knowledge Intelligence

**Goal:** Sabdo doesn't just store memories — it discovers patterns, extracts lessons, and recommends precedents across thousands of decisions.

**Estimate:** 6–10 weeks

**Dependency:** Requires P3.5D (Audit Report for case data, Meta Deliberation for timeline, Entity Graph from P3.5A as seed)

---

#### 1. Knowledge Graph

**Files to create:**
- `core/knowledge/__init__.py`
- `core/knowledge/graph.py` — `DecisionKnowledgeGraph` class (nodes: decision, entity, domain, stakeholder, principle, verdict; edges: references, trades_off, impacts, evaluates)

**Files to modify:**
- `core/memory/store.py` — integrate knowledge graph alongside vector similarity
- `pyproject.toml` — add `networkx>=3.0` dependency
- `tests/test_knowledge_graph.py` — new test file

**Implementation approach:**
1. Use NetworkX as the in-memory graph backend
2. Each deliberation populates: decision node → entity nodes (from context analysis) → domain node → stakeholder nodes → principle nodes (from principle evaluation) → verdict node
3. Edges: `references` (claim → entity), `trades_off` (principle ↔ principle), `impacts` (scenario → stakeholder)
4. Graph traversal queries: "Which principles trade off most often in healthcare decisions?"

**Success criteria:**
- Graph builds correctly for all past and new cases
- Graph traversal queries return in <100ms for 1000+ cases
- Exportable to GraphML for visualization

---

#### 2. Case Clustering

**Files to create:**
- `core/knowledge/clustering.py` — `CaseClusterer` class

**Files to modify:**
- `core/knowledge/graph.py` — add cluster tags to decision nodes
- `tests/test_clustering.py` — new test file

**Implementation approach:**
1. Feature vector per case: [domain_onehot, stance_counts (6), principle_scores (5), conflict_types (5), verdict_binary]
2. Apply HDBSCAN or K-Means (configurable) on the feature space
3. Assign cluster_id to each case; store in knowledge graph
4. Visualize cluster composition (domain × verdict cross-tab)

**Success criteria:**
- ≥5 interpretable clusters on a dataset of 200+ synthetic cases
- Silhouette score > 0.3
- Each cluster has a human-readable label (e.g., "high-risk regulatory denials")

---

#### 3. Pattern Discovery

**Files to create:**
- `core/knowledge/patterns.py` — `PatternDiscoverer` class

**Files to modify:**
- `tests/test_patterns.py` — new test file

**Implementation approach:**
1. Association rule mining (Apriori / FP-Growth) on case features
2. Discover rules: `{persona: DEVILS_ADVOCATE, stance: no} → {verdict: do_not_proceed}` with confidence/lift
3. Discover principle trade-off patterns: `{high: sustainability} → {low: economic_growth}` across cases
4. Output: ranked list of discovered patterns with support, confidence, lift

**Success criteria:**
- Discovers ≥10 non-trivial patterns from 200+ synthetic cases
- Patterns have minimum support 0.05, minimum confidence 0.6
- No patterns that are obvious statistical artifacts (verified by human review)

---

#### 4. Precedent Recommendation

**Files to create:**
- `core/knowledge/precedent.py` — `PrecedentRecommender` class

**Files to modify:**
- `apps/api/routes/deliberations.py` — add `GET /deliberate/{id}/precedents`
- `apps/web/src/` — add precedent display panel
- `tests/test_precedent.py` — new test file

**Implementation approach:**
1. Given a new case, compute similarity to all past cases: weighted combination of (0.4 × vector similarity from `CollectiveWisdomMemory`) + (0.3 × knowledge graph distance) + (0.2 × domain match) + (0.1 × stakeholder overlap)
2. Return top-K (default 5) most similar past cases with: similarity score, verdict, confidence, outcome (if tracked)
3. Include a brief "why similar" explanation (shared domain, same stakeholders, similar conflict pattern)

**Success criteria:**
- Top-1 recommendation matches human expert judgment ≥60% of the time (evaluated on 50 cases)
- API response time <200ms with 1000 indexed cases
- Recommendation quality improves as more cases are added (monotonic)

---

#### 5. Lessons Learned Extraction

**Files to create:**
- `core/knowledge/lessons.py` — `LessonsExtractor` class

**Files to modify:**
- `core/knowledge/precedent.py` — integrate lessons into precedent display
- `tests/test_lessons.py` — new test file

**Implementation approach:**
1. For cases where outcome is tracked (success/failure), compare predicted verdict vs actual outcome
2. Extract: "What went as expected", "What surprised", "What we would do differently"
3. Template-based generation using case data: stance agreement vs actual, principle weights vs outcome
4. If LLM available: use structured prompt to generate natural-language lessons from case diff

**Success criteria:**
- Extracts ≥3 lessons per case with tracked outcomes
- Lessons are factually grounded (each statement links back to case data)
- No hallucinated lessons (verified by human audit on 50 cases)

---

#### 6. Decision Timeline

**Files to create:**
- `core/knowledge/timeline.py` — `DecisionTimelineBuilder` class

**Files to modify:**
- `apps/api/routes/deliberations.py` — add `GET /deliberate/{id}/timeline`
- `apps/web/src/` — add timeline visualization component
- `tests/test_timeline.py` — new test file

**Implementation approach:**
1. Each deliberation round produces a snapshot: `{ round, verdict, wisdom_score, confidence, key_changes }`
2. Key changes between rounds: stance flips, new evidence, scenario focus shift, principle weight adjustments
3. Visual: Gantt-like timeline with round markers, color-coded by verdict direction

**Success criteria:**
- Timeline accurately captures all re-deliberation rounds
- Key changes are identified with ≥80% accuracy (human audit)
- API response <50ms per case

**P3.8 Definition of Done:**
- [ ] Knowledge graph builds and queries correctly
- [ ] Case clustering produces ≥5 interpretable clusters
- [ ] Precedent recommendation returns relevant past cases in <200ms
- [ ] Lessons extracted for all cases with tracked outcomes
- [ ] Timeline renders correctly for single and multi-round cases
- [ ] All new modules have ≥80% test coverage

---

### P4: Evaluation Platform & Cross-Model Benchmarking

**Goal:** Turn deliberation into a benchmarking engine — compare quality, consistency, cost, and latency across any model configuration systematically.

**Estimate:** 8–12 weeks

**Dependency:** Requires P3.5 (evidence verification, calibration, audit)

**Metrics per configuration:** Agreement Score, Diversity Score, Reasoning Depth, Evidence Coverage, Unsupported Claim Ratio, Cost, Latency, Token Efficiency. Output: radar chart + leaderboard.

---

#### 1. Decision Benchmark Dataset

**Files to create:**
- `benchmarks/__init__.py`
- `benchmarks/cases/` — directory of YAML/JSON case files, organized by domain subdirectories
- `benchmarks/registry.py` — `BenchmarkRegistry` to load and query cases
- `benchmarks/templates/` — case template (question, context, domain, stakeholders, expected_considerations)

**Implementation approach:**
1. Curate 20+ cases across 5 domains: business (5), policy (5), ethics (5), technology (3), personal (2)
2. Each case is a YAML file in a domain subdirectory: `benchmarks/cases/healthcare/case-001.yaml`, `benchmarks/cases/finance/case-002.yaml`, etc.
3. Each case includes: `id`, `domain`, `question`, `context`, `stakeholders`, `urgency`, `principle_profile`, `tags`, plus optional `expected_principles` and `expected_conflict_types`.
4. Registry auto-discovers cases from `benchmarks/cases/`. Community can add new domains by creating new subdirectories.

**Dataset Registry structure:**
```
benchmarks/
├── registry.py           # BenchmarkRegistry
├── templates/
│   └── case.yaml         # Case template
├── cases/
│   ├── business/         # 5 cases
│   ├── policy/           # 5 cases
│   ├── ethics/           # 5 cases
│   ├── technology/       # 3 cases
│   └── personal/         # 2 cases
└── bias/                 # Bias evaluation datasets
    ├── bbq/              # BBQ-derived test cases
    ├── stereoset/        # StereoSet-derived
    └── truthfulqa/       # TruthfulQA-derived
```

**Success criteria:**
- All 5 domains represented with ≥2 cases each
- Each case triggers at least 4 of 6 advisor personas with distinct stances
- Benchmark dataset is versioned and extensible (add new case = add YAML file)
- Bias datasets loadable and runnable through the same cross-model runner

---

#### 2. Cross-Model Runner

**Files to create:**
- `benchmarks/runner.py` — `BenchmarkRunner` class
- `benchmarks/configs/` — predefined configurations: `dry_run.yaml`, `gpt4.yaml`, `deepseek.yaml`, `gemini.yaml`, `mixed.yaml`

**Files to modify:**
- `apps/api/routes/deliberations.py` — add `POST /benchmark/run` endpoint
- `pyproject.toml` — add `rich` dependency for CLI output
- `tests/test_benchmark_runner.py` — new test file

**Implementation approach:**
1. **Phase 1 — Configuration-driven:** Each benchmark config specifies: `mode`, `per_persona_model_overrides` (for mixed mode), `budget`, `max_rounds`
2. **Phase 2 — Batch execution:** Runner iterates over all configs × all cases. For each combination, run deliberation, collect results, store in `BenchmarkResult`.
3. **Phase 3 — CLI:** `sabdo benchmark run --configs dry_run,gpt4 --cases all --output results.json`
4. **Phase 4 — API:** `POST /benchmark/run` with JSON body specifying configs and case IDs; returns async job ID; `GET /benchmark/jobs/{id}` for progress.

**Supported configurations:**
| Config | Description |
|--------|-------------|
| `dry_run` | No LLM calls, pure heuristic |
| `gpt4` | All personas via GPT-4 |
| `deepseek` | All personas via DeepSeek |
| `gemini` | All personas via Gemini |
| `claude` | All personas via Claude |
| `mixed_gpt_deepseek` | Rational/ECONOMIC via GPT, Humanitarian/Legal via DeepSeek |
| `mixed_local_cloud` | Sensitive personas local (Ollama), others cloud |
| `cost_optimized` | Auto-select cheapest per-persona that meets quality threshold |
| `lowest_latency` | Auto-select fastest per-persona |

**Integration point:** Uses existing `DeliberationGraph` with mode override. Does not modify the core pipeline.

---

#### 3. Single LLM Baseline Comparison

**Files to create:**
- `benchmarks/baseline.py` — `BaselineComparator` class

**Files to modify:**
- `benchmarks/runner.py` — integrate baseline as an automatic step in benchmark runs
- `tests/test_baseline.py` — new test file

**Implementation approach:**
1. For each case, also run the question directly through each LLM (no deliberation): "Answer this question with a yes/no stance and reasoning."
2. Parse the raw LLM response into a pseudo-verdict.
3. Compare: WisdomScore of deliberation verdict vs pseudo-verdict; stance agreement; evidence coverage; bias flags.
4. Delta metrics: `improvement = deliberation_score - raw_llm_score`

---

#### 4. Cost & Latency Analytics + Optimizer

**Files to create:**
- `benchmarks/cost.py` — `CostAnalyzer` class
- `benchmarks/optimizer.py` — `ConfigOptimizer` class (what-if recommendations)

**Implementation approach:**
1. **Cost tracking:** Each benchmark run records per-persona: model, tokens in/out, latency, cost (from model pricing table).
2. **Aggregation:** Per-config totals and averages: total_cost, avg_latency, cost_per_quality_point.
3. **What-if optimizer:** Given a benchmark result, compute: "If we replaced {model_X} with {model_Y} on {persona_Z}, cost changes by A%, quality changes by B%."
4. **Output:** Comparison tables (rich CLI tables + JSON) sorted by cost, quality, or cost/quality ratio.

---

#### 5. Cost-Aware Intelligent Model Router

**Files to modify:**
- `core/inference/selection.py` — enhance `BackendSelector.select()` with new routing dimensions
- `core/inference/adapter.py` — add `cost_per_token`, `avg_latency_ms` to `InferenceCapabilities`
- `core/models.py` — add `RoutingConstraints { max_cost, max_latency, data_sensitivity, preferred_providers }` model

**New routing dimensions:**
| Dimension | Source | Behavior |
|-----------|--------|----------|
| Cost budget | `RoutingConstraints.max_cost` | Exclude models exceeding budget |
| Latency tolerance | `RoutingConstraints.max_latency` | Exclude models slower than threshold |
| Data sensitivity | `RoutingConstraints.data_sensitivity` | `low` → any provider; `medium` → local or trusted providers only; `high` → local only |
| Historical performance | `InferenceRegistry.verified` | Prefer models with higher `avg_wisdom_contribution` for similar task types |
| Task type | `CapabilityRequirement` | Match model strengths to task type (reasoning, numerical, ethical, etc.) |

---

#### 6. Cross-Model Agreement Metrics

**Files to create:**
- `benchmarks/agreement.py` — `AgreementAnalyzer` class

**Metrics computed:**
1. **Stance agreement:** % of configurations that produce the same stance (yes/cautious_yes/cautious_no/no)
2. **Conflict pattern similarity:** Jaccard similarity of conflict sets across configurations
3. **WisdomScore stability:** Standard deviation of overall WisdomScore across configurations
4. **Persona-level agreement:** For each persona, how often it gives the same stance across different model backends
5. **Krippendorff's alpha:** Inter-rater reliability across model configurations (treat each config as a "rater")

---

#### 7. Radar Chart & Leaderboard

**Files to create:**
- `apps/web/src/components/benchmark/` — RadarChart, Leaderboard, ConfigComparisonTable components
- `apps/api/routes/benchmarks.py` — benchmark results endpoints

**Implementation approach:**
1. Radar chart: 8 axes (one per metric), one polygon per configuration. Normalize each axis to 0–100.
2. Leaderboard: Sort configurations by configurable composite score (user can weight each dimension).
3. Comparison table: Side-by-side metric values with color coding (green = best, red = worst per metric).
4. Distribution plot: Box plot of WisdomScore across configurations.

---

#### 8. Public Model Comparison Report + Academic Paper

**Deliverable:** Published report (GitHub Pages + PDF) + academic paper submission.

**Report contents:**
1. Methodology: benchmark dataset, configurations, metrics
2. Results per domain: radar charts, leaderboard
3. Cost-quality analysis: Pareto frontier of cost vs quality
4. Model-persona fit: which models excel at which roles
5. Deliberation vs single LLM: when deliberation adds value
6. Key findings: top 5 insights from the benchmark

**Paper target venues:**
- NeurIPS Datasets & Benchmarks track
- ACL (Ethics / NLP for Social Good)
- FAccT (Fairness, Accountability, Transparency)
- arXiv preprint for community feedback

**Paper outline:**
1. Introduction — problem with single-LLM decisions
2. The Sabdo deliberation framework
3. Benchmark methodology — 20+ cases, 9 model configurations, 8 metrics
4. Results — radar charts, leaderboard, statistical analysis
5. Analysis — when deliberation beats single LLM, model-persona fit
6. Limitations and future work

**P4 Definition of Done:**
- [ ] All 8 tasks complete
- [ ] Cross-model runner can execute all configs on all benchmark cases
- [ ] Radar chart and leaderboard render correctly for ≥5 configurations
- [ ] Public report published with ≥20 benchmark cases
- [ ] Cost what-if optimizer gives correct recommendations (validated against manual calculation)
- [ ] Paper preprint submitted to arXiv

---

### P5: Production Platform (v1.0 Core)

**Goal:** Make the system deployable and usable by external teams — focus on essentials for open source adoption.

**Estimate:** 8–12 weeks

**Implementation order:** Database → API Key Management → RBAC → Audit Log → Decision Search → PDF Export.

| Priority | Task | Approach | Key Files |
|----------|------|----------|-----------|
| 1 | **Database integration** | Move from in-memory to PostgreSQL via SQLAlchemy. Alembic migrations for all models. pgvector for similarity search. Connection pooling with asyncpg. | `apps/api/db/`, Alembic migrations |
| 2 | **API key management** | Generate prefixed keys (`sabdo_sk_xxx`). Hash stored (SHA-256). Track usage: last_used_at, total_requests, rate_limit_bucket. Rate limiting via Redis sliding window. | `apps/api/auth.py`, `core/auth/api_keys.py` |
| 3 | **RBAC** | Org isolation via `org_id` on all entities. Teams within org. Roles: `admin` (full control), `editor` (run deliberations, view org data), `viewer` (read-only). Permission checks as FastAPI dependency. | `apps/api/rbac.py`, `core/auth/models.py` |
| 4 | **Enterprise audit log** | Immutable append-only log table in PostgreSQL. Every state mutation records: `actor_id, action, resource_type, resource_id, old_state, new_state, timestamp, ip_address`. No UPDATE/DELETE on log rows. | `apps/api/audit.py`, `db/migrations/` |
| 5 | **Decision search** | Full-text search (PostgreSQL `tsvector` on question, summary, verdict). Filters: domain, stakeholder, persona, date range, verdict type. Paginated results. | `apps/api/routes/sessions.py`, SQLAlchemy full-text search |
| 6 | **PDF report export** | Server-side PDF generation (WeasyPrint or ReportLab). Template: executive summary, deliberation details, evidence graph, audit annex. Background job for async generation. | `apps/api/export/pdf.py` |

**Deferred to v1.1 (post-MVP):**
| Feature | Rationale |
|---------|-----------|
| **Secret management** | Environment variables sufficient for initial deployments |
| **Governance Dashboard** | UI nicety — core pipeline and API are more critical |
| **SSO/SAML** | Most teams use API keys or basic auth first |
| **On-premise mode** | Docker Compose already works; standalone SQLite mode can wait |

**P5 Definition of Done:**
- [ ] PostgreSQL migration with zero data loss from in-memory
- [ ] API key auth with rate limiting
- [ ] Org-scoped RBAC with admin/editor/viewer roles
- [ ] Immutable audit log for all state mutations
- [ ] Full-text decision search returns results in <500ms
- [ ] PDF export produces valid, well-formatted documents

---

### P6A: Community Intelligence — Foundation

**Goal:** Build an open community around shared decision intelligence.

**Estimate:** 6–8 weeks

| Task | Approach | Key Files |
|------|----------|-----------|
| **Shared case repository** | Public PostgreSQL schema with anonymized cases. Opt-in publishing from org dashboard. Cases stripped of PII before publishing. Browse, search, filter public cases. | `apps/api/routes/community.py`, `core/community/anonymizer.py` |
| **Community feedback** | Registered users can upvote/downvote verdicts, leave comments on reasoning. Voting history tracked to prevent abuse. Comment threading. | `apps/api/routes/community.py`, `db/migrations/` |
| **Public benchmark** | Community-contributed test cases via PR to `benchmarks/cases/`. Auto-run benchmark on merge. Public leaderboard of model performance. | `benchmarks/community/`, `apps/web/src/pages/leaderboard/` |
| **Decision comparison** | Side-by-side view of two verdicts on same case with different principle profiles. Highlight: stance differences, principle score deltas, conflict pattern changes. | `apps/web/src/components/compare/`, `apps/api/routes/compare.py` |

**P6A Definition of Done:**
- [ ] Public case repository searchable and browsable
- [ ] Feedback system (upvote + comments) functional and abuse-resistant
- [ ] Community benchmark pipeline auto-runs on PR merge
- [ ] Decision comparison view renders side-by-side correctly

---

### P6B: Community Intelligence — Marketplace

**Goal:** Extensible plugin ecosystem for advanced use cases.

**Estimate:** 8–10 weeks

**Dependency:** P6A

| Task | Approach | Key Files |
|------|----------|-----------|
| **Plugin SDK** | Type-safe Python SDK (`sabdo-sdk` package). Abstract base classes: `BaseAdvisor`, `BaseEvaluator`, `BaseReporter`. Plugin discovery via entry_points. Versioned API contract. | `packages/sabdo-sdk/` |
| **Plugin Sandbox** | Each plugin runs with declared `Permissions { needs_network, needs_filesystem, max_memory_mb, timeout_s }`. Sandbox executes in isolated subprocess with resource limits (RLIMIT_AS, RLIMIT_CPU). Network access blocked by default. Malicious plugin detection via static analysis on registration. | `core/plugins/sandbox.py`, `core/plugins/security.py` |
| **Community advisors** | Plugin system loads advisors from `pip install sabdo-advisor-{name}`. Registry auto-discovers installed plugins. Sandboxed execution via Plugin Sandbox. | `core/advisors/plugin.py` |
| **Outcome feedback loop** | Track real decisions and their actual outcomes (success/failure/neutral). Periodically re-tune principle weights using Bayesian optimization to maximize outcome alignment. Requires opt-in outcome reporting. | `core/feedback/optimizer.py` |
| **API marketplace** | Webhook triggers on deliberation complete. Integration templates: Slack notification, Jira ticket creation, Notion database entry, Google Sheets logging. Community-contributed integrations. | `apps/api/integrations/`, `core/integrations/registry.py` |

**P6B Definition of Done:**
- [ ] Plugin SDK published on PyPI
- [ ] At least 2 community advisors built with the SDK
- [ ] Outcome feedback loop functional on ≥100 tracked outcomes
- [ ] ≥3 API integrations working (Slack, Jira, Notion)

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LLM provider API changes | Medium | High | Generic HTTP adapters; protocol-based abstraction |
| Deliberation too slow with real LLMs | High | Medium | Parallel advisor calls; streaming responses |
| Low-quality LLM responses | Medium | High | Response schema validation; criteria-based extraction |
| Principle weights contested | High | Low | Configurable profiles; no universal values imposed |
| Scenario exploration dismissed as fake | Medium | Medium | Transparent assumptions + uncertainty levels; no prediction claims |
| Meta Deliberation infinite loop | Low | Medium | Max re-deliberation limit (3×); human-in-the-loop break after limit |
| Cost optimizer misleads with incomplete data | Medium | Medium | Confidence intervals on savings estimates; disclaimer that quality metrics are estimated |
| **P3.5 scope too large** | High | Medium | Split into 4 internal milestones (A/B/C/D); each milestone independently usable |
| Bias benchmark validation incomplete | Medium | Medium | Use BBQ/StereoSet first; clearly document known limitations |
| Calibration unprovable without outcomes | Medium | High | Seed dataset of 200 synthetic ground-truth cases; add outcome tracking infrastructure early |
| Knowledge graph too slow at scale | Low | Medium | Lazy loading; graph partitioning by domain; fallback to vector search |
| Plugin sandbox bypass | Low | High | Subprocess isolation; resource limits; code review for all published plugins |
| Plugin SDK backward compatibility | Medium | High | Semantic versioning; deprecation policy; breaking changes in major versions only |

---

## Beyond v1.0 — Long-Term Vision

### v1.0 Milestone

All phases from P0 through P6B complete. Sabdo Pandito Ratu is a production-ready **Open Deliberation Operating System (OpenDOS)** that is explainable, replayable, and auditable.

### v2.0 Horizons

| Phase | Focus |
|-------|-------|
| **P7: Autonomous Advisors** | Advisors that learn from past cases, auto-tune their evaluation criteria, and specialize in domains over time |
| **P8: Organizational Learning** | Cross-organization pattern discovery, industry-specific principle profiles, federated deliberation |
| **P9: Collective Intelligence** | Network of Sabdo instances sharing anonymized insights; meta-benchmarking across organizations |

### Positioning (audience-specific)

| Audience | Positioning |
|----------|-------------|
| Technical | **Open Deliberation Operating System (OpenDOS)** — deliberation, evaluation, and governance layer that is LLM-agnostic |
| Architectural | **Decision Orchestration Layer** — sits between models and applications, managing quality and accountability |
| Business | **Decision Intelligence Platform** — auditable, explainable, multi-model decision engine for enterprise governance |
