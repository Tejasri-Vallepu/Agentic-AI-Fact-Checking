from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.application import create_application


router = APIRouter(prefix="/api", tags=["Fact Checking"])

_system = None


def get_system():
    global _system

    if _system is None:
        _system = create_application()

    return _system


class FactCheckRequest(BaseModel):
    claim: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class FactCheckResponse(BaseModel):
    claim: str
    verdict: str
    confidence: float
    explanation: str
    key_facts: list[str]
    evidence_ids: list[str]
    reasoning_summary: str


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check(request: FactCheckRequest):
    output = get_system().run(
        claim_text=request.claim,
        top_k=request.top_k,
    )

    result = output["result"]

    return FactCheckResponse(
        claim=request.claim,
        verdict=result.verdict,
        confidence=result.confidence,
        explanation=result.explanation,
        key_facts=result.key_facts,
        evidence_ids=result.evidence_ids,
        reasoning_summary=result.reasoning_summary,
    )
