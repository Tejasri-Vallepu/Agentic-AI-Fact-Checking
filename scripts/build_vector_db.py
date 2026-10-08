from app.core.config import settings
from app.data.loader import DatasetLoader
from app.retrieval.document_loader import ArticleLoader
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.vector_store import ChromaVectorStore
from app.utils.logger import configure_logging


def main():
    logger = configure_logging()

    project_root = settings.project_root

    # ---------------------------------------------------------
    # 1. Load training claims
    # ---------------------------------------------------------
    dataset_loader = DatasetLoader(project_root)

    train_claims = dataset_loader.load_split("train")

    logger.info(
        f"Training claims loaded: {len(train_claims)}"
    )

    # ---------------------------------------------------------
    # 2. Collect local review article IDs
    # ---------------------------------------------------------
    article_ids = sorted(
        {
            claim.review_article
            for claim in train_claims
            if claim.review_article
        }
    )

    logger.info(
        f"Unique review articles to index: {len(article_ids)}"
    )

    # ---------------------------------------------------------
    # 3. Load local article files
    # ---------------------------------------------------------
    article_loader = ArticleLoader(
        project_root / "data" / "raw" / "articles"
    )

    documents = []

    for article_id in article_ids:
        try:
            document = article_loader.load_article(article_id)

            if document["text"].strip():
                documents.append(document)

        except FileNotFoundError:
            logger.warning(
                f"Skipping missing article: {article_id}"
            )

    logger.info(
        f"Articles successfully loaded: {len(documents)}"
    )

    if not documents:
        raise RuntimeError(
            "No evidence articles were loaded."
        )

    # ---------------------------------------------------------
    # 4. Generate embeddings
    # ---------------------------------------------------------
    embedding_model = EmbeddingModel()

    texts = [
        document["text"]
        for document in documents
    ]

    logger.info(
        f"Generating embeddings for {len(texts)} articles..."
    )

    embeddings = embedding_model.encode_documents(texts)

    # ---------------------------------------------------------
    # 5. Store embeddings in ChromaDB
    # ---------------------------------------------------------
    vector_store = ChromaVectorStore(
        settings.vector_db_path
    )

    vector_store.add_documents(
        documents,
        embeddings,
    )

    logger.info(
        f"Vector database now contains "
        f"{vector_store.count} documents."
    )


if __name__ == "__main__":
    main()