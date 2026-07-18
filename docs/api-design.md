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

Initiates a multi-advisor deliberation process. The pipeline runs asynchronously — the endpoint returns immediately with a `session_id` for polling.

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
    "advisors": ["rational_analyst", "economic", "devils_advocate"],
    "debate_rounds": 2,
    "return_full_report": true,
    "timeout_seconds": 60
  }
}
```

The `config.advisors` field accepts persona IDs (`rational_analyst`, `humanitarian`, `economic`, `legal`, `devils_advocate`, `long_term_strategist`). If omitted, all 6 active personas are used.

**Response (202 Accepted):**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "pending",
  "status_url": "/api/v1/deliberate/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "estimated_completion_seconds": 30
}
```

### 2.2 Get Deliberation Status

```
GET /api/v1/deliberate/{session_id}
```

**Response (in progress):**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question": "Should our startup pivot from B2C to B2B?",
  "status": "generating_perspectives",
  "progress": {
    "current_step": "generate_perspectives",
    "steps_completed": 1,
    "steps_total": 9,
    "steps": [
      {"name": "analyze_context", "status": "completed"},
      {"name": "generate_perspectives", "status": "in_progress"},
      {"name": "collect_arguments", "status": "pending"},
      {"name": "resolve_conflicts", "status": "pending"},
      {"name": "evaluate_principles", "status": "pending"},
      {"name": "explore_scenarios", "status": "pending"},
      {"name": "reflect", "status": "pending"},
      {"name": "score_wisdom", "status": "pending"},
      {"name": "generate_verdict", "status": "pending"}
    ]
  },
  "advisor_statuses": [
    {
      "persona": "rational_analyst",
      "stance": "cautious_yes",
      "confidence": 0.72
    }
  ]
}
```

**Response (completed):**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question": "Should our startup pivot from B2C to B2B?",
  "status": "completed",
  "progress": {
    "current_step": null,
    "steps_completed": 9,
    "steps_total": 9,
    "steps": [
      {"name": "analyze_context", "status": "completed"},
      {"name": "generate_perspectives", "status": "completed"},
      {"name": "collect_arguments", "status": "completed"},
      {"name": "resolve_conflicts", "status": "completed"},
      {"name": "evaluate_principles", "status": "completed"},
      {"name": "explore_scenarios", "status": "completed"},
      {"name": "reflect", "status": "completed"},
      {"name": "score_wisdom", "status": "completed"},
      {"name": "generate_verdict", "status": "completed"}
    ]
  },
  "advisor_statuses": [
    {"persona": "rational_analyst", "stance": "cautious_yes", "confidence": 0.82},
    {"persona": "humanitarian", "stance": "cautious_no", "confidence": 0.65},
    {"persona": "economic", "stance": "yes", "confidence": 0.91},
    {"persona": "legal", "stance": "cautious_yes", "confidence": 0.55},
    {"persona": "devils_advocate", "stance": "no", "confidence": 0.78},
    {"persona": "long_term_strategist", "stance": "cautious_yes", "confidence": 0.70}
  ],
  "verdict": {
    "decision": "Proceed with caution — monitor key risk factors",
    "confidence": 0.78,
    "summary": "After consulting 6 advisor personas, identifying 4 key conflicts, and evaluating 5 ethical principles (3/5 score >= 7/10), the council recommends: Proceed with caution — monitor key risk factors",
    "wisdom_score": 72.4
  },
  "report_url": "/api/v1/deliberate/a1b2c3d4-e5f6-7890-abcd-ef1234567890/report"
}
```

### 2.3 Get Full Deliberation Report

```
GET /api/v1/deliberate/{session_id}/report
```

Returns the complete detailed report including all perspectives, arguments, conflicts, evaluations, scenarios, reflection, and the final verdict.

**Response:**

