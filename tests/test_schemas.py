from app.schemas.claim import Claim
from app.schemas.fact_check import FactCheckResult


def test_claim_schema():
    claim = Claim(
        claim_id="1",
        claim_text="Example claim",
    )

    assert claim.claim_text == "Example claim"


def test_fact_check_schema():
    result = FactCheckResult(
        verdict="SUPPORTED",
        confidence=0.9,
        explanation="Evidence supports the claim.",
        key_facts=["Fact A"],
        evidence_ids=["1.json"],
        reasoning_summary="The evidence is consistent.",
    )

    assert result.verdict == "SUPPORTED"
    assert 0 <= result.confidence <= 1
