# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
import pytest

from core.models import (
    AdvisorPersona,
    AdvisorResponse,
    Claim,
    Evidence,
    VerificationStatus,
)
from core.verification.engine import StructuralEvidenceVerifier


@pytest.fixture
def verifier() -> StructuralEvidenceVerifier:
    return StructuralEvidenceVerifier()


@pytest.fixture
def sample_response() -> AdvisorResponse:
    return AdvisorResponse(
        advisor_id="ra_001",
        persona=AdvisorPersona.RATIONAL_ANALYST,
        stance="yes",
        summary="Solar panels reduce carbon emissions by 40%.",
        reasoning="Data shows renewable energy adoption lowers emissions.",
        confidence=0.85,
        key_points=[
            "Solar costs dropped 90% in a decade.",
            "Payback period is 5 years.",
        ],
        data_sources=[
            "IEA Renewables 2025 report",
            "IRENA cost study 2024",
        ],
        assumptions=["Grid infrastructure can handle the load."],
    )


class TestExtractClaims:
    def test_extracts_summary_as_claim(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        summaries = [c.text for c in claims]
        assert "Solar panels reduce carbon emissions by 40%." in summaries

    def test_extracts_key_points_as_claims(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        texts = [c.text for c in claims]
        assert "Solar costs dropped 90% in a decade." in texts
        assert "Payback period is 5 years." in texts

    def test_all_claims_have_required_fields(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        for c in claims:
            assert c.id
            assert c.text
            assert c.source_advisor_id == "ra_001"
            assert c.source_persona == AdvisorPersona.RATIONAL_ANALYST
            assert 0 <= c.confidence <= 1

    def test_claims_have_extracted_entities(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        for c in claims:
            assert len(c.extracted_entities) > 0

    def test_empty_responses_produce_no_claims(self, verifier):
        claims = verifier.extract_claims([])
        assert claims == []


class TestExtractEvidence:
    def test_extracts_data_sources_as_evidence(self, verifier, sample_response):
        evidence = verifier.extract_evidence([sample_response])
        refs = [e.source_ref for e in evidence]
        assert "IEA Renewables 2025 report" in refs
        assert "IRENA cost study 2024" in refs

    def test_all_evidence_has_required_fields(self, verifier, sample_response):
        evidence = verifier.extract_evidence([sample_response])
        for e in evidence:
            assert e.id
            assert e.text
            assert e.source_type == "data_source"

    def test_no_data_sources_produces_empty_evidence(self, verifier):
        resp = AdvisorResponse(
            advisor_id="test",
            persona=AdvisorPersona.RATIONAL_ANALYST,
            stance="yes",
            summary="Test.",
            reasoning="Test.",
            confidence=0.5,
            key_points=[],
            data_sources=[],
        )
        evidence = verifier.extract_evidence([resp])
        assert evidence == []


class TestVerify:
    def test_verified_when_evidence_matches(self, verifier):
        claims = [
            Claim(
                text="Solar power reduces carbon emissions significantly.",
                source_advisor_id="ra_001",
                source_persona=AdvisorPersona.RATIONAL_ANALYST,
                confidence=0.85,
                extracted_entities=["solar", "power", "reduces", "carbon", "emissions"],
            ),
        ]
        evidence = [
            Evidence(
                text="Solar power adoption reduces carbon emissions by 40% per IEA 2025.",
                source_ref="IEA Renewables 2025 report",
                source_type="data_source",
            ),
        ]
        results = verifier.verify(claims, evidence)
        assert len(results) == 1
        assert results[0].status == VerificationStatus.VERIFIED

    def test_unsupported_when_no_evidence(self, verifier):
        claims = [
            Claim(
                text="Unsupported claim with no evidence.",
                source_advisor_id="test",
                source_persona=AdvisorPersona.RATIONAL_ANALYST,
                confidence=0.2,
                extracted_entities=["unsupported"],
            ),
        ]
        results = verifier.verify(claims, [])
        assert len(results) == 1
        assert results[0].status == VerificationStatus.UNSUPPORTED

    def test_uncertain_when_low_overlap(self, verifier):
        claims = [
            Claim(
                text="Completely unrelated topic about ocean tides.",
                source_advisor_id="test",
                source_persona=AdvisorPersona.RATIONAL_ANALYST,
                confidence=0.7,
                extracted_entities=["completely", "unrelated", "topic", "ocean", "tides"],
            ),
        ]
        evidence = [
            Evidence(
                text="IEA Renewables 2025 report.",
                source_ref="IEA Renewables 2025 report",
                source_type="data_source",
            ),
        ]
        results = verifier.verify(claims, evidence)
        assert results[0].status == VerificationStatus.UNCERTAIN

    def test_all_claims_produce_result(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        evidence = verifier.extract_evidence([sample_response])
        results = verifier.verify(claims, evidence)
        assert len(results) == len(claims)

    def test_result_has_confidence(self, verifier):
        claims = [
            Claim(
                text="Solar costs dropped 90%.",
                source_advisor_id="ra_001",
                source_persona=AdvisorPersona.RATIONAL_ANALYST,
                confidence=0.85,
                extracted_entities=["solar", "costs", "dropped"],
            ),
        ]
        evidence = [
            Evidence(
                text="IRENA cost study 2024 shows 90% drop.",
                source_ref="IRENA 2024",
                source_type="data_source",
            ),
        ]
        results = verifier.verify(claims, evidence)
        assert 0 <= results[0].confidence <= 1


class TestDetectContradictions:
    def test_no_contradictions_by_default(self, verifier):
        assert verifier.detect_contradictions([]) == []


class TestIntegration:
    def test_full_extract_verify_flow(self, verifier, sample_response):
        claims = verifier.extract_claims([sample_response])
        evidence = verifier.extract_evidence([sample_response])
        results = verifier.verify(claims, evidence)

        assert len(claims) == 3
        assert len(evidence) == 2
        assert len(results) == 3

        for r in results:
            assert r.claim_id
            assert r.status in (
                VerificationStatus.VERIFIED,
                VerificationStatus.UNSUPPORTED,
                VerificationStatus.UNCERTAIN,
            )
            assert 0 <= r.support_ratio <= 1