```json
{
  "case": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "question": "Should our startup pivot from B2C to B2B?",
    "domain": "business"
  },
  "verdict": {
    "decision": "Proceed with caution — monitor key risk factors",
    "confidence": 0.78,
    "wisdom_score": {
      "evidence_quality": 72.0,
      "perspective_diversity": 85.0,
      "ethical_alignment": 68.0,
      "long_term_impact": 70.0,
      "uncertainty_handling": 65.0,
      "reversibility": 80.0
    },
    "overall_score": 72.4
  },
  "council_composition": [
    {
      "persona": "rational_analyst",
      "stance": "cautious_yes",
      "confidence": 0.82,
      "summary": "From a rational_analyst perspective, the assessment is **cautious_yes**..."
    }
  ],
  "conflicts": [
    {
      "type": "explicit_conflict",
      "between": ["economic", "devils_advocate"],
      "description": "economic (yes) conflicts with devils_advocate (no)",
      "root_cause": "Opposing stances on the core question"
    },
    {
      "type": "consensus",
      "between": ["rational_analyst", "humanitarian", "legal", "long_term_strategist"],
      "description": "All advisors agree: cautious_yes",
      "root_cause": "Unified assessment across all perspectives"
    }
  ],
  "principle_evaluations": [
    {
      "principle": "fairness",
      "score": 7.5,
      "weight": 0.20,
      "rationale": "Evaluated against stakeholder impact",
      "concerns": ["Potential unequal access to transition support"]
    }
  ],
  "scenario_explorations": [
    {
      "name": "aggressive_pivot_optimistic_6_months",
      "horizon": "6 months",
      "probability": 0.55,
      "assumptions": [{"description": "Market demand materializes", "confidence": 0.6}],
      "uncertainty_level": "medium",
      "net_impact": 3.0
    }
  ],
  "reflection": {
    "reflection_notes": [
      "Healthy disagreement detected: economic vs devils_advocate...",
      "Data gaps identified: 3. Decision confidence should reflect this uncertainty."
    ],
    "missing_perspectives": [],
    "consistency_issues": [],
    "confidence_adjustment": -0.15
  },
  "reasoning": {
    "key_factors": [
      "Market analysis shows 34% YoY growth in B2B segment",
      "Current churn rate of 12% indicates B2C product-market fit issues"
    ],
    "supporting": [
      {"persona": "economic", "argument": "Analysis from economic perspective", "confidence": 0.91, "score": 91.0}
    ],
    "opposing": [
      {"persona": "devils_advocate", "argument": "Analysis from devils_advocate perspective", "confidence": 0.78, "score": 78.0}
    ],
    "conflict_resolution": "Conflict between economic and devils_advocate: Different value priorities and evaluation frameworks. Resolved by seeking balanced approach."
  },
  "uncertainties": [
    "Cost and budget details are missing",
    "Revenue projections are not validated"
  ],
  "alternatives": [
    "Phased approach — implement gradually with checkpoints",
    "Parallel track — run pilot before full commitment",
    "Status quo — maintain current course with adjustments"
  ],
  "recommendations": [
    "Validate key assumptions with empirical data before committing",
    "Address fairness concerns: review alignment"
  ],
  "model_selections": [
    {
      "persona": "rational_analyst",
      "selected_adapter": "ollama",
      "selected_model": "llama3.1",
      "selection_reason": "Declared=6.5/10 (no verified data yet) — best across 2 adapter/model(s)",
      "fallback_occurred": false,
      "fallback_from": null
    }
  ]
}
```

### 2.4 List Sessions

```
GET /api/v1/sessions?status=completed&limit=20&offset=0
```

**Response:**

```json
{
  "items": [],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

*Note: Session listing returns data from the in-memory store. PostgreSQL persistence is optional — sessions survive only while the server is running without a database.*

### 2.5 Session Stats

```
GET /api/v1/sessions/stats
```

**Response:**

```json
{
  "total_cases": 5,
  "cases_with_outcomes": 2,
  "avg_confidence": 0.78,
  "avg_outcome_score": 3.5,
  "domains": ["business", "technology"]
}
```

### 2.6 List Advisors

```
GET /api/v1/advisors
```

**Response:**

```json
{
  "advisors": [
    {
      "persona": "rational_analyst",
      "name": "Rational Analyst",
      "description": "Focuses on data, probabilities, and empirical evidence",
      "active": true,
      "capability_requirements": {
        "reasoning": 9,
        "structured_output": true,
        "nuanced_language": false,
        "ethical_reasoning": 0,
        "numerical_reasoning": 8,
        "long_context": false,
        "high_reliability": true
      }
    }
  ]
}
```

### 2.7 Get Advisor Detail

```
GET /api/v1/advisors/{persona}
```

**Response:**

```json
{
  "persona": "rational_analyst",
  "name": "Rational Analyst",
  "description": "Focuses on data, probabilities, and empirical evidence",
  "system_prompt": "You are a Rational Analyst...",
  "priority_weights": {"evidence": 0.4, "logic": 0.4, "data": 0.2},
  "capability_requirements": {
    "reasoning": 9,
    "structured_output": true,
    "numerical_reasoning": 8
  },
  "active": true
}
```

---

## 3. WebSocket API

### 3.1 Stream Deliberation Progress

```
WS /api/v1/ws/deliberate/{session_id}
```

Provides real-time updates on deliberation progress. The server sends JSON messages as the pipeline progresses.

**Messages (Server → Client):**

```json
// Status update (sent every 0.5s during deliberation)
{
  "type": "status_update",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "generating_perspectives",
  "current_step": "generate_perspectives",
  "steps_completed": 1,
  "steps_total": 9
}

// Verdict ready
{
  "type": "verdict",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "verdict": {
    "decision": "Proceed with caution — monitor key risk factors",
    "confidence": 0.78,
    "wisdom_score": 72.4
  }
}

// Error
{
  "type": "error",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "detail": "No inference adapters available"
}
```

**Client → Server messages:**

The client can request a status refresh by sending any text message (e.g., `"ping"`).

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
| 404         | NOT_FOUND             | Session or advisor not found       |
| 500         | INTERNAL_ERROR        | Unexpected server error            |

---

## 5. Pydantic Schemas (API Layer)

```python
from pydantic import BaseModel, Field
from uuid import UUID


class DeliberateRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=5000)
    context: dict = Field(default_factory=dict)
    config: DeliberationConfig | None = None


class DeliberationConfig(BaseModel):
    advisors: list[str] | None = None  # persona IDs, None = use all active
    debate_rounds: int = Field(default=2, ge=0, le=5)
    judge: str | None = None
    return_full_report: bool = True
    timeout_seconds: int = Field(default=60, ge=10, le=300)


class AdvisorListItem(BaseModel):
    persona: str
    name: str
    description: str
    active: bool
    capability_requirements: dict
```
