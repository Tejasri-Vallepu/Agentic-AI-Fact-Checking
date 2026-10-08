from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def encode_documents(self, texts):
        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

    def encode_query(self, text):
        return self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
