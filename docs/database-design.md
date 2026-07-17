# Database Design

## Sabdo Pandito Ratu — PostgreSQL + pgvector

---

## 1. Entity Relationship Diagram

```
┌─────────────────────┐       ┌───────────────────────────┐
│     advisors        │       │   deliberation_sessions   │
├─────────────────────┤       ├───────────────────────────┤
│ id (PK)             │──────┐│ id (PK)                   │
│ name                │      ││ question (TEXT)            │
│ provider            │      ││ context (JSONB)            │
│ model               │      ││ status (ENUM)              │
│ capabilities (JSONB)│      ││ config (JSONB)             │
│ specialization      │      ││ verdict_id (FK → verdicts) │
│ config (JSONB)      │      ││ created_at                │
│ active (BOOL)       │      ││ completed_at              │
│ created_at          │      │└───────────┬───────────────┘
│ updated_at          │      │            │
└─────────────────────┘      │            │
                             │            │
┌─────────────────────┐      │            │
│  advisor_responses  │      │            │
├─────────────────────┤      │            │
│ id (PK)             │      │            │
│ session_id (FK) ────┼──────┘            │
│ advisor_id (FK) ────┼───────────────────┘
│ perspective (JSONB) │                    │
│ arguments (JSONB)   │                    │
│ confidence (FLOAT)  │                    │
│ latency_ms (INT)    │                    │
│ created_at          │                    │
└─────────────────────┘                    │
                                           │
┌─────────────────────┐                    │
│     verdicts        │                    │
├─────────────────────┤                    │
│ id (PK)             │                    │
│ decision (TEXT)     │◄───────────────────┘
│ confidence (FLOAT)  │
│ reasoning (JSONB)   │
│ summary (TEXT)      │
│ scores (JSONB)      │
│ metadata (JSONB)    │
│ created_at          │
└─────────────────────┘

┌─────────────────────┐       ┌─────────────────────┐
│   disagreements     │       │   evidence_scores   │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK)             │
│ session_id (FK)     │       │ session_id (FK)     │
│ type (ENUM)         │       │ argument_id (FK)    │
│ description (TEXT)  │       │ logic_score (FLOAT) │
│ between_advisors    │       │ evidence_score(FLOAT)│
│   (UUID[])          │       │ relevance_score(FLOAT)│
│ resolution (TEXT)   │       │ overall_score (FLOAT)│
│ created_at          │       │ created_at          │
└─────────────────────┘       └─────────────────────┘

┌─────────────────────┐
│   embeddings        │  (pgvector)
├─────────────────────┤
│ id (PK)             │
│ session_id (FK)     │
│ advisor_id (FK)     │
│ content_type (ENUM) │  -- 'question' | 'perspective' | 'argument' | 'verdict'
│ content_hash (TEXT) │
│ embedding (VECTOR)  │  -- 1536d (OpenAI) or 1024d (custom)
│ created_at          │
└─────────────────────┘

CREATE INDEX idx_embeddings_vector ON embeddings
  USING ivfflat (embedding vector_cosine_ops);
```

---

## 2. Table Definitions

### 2.1 `advisors`

Stores metadata about each AI advisor registered in the Intelligence Council.

```sql
CREATE TYPE provider_type AS ENUM ('openai', 'anthropic', 'ollama', 'custom');

CREATE TABLE advisors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    provider        provider_type NOT NULL,
    model           VARCHAR(255) NOT NULL,
    capabilities    JSONB NOT NULL DEFAULT '[]',
    specialization  VARCHAR(255),
    config          JSONB NOT NULL DEFAULT '{}',
    active          BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (provider, model)
);

CREATE INDEX idx_advisors_active ON advisors (active);
CREATE INDEX idx_advisors_provider ON advisors (provider);
```

### 2.2 `deliberation_sessions`

Each user request creates a new session that tracks the full lifecycle.

```sql
CREATE TYPE session_status AS ENUM (
    'pending', 'generating_perspectives', 'collecting_arguments',
    'identifying_disagreements', 'evaluating_evidence', 'scoring',
    'generating_verdict', 'completed', 'failed'
);

CREATE TABLE deliberation_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    context         JSONB NOT NULL DEFAULT '{}',
    status          session_status NOT NULL DEFAULT 'pending',
    config          JSONB NOT NULL DEFAULT '{}',
    verdict_id      UUID REFERENCES verdicts(id) ON DELETE SET NULL,
    error_message   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

CREATE INDEX idx_sessions_status ON deliberation_sessions (status);
CREATE INDEX idx_sessions_created ON deliberation_sessions (created_at DESC);
```

### 2.3 `advisor_responses`

Individual responses from each advisor within a session.

