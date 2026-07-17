# API Design

## Sabdo Pandito Ratu — REST & WebSocket API Specification

---

## 1. Base URL

```
Development:  http://localhost:8000/api/v1
Production:   https://api.sabdo-pandito-ratu.dev/api/v1
```

All endpoints return JSON. Authentication is via `X-API-Key` header (future: OAuth2).

---

## 2. Core Endpoints

### 2.1 Start a Deliberation

Initiates a multi-advisor deliberation process.

```
POST /api/v1/deliberate
```

**Request Body:**

```json
{
  "question": "Should our startup pivot from B2C to B2B?",
  "context": {
    "industry": "edtech",
    "region": "SEA",
    "company_stage": "seed",
    "metrics": {
      "mrr": 5000,
      "churn_rate": 0.12,
      "cac": 45,
      "ltv": 180
    }
  },
  "config": {
    "advisors": ["gpt-4", "claude-3-opus", "llama-3-70b"],
    "debate_rounds": 2,
    "judge": "claude-3-opus",
    "return_full_report": true,
    "timeout_seconds": 60
  }
}
```

**Response (202 Accepted):**

```json
{
  "session_id": "sess_a1b2c3d4",
  "status": "pending",
  "status_url": "/api/v1/deliberate/sess_a1b2c3d4",
  "estimated_completion_seconds": 25
}
```

### 2.2 Get Deliberation Status

```
GET /api/v1/deliberate/{session_id}
```

**Response:**

```json
{
  "session_id": "sess_a1b2c3d4",
  "question": "Should our startup pivot from B2C to B2B?",
  "status": "completed",
  "progress": {
    "current_step": "generate_verdict",
    "steps_completed": 5,
    "steps_total": 6
  },
  "advisor_statuses": [
    {
      "advisor_id": "gpt-4",
      "status": "completed",
      "confidence": 0.82,
      "latency_ms": 3400
    },
    {
      "advisor_id": "claude-3-opus",
      "status": "completed",
      "confidence": 0.91,
      "latency_ms": 4200
    },
    {
      "advisor_id": "llama-3-70b",
      "status": "completed",
      "confidence": 0.75,
      "latency_ms": 5800
    }
  ],
  "verdict": { ... },
  "created_at": "2026-07-17T10:00:00Z",
  "completed_at": "2026-07-17T10:00:25Z"
}
```

### 2.3 Get Full Deliberation Report

```
GET /api/v1/deliberate/{session_id}/report
```

Returns the complete detailed report including all perspectives, arguments, disagreements, evaluations, scores, and the final verdict.

**Response:**

```json
{
  "session_id": "sess_a1b2c3d4",
  "verdict": {
    "decision": "Proceed with a phased pivot — maintain B2C while building B2B MVP for 3 educational institutions",
    "confidence": 0.78,
    "summary": "A majority of advisors recommend a phased approach...",
    "reasoning": {
      "key_factors": [
        "Current B2C MRR provides runway for 6 months",
        "B2B market in SEA edtech growing at 34% YoY",
        "Churn rate of 12% signals product-market fit issues in B2C"
      ],
      "supporting_arguments": [
        {
          "advisor_id": "claude-3-opus",
          "argument": "B2B contracts provide predictable revenue and higher LTV",
          "score": 0.91
        },
        {
          "advisor_id": "gpt-4",
          "argument": "Dual-track approach reduces downside risk",
          "score": 0.82
        }
      ],
      "opposing_arguments": [
        {
          "advisor_id": "llama-3-70b",
          "argument": "Pivot may dilute focus and burn out the team",
          "score": 0.75
        }
      ],
      "disagreements": [
        {
          "type": "explicit_conflict",
          "between": ["claude-3-opus", "llama-3-70b"],
          "issue": "Speed of pivot",
          "resolution": "Compromise: phased approach over 6 months"
        }
      ]
    },
    "uncertainty_factors": [
      "Market data is 3 months old",
      "Competitor analysis not included in context"
    ],
    "recommendations": [
      "Validate B2B demand with 5 customer interviews before committing resources",
      "Set a 3-month checkpoint to evaluate B2B traction",
      "Maintain B2C operations at current level during transition"
    ]
  },
  "scores": {
    "claude-3-opus": 0.91,
    "gpt-4": 0.82,
    "llama-3-70b": 0.75
  },
  "created_at": "2026-07-17T10:00:00Z"
}
```

### 2.4 List Sessions

```
GET /api/v1/sessions?status=completed&limit=20&offset=0
```

**Response:**

