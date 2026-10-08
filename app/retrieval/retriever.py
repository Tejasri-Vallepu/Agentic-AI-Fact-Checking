from app.core.config import settings


class EvidenceRetriever:
    def __init__(self, embedding_model, vector_store):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def search(self, claim_text: str, top_k: int | None = None):
        if self.vector_store.count == 0:
            raise RuntimeError(
                "Vector database is empty. Run scripts\\build_vector_db.py first."
            )

        k = top_k or settings.RETRIEVAL_TOP_K

        query_embedding = self.embedding_model.encode_query(claim_text)
        results = self.vector_store.search(query_embedding, top_k=k)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        evidence = []

        for document_id, text, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            score = 1.0 / (1.0 + float(distance))

            evidence.append(
                {
                    "document_id": str(document_id),
                    "text": text,
                    "score": score,
                    "metadata": metadata or {},
                }
            )

        return evidence
