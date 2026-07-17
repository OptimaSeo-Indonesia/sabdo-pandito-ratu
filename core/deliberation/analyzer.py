# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import re

from core.models import ContextAnalysis


DOMAIN_KEYWORDS: dict[str, set[str]] = {
    "technology": {
        "software", "app", "website", "platform", "tech", "digital",
        "startup", "saas", "algorithm", "data", "ai", "machine learning",
        "cloud", "server", "database", "api", "engineering", "product",
    },
    "business": {
        "revenue", "profit", "market", "customer", "investment",
        "acquisition", "merger", "pivot", "b2b", "b2c", "business",
        "strategy", "growth", "revenue", "cost", "budget", "hiring",
        "layoff", "funding", "valuation", "ipo", "stakeholder",
    },
    "healthcare": {
        "health", "medical", "patient", "hospital", "clinical",
        "treatment", "drug", "therapy", "diagnosis", "vaccine",
        "disease", "doctor", "nurse", "wellness",
    },
    "education": {
        "school", "student", "teacher", "curriculum", "education",
        "learning", "training", "university", "college", "course",
        "pedagogy", "classroom", "academic",
    },
    "policy": {
        "government", "regulation", "policy", "law", "public",
        "compliance", "mandate", "legislation", "tax", "subsidy",
        "environmental", "climate", "carbon", "emission",
    },
    "personal": {
        "career", "family", "personal", "life", "decision",
        "move", "relocate", "relationship", "marry", "invest",
        "buy", "purchase", "house", "car",
    },
}


DOMAIN_STAKEHOLDERS: dict[str, list[str]] = {
    "technology": ["engineering team", "product managers", "users", "investors"],
    "business": ["executives", "employees", "shareholders", "customers", "partners"],
    "healthcare": ["patients", "healthcare providers", "regulators", "insurers"],
    "education": ["students", "educators", "parents", "administrators"],
    "policy": ["citizens", "government agencies", "businesses", "nonprofits"],
    "personal": ["yourself", "family", "close relations"],
}


DOMAIN_CONSTRAINTS: dict[str, list[str]] = {
    "technology": ["technical feasibility", "development timeline", "infrastructure"],
    "business": ["budget constraints", "market conditions", "competitive landscape"],
    "healthcare": ["ethical guidelines", "patient safety", "regulatory compliance"],
    "education": ["accreditation requirements", "resource availability"],
    "policy": ["legal framework", "public opinion", "budget allocation"],
    "personal": ["personal values", "financial situation", "timing"],
}


HIGH_STAKE_KEYWORDS = {
    "critical", "urgent", "life", "death", "irreversible", "massive",
    "catastrophic", "existential", "bankruptcy", "terminal",
}


HIGH_SENSITIVITY_KEYWORDS = {
    "immediately", "urgent", "asap", "deadline", "emergency",
    "time-sensitive", "critical", "today", "tomorrow", "this week",
}


class ContextAnalyzer:
    def analyze(self, question: str, context: dict | None = None) -> ContextAnalysis:
        ctx = context or {}
        question_lower = question.lower()

        domain = self._detect_domain(question_lower)
        stakes = self._detect_stakes(question_lower, ctx)
        stakeholders = self._detect_stakeholders(question_lower, domain, ctx)
        time_sensitivity = self._detect_time_sensitivity(question_lower, ctx)
        key_constraints = self._detect_constraints(domain, ctx)
        data_gaps = self._detect_data_gaps(question, domain, ctx)

        return ContextAnalysis(
            domain=domain,
            stakes=stakes,
            affected_stakeholders=stakeholders,
            time_sensitivity=time_sensitivity,
            key_constraints=key_constraints,
            data_gaps=data_gaps,
        )

    def _detect_domain(self, question_lower: str) -> str:
        scores: dict[str, int] = {}
        for domain, keywords in DOMAIN_KEYWORDS.items():
            scores[domain] = sum(1 for kw in keywords if kw in question_lower)
        if not scores or max(scores.values()) == 0:
            return "general"
        return max(scores, key=scores.get)

    def _detect_stakes(self, question_lower: str, context: dict) -> str:
        if context.get("stakes"):
            return context["stakes"]
        matches = sum(1 for kw in HIGH_STAKE_KEYWORDS if kw in question_lower)
        if matches >= 2:
            return "high"
        if matches == 1:
            return "medium"
        return "low"

    def _detect_stakeholders(
        self, question_lower: str, domain: str, context: dict
    ) -> list[str]:
        if context.get("stakeholders"):
            return context["stakeholders"]
        extracted: list[str] = []
        stakeholder_patterns = [
            r"(?:for|affect|impact|involve)\s+([\w\s]+?)(?:,|and|\.|$)",
        ]
        for pattern in stakeholder_patterns:
            for match in re.finditer(pattern, question_lower):
                extracted.append(match.group(1).strip())
        domain_defaults = DOMAIN_STAKEHOLDERS.get(domain, ["primary stakeholders"])
        combined = extracted + domain_defaults
        seen: set[str] = set()
        return [s for s in combined if not (s in seen or seen.add(s))][:5]

    def _detect_time_sensitivity(self, question_lower: str, context: dict) -> str:
        if context.get("time_sensitivity"):
            return context["time_sensitivity"]
        matches = sum(1 for kw in HIGH_SENSITIVITY_KEYWORDS if kw in question_lower)
        if matches >= 2:
            return "urgent"
        if matches == 1:
            return "time-sensitive"
        return "moderate"

    def _detect_constraints(self, domain: str, context: dict) -> list[str]:
        if context.get("constraints"):
            return context["constraints"]
        return DOMAIN_CONSTRAINTS.get(domain, [])

    def _detect_data_gaps(self, question: str, domain: str, context: dict) -> list[str]:
        if context.get("data_gaps"):
            return context["data_gaps"]
        gaps: list[str] = []
        gap_indicators = {
            "cost": "Specific cost figures not provided",
            "budget": "Budget details not specified",
            "revenue": "Revenue projections not available",
            "deadline": "Time constraints not clearly defined",
            "risk": "Risk assessment data not provided",
            "market": "Market analysis data not provided",
            "user": "User impact data not available",
            "employee": "Employee impact data not specified",
            "regulation": "Regulatory requirements not identified",
            "compliance": "Compliance framework not specified",
        }
        question_lower = question.lower()
        for keyword, gap_text in gap_indicators.items():
            if keyword not in question_lower:
                gaps.append(gap_text)
        return gaps[:5]