```json
{
  "items": [
    {
      "session_id": "sess_a1b2c3d4",
      "question": "Should our startup pivot...",
      "status": "completed",
      "advisor_count": 3,
      "confidence": 0.78,
      "created_at": "2026-07-17T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### 2.5 List Advisors

```
GET /api/v1/advisors
```

**Response:**

```json
{
  "advisors": [
    {
      "id": "advisor_gpt4",
      "name": "GPT-4 Strategist",
      "provider": "openai",
      "model": "gpt-4-turbo",
      "capabilities": ["reasoning", "business_analysis", "coding"],
      "specialization": "business_strategy",
      "active": true
    },
    {
      "id": "advisor_claude3",
      "name": "Claude 3 Analyst",
      "provider": "anthropic",
      "model": "claude-3-opus-20240229",
      "capabilities": ["reasoning", "research", "ethics"],
      "specialization": "risk_analysis",
      "active": true
    }
  ]
}
```

---

## 3. WebSocket API

### 3.1 Stream Deliberation Progress

```
WS /api/v1/ws/deliberate/{session_id}
```

Provides real-time streaming of deliberation progress.

**Messages (Server → Client):**

```json
// Step update
{
  "type": "step_update",
  "session_id": "sess_a1b2c3d4",
  "current_step": "generate_perspectives",
  "progress": 0.16
}

// Advisor response received
{
  "type": "advisor_response",
  "session_id": "sess_a1b2c3d4",
  "advisor_id": "claude-3-opus",
  "perspective": {
    "stance": "cautious_pivot",
    "summary": "A phased pivot is recommended...",
    "confidence": 0.91
  }
}

// Disagreement detected
{
  "type": "disagreement",
  "session_id": "sess_a1b2c3d4",
  "between": ["claude-3-opus", "llama-3-70b"],
  "issue": "Timeline for pivot"
}

// Verdict ready
{
  "type": "verdict",
  "session_id": "sess_a1b2c3d4",
  "verdict": { ... },
  "report_url": "/api/v1/deliberate/sess_a1b2c3d4/report"
}

// Error
{
  "type": "error",
  "session_id": "sess_a1b2c3d4",
  "code": "ADVISOR_TIMEOUT",
  "message": "llama-3-70b did not respond within 30s",
  "advisor_id": "llama-3-70b"
}
```

---

## 4. Error Responses

All errors follow a consistent schema:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [
      {
        "field": "question",
        "message": "Field required"
      }
    ],
    "trace_id": "trace_abc123"
  }
}
```

### Error Codes

| HTTP Status | Code                  | Description                        |
|-------------|-----------------------|------------------------------------|
| 400         | VALIDATION_ERROR      | Invalid request body or parameters |
| 401         | UNAUTHORIZED          | Missing or invalid API key         |
| 404         | NOT_FOUND             | Session or advisor not found       |
| 408         | ADVISOR_TIMEOUT       | An advisor did not respond in time |
| 429         | RATE_LIMITED          | Too many requests                  |
| 500         | INTERNAL_ERROR        | Unexpected server error            |
| 502         | PROVIDER_ERROR        | AI provider returned an error      |
| 503         | SERVICE_UNAVAILABLE   | System is overloaded or in maintenance |

---

## 5. Rate Limiting

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700123456
```

| Tier     | Rate Limit         | Burst   |
|----------|---------------------|---------|
| Free     | 10 req/min         | 20      |
| Pro      | 100 req/min        | 200     |
| Enterprise | Custom           | Custom  |

---

## 6. Pydantic Schemas (API Layer)

```python
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class DeliberateRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    context: dict = Field(default_factory=dict)
    config: DeliberationConfig | None = None


class DeliberationConfig(BaseModel):
    advisors: list[str] | None = None  # None = use all active
    debate_rounds: int = Field(default=2, ge=0, le=5)
    judge: str | None = None
    return_full_report: bool = True
    timeout_seconds: int = Field(default=60, ge=10, le=300)


class VerdictResponse(BaseModel):
    session_id: UUID
    decision: str
    confidence: float = Field(..., ge=0, le=1)
    summary: str
    reasoning: ReasoningDetail
    uncertainty_factors: list[str]
    recommendations: list[str]
    scores: dict[str, float]


class ReasoningDetail(BaseModel):
    key_factors: list[str]
    supporting_arguments: list[ScoredArgument]
    opposing_arguments: list[ScoredArgument]
    disagreements: list[DisagreementSummary]


class ScoredArgument(BaseModel):
    advisor_id: str
    argument: str
    score: float = Field(..., ge=0, le=1)
```
