import json
from pathlib import Path
from typing import Any

from app.preprocessing.text import normalize_claim
from app.schemas.claim import Claim


class DatasetLoader:
    """
    Loads the original CheckThat-style JSON dataset from data/raw
    without modifying the original dataset files.
    """

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data" / "raw"

    def _load_json(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _extract_records(self, data: Any) -> list[dict]:
        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            for key in ("data", "records", "claims", "items"):
                if key in data and isinstance(data[key], list):
                    return data[key]

        raise ValueError("Unsupported dataset JSON structure.")

    def _convert_record(self, record: dict, index: int) -> Claim:
        metadata = record.get("metadata", {}) or {}
        label_data = record.get("label", {}) or {}

        claim_text = (
            metadata.get("claim")
            or record.get("claim")
            or record.get("text")
            or ""
        )

        claim_id = (
            metadata.get("claim_id")
            or record.get("id")
            or str(index)
        )

        premise_articles = metadata.get("premise_articles", []) or []
        review_article = label_data.get("review_article")
        original_rating = label_data.get("original_rating")

        return Claim(
            claim_id=str(claim_id),
            claim_text=normalize_claim(str(claim_text)),
            label=None if original_rating is None else str(original_rating),
            language="en",
            premise_articles=[str(x) for x in premise_articles],
            review_article=(
                None
                if review_article is None
                else str(review_article)
            ),
        )

    def load_split(self, split: str) -> list[Claim]:
        mapping = {
            "train": "train.json",
            "valid": "valid.json",
            "val": "valid.json",
            "test": "test.json",
        }

        if split not in mapping:
            raise ValueError(
                f"Unknown split: {split}. "
                f"Expected one of: {list(mapping.keys())}"
            )

        path = self.data_dir / mapping[split]

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {path}"
            )

        records = self._extract_records(
            self._load_json(path)
        )

        return [
            self._convert_record(record, index)
            for index, record in enumerate(records)
        ]

    def load_all(self) -> dict[str, list[Claim]]:
        return {
            "train": self.load_split("train"),
            "valid": self.load_split("valid"),
            "test": self.load_split("test"),
        }