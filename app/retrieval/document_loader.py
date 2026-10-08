import json
from pathlib import Path
from typing import Any


class ArticleLoader:
    def __init__(self, articles_directory: Path):
        self.articles_directory = Path(articles_directory)

    def _collect_text(self, value: Any) -> list[str]:
        if isinstance(value, str):
            cleaned = value.strip()
            return [cleaned] if cleaned else []

        if isinstance(value, list):
            result = []
            for item in value:
                result.extend(self._collect_text(item))
            return result

        if isinstance(value, dict):
            result = []
            for key, item in value.items():
                # Avoid indexing common metadata-only fields as evidence text.
                if key.lower() in {
                    "id",
                    "url",
                    "source",
                    "timestamp",
                    "date",
                }:
                    continue
                result.extend(self._collect_text(item))
            return result

        return []

    def load_article(self, article_id: str) -> dict:
        path = self.articles_directory / article_id

        if not path.exists():
            raise FileNotFoundError(f"Article not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        parts = self._collect_text(data)
        text = "\n".join(parts).strip()

        return {
            "document_id": str(article_id),
            "text": text,
            "metadata": {
                "source_file": str(path),
            },
        }

    def load_all_articles(self) -> list[dict]:
        documents = []

        for path in self.articles_directory.rglob("*.json"):
            relative_id = path.relative_to(self.articles_directory).as_posix()

            try:
                documents.append(self.load_article(relative_id))
            except Exception:
                continue

        return documents
