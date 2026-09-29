"""Evaluation helpers for measuring retrieval and answer quality in the legislation RAG pipeline.

This module is a placeholder for metrics such as retrieval recall, ranking quality,
and grounding checks on legal question-answer pairs.
"""

# Add evaluation functions here as the retrieval pipeline matures.
# Typical checks include recall@k, MRR, and answer-grounded scoring.


def chunk_id(metadata: dict) -> tuple:
    """Build a stable identifier for a chunk from its metadata.

    Args:
        metadata (dict): A chunk metadata dictionary containing page, article,
            and clause fields.

    Returns:
        tuple: A tuple of (page, article, clause) used to compare chunks across
        retrieval results and ground-truth labels.
    """
    return (
        metadata["page"],
        metadata["article"],
        metadata["clause"],
    )

def precision_at_k(results, relevant_ids: set[str], k: int) -> float:
    """Measure how many of the top-k retrieved chunks are actually relevant.
    
        Args:
            results: A list-like collection of retrieved chunk objects, each with a
                metadata attribute.
            relevant_ids (set): The set of ground-truth relevant chunk IDs.
            k (int): The number of top results to evaluate.
    
        Returns:
            float: The fraction of retrieved results within the top-k that are relevant.
    """
    retrieved_ids = [
        result.metadata["chunk_id"]
        for result in results[:k]
    ]

    relevant_count = sum(
        chunk_id in relevant_ids
        for chunk_id in retrieved_ids
    )

    # print("DEBUG retrieved_ids:", retrieved_ids)
    # print("DEBUG relevant_ids:", relevant_ids)
    # print("DEBUG relevant_count:", relevant_count)

    return relevant_count / k


def recall_at_k(results, relevant_ids: set[str], k: int) -> float:
    """Measure how many relevant chunks were successfully recovered in the top-k.
    
        Args:
            results: A list-like collection of retrieved chunk objects, each with a
                metadata attribute.
            relevant_ids (set): The set of ground-truth relevant chunk IDs.
            k (int): The number of top results to consider for retrieval recall.
    
        Returns:
            float: The proportion of all relevant chunks that appear in the top-k.
        """
    retrieved_ids = [
        result.metadata["chunk_id"]
        for result in results[:k]
    ]

    if not relevant_ids:
        return 0.0

    relevant_count = sum(
        chunk_id in relevant_ids
        for chunk_id in retrieved_ids
    )

    # print("DEBUG retrieved_ids:", retrieved_ids)
    # print("DEBUG relevant_ids:", relevant_ids)
    # print("DEBUG relevant_count:", relevant_count)

    return relevant_count / len(relevant_ids)