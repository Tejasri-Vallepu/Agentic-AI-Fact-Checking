def recall_at_k(
    relevant_document_ids: list[str],
    retrieved_document_ids: list[str],
) -> float:
    relevant = set(relevant_document_ids)

    if not relevant:
        return 0.0

    retrieved = set(retrieved_document_ids)

    return len(relevant.intersection(retrieved)) / len(relevant)