```sql
CREATE TABLE advisor_responses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES deliberation_sessions(id) ON DELETE CASCADE,
    advisor_id      UUID NOT NULL REFERENCES advisors(id) ON DELETE CASCADE,
    perspective     JSONB NOT NULL,
    arguments       JSONB NOT NULL DEFAULT '[]',
    confidence      FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    latency_ms      INTEGER,
    status          VARCHAR(50) NOT NULL DEFAULT 'success',
    error_message   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (session_id, advisor_id)
);

CREATE INDEX idx_responses_session ON advisor_responses (session_id);
CREATE INDEX idx_responses_advisor ON advisor_responses (advisor_id);
```

### 2.4 `verdicts`

Final decision output from the deliberation pipeline.

```sql
CREATE TABLE verdicts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision        TEXT NOT NULL,
    confidence      FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    reasoning       JSONB NOT NULL,
    summary         TEXT NOT NULL,
    scores          JSONB NOT NULL DEFAULT '{}',
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_verdicts_confidence ON verdicts (confidence DESC);
```

### 2.5 `disagreements`

Records identified conflicts between advisor perspectives.

```sql
CREATE TYPE disagreement_type AS ENUM (
    'explicit_conflict', 'nuance_difference', 'consensus', 'incompatible_assumption'
);

CREATE TABLE disagreements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES deliberation_sessions(id) ON DELETE CASCADE,
    type            disagreement_type NOT NULL,
    description     TEXT NOT NULL,
    between_advisors UUID[] NOT NULL,  -- array of advisor IDs
    resolution      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_disagreements_session ON disagreements (session_id);
CREATE INDEX idx_disagreements_type ON disagreements (type);
```

### 2.6 `evidence_scores`

Quantified evaluation of each argument's quality.

```sql
CREATE TABLE evidence_scores (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES deliberation_sessions(id) ON DELETE CASCADE,
    argument_id     UUID NOT NULL,  -- references JSON path in advisor_responses.arguments
    advisor_id      UUID NOT NULL REFERENCES advisors(id) ON DELETE CASCADE,
    logic_score     FLOAT CHECK (logic_score >= 0 AND logic_score <= 1),
    evidence_score  FLOAT CHECK (evidence_score >= 0 AND evidence_score <= 1),
    relevance_score FLOAT CHECK (relevance_score >= 0 AND relevance_score <= 1),
    overall_score   FLOAT CHECK (overall_score >= 0 AND overall_score <= 1),
    rationale       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_evidence_session ON evidence_scores (session_id);
CREATE INDEX idx_evidence_advisor ON evidence_scores (advisor_id);
```

### 2.7 `embeddings`

Vector storage for semantic search and similarity comparison.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TYPE embedding_content_type AS ENUM (
    'question', 'perspective', 'argument', 'verdict'
);

CREATE TABLE embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES deliberation_sessions(id) ON DELETE CASCADE,
    advisor_id      UUID REFERENCES advisors(id) ON DELETE CASCADE,
    content_type    embedding_content_type NOT NULL,
    content_hash    VARCHAR(64) NOT NULL,
    embedding       VECTOR(1536) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_embeddings_l2 ON embeddings
    USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

CREATE INDEX idx_embeddings_cosine ON embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX idx_embeddings_session ON embeddings (session_id);
CREATE INDEX idx_embeddings_type ON embeddings (content_type);
```

---

## 3. Indexing Strategy

| Table                 | Index Type     | Purpose                                    |
|-----------------------|----------------|--------------------------------------------|
| embeddings            | IVFFlat (cosine) | Fast vector similarity search            |
| embeddings            | IVFFlat (L2)     | Alternative distance metric             |
| deliberation_sessions | B-tree (created_at DESC) | Recent sessions query           |
| advisor_responses     | B-tree (session_id) | Fast lookup by session               |
| disagreements         | B-tree (session_id) | Fast lookup by session               |

---

## 4. Partitioning Strategy (Future)

When the system handles >1M deliberations:

- Partition `deliberation_sessions` by `created_at` (monthly ranges)
- Partition `advisor_responses` by `session_id` (reference partitioning)
- Partition `embeddings` by `created_at` (monthly ranges)

---

## 5. Data Retention & Archival

| Data                  | Retention                 | Action                                    |
|-----------------------|---------------------------|-------------------------------------------|
| Active sessions       | Until completed + 30 days | Soft delete, then archive to cold storage |
| Completed verdicts    | Indefinite                | Keep for audit trail                      |
| Embeddings            | 90 days                   | Archive to object storage (S3/MinIO)      |
| Advisor responses     | 90 days                   | Summarize and archive                     |
| Logs                  | 30 days                   | Structured logs to log aggregator         |
