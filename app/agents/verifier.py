from google.genai import types

from app.core.config import settings
from app.llm.gemini_client import GeminiClient
from app.schemas.fact_check import FactCheckResult


class GeminiVerifier:
    def __init__(self):
        self.client = GeminiClient()

    def verify(self, claim_text: str, evidence: list[dict]) -> FactCheckResult:
        evidence_text = "\n\n".join(
            [
                (
                    f"Evidence ID: {item['document_id']}\n"
                    f"Score: {item['score']:.4f}\n"
                    f"Text: {item['text']}"
                )
                for item in evidence
            ]
        )

        prompt = f"""
You are a professional fact-checking verifier.

Verify the claim using ONLY the supplied evidence.
Do not use outside knowledge.
Do not invent facts.
If the evidence is not enough, return INSUFFICIENT_EVIDENCE.

Claim:
{claim_text}

Evidence:
{evidence_text}

Return a structured result with:
- verdict
- confidence from 0 to 1
- explanation
- key_facts
- evidence_ids
- reasoning_summary

The verdict must be exactly one of:
SUPPORTED
REFUTED
PARTIALLY_SUPPORTED
INSUFFICIENT_EVIDENCE
"""

        response = self.client.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2048,
                response_mime_type="application/json",
                response_schema=FactCheckResult,
            ),
        )

        if not response.parsed:
            raise RuntimeError("Gemini did not return a structured result.")

        return response.parsed
