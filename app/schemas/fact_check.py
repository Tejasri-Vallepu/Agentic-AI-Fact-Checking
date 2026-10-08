from typing import Literal

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    document_id: str
    text: str
    score: float = 0.0


class FactCheckResult(BaseModel):
    verdict: Literal[
        "SUPPORTED",
        "REFUTED",
        "PARTIALLY_SUPPORTED",
        "INSUFFICIENT_EVIDENCE",
    ]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    key_facts: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    reasoning_summary: str
