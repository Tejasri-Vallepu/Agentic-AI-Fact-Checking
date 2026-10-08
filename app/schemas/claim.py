from typing import Optional

from pydantic import BaseModel, Field


class Claim(BaseModel):
    claim_id: str = Field(description="Unique identifier of the claim")
    claim_text: str = Field(min_length=1, description="The factual claim to verify")
    label: Optional[str] = Field(
        default=None,
        description="Original dataset veracity label",
    )
    language: str = Field(default="en", description="Claim language")
    premise_articles: list[str] = Field(
        default_factory=list,
        description="Articles associated with the claim",
    )
    review_article: Optional[str] = Field(
        default=None,
        description="Review article associated with the claim",
    )
