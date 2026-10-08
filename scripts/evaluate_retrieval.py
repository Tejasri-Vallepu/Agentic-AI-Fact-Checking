from app.core.config import settings
from app.data.loader import DatasetLoader
from app.evaluation.retrieval import recall_at_k
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.retriever import EvidenceRetriever
from app.retrieval.vector_store import ChromaVectorStore


def main():
    loader = DatasetLoader(settings.project_root)
    test_claims = loader.load_split("test")[:100]

    embedding_model = EmbeddingModel()

    vector_store = ChromaVectorStore(
        settings.vector_db_path
    )

    retriever = EvidenceRetriever(
        embedding_model,
        vector_store,
    )

    for k in (1, 3, 5):
        scores = []

        for claim in test_claims:
            retrieved = retriever.search(
                claim.claim_text,
                top_k=k,
            )

            retrieved_ids = [
                item["document_id"]
                for item in retrieved
            ]

            scores.append(
                recall_at_k(
                    claim.premise_articles,
                    retrieved_ids,
                )
            )

        average = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        print(
            f"Recall@{k}: {average:.4f}"
        )


if __name__ == "__main__":
    main()
