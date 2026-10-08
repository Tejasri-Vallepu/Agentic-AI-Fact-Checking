from pathlib import Path

import chromadb


class ChromaVectorStore:
    def __init__(
        self,
        persist_directory: Path,
        collection_name: str = "fact_check_evidence",
    ):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    @property
    def count(self) -> int:
        return self.collection.count()

    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to ChromaDB
        in smaller batches to stay within Chroma's
        maximum batch size.
        """

        ids = [
            item["document_id"]
            for item in documents
        ]

        texts = [
            item["text"]
            for item in documents
        ]

        metadatas = [
            {
                key: str(value)
                for key, value in item.get(
                    "metadata", {}
                ).items()
            }
            for item in documents
        ]

        embedding_list = embeddings.tolist()

        # ChromaDB allows only a limited number of
        # records in one upsert operation.
        batch_size = 5000

        for start in range(
            0,
            len(documents),
            batch_size
        ):
            end = min(
                start + batch_size,
                len(documents)
            )

            print(
                f"Adding documents "
                f"{start + 1}-{end} "
                f"of {len(documents)}..."
            )

            self.collection.upsert(
                ids=ids[start:end],
                documents=texts[start:end],
                embeddings=embedding_list[start:end],
                metadatas=metadatas[start:end],
            )

    def search(
        self,
        query_embedding,
        top_k: int = 5
    ):
        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return results