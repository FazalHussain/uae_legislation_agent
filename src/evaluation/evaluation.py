"""Evaluation helpers for measuring retrieval and answer quality in the legislation RAG pipeline.

This module is a placeholder for metrics such as retrieval recall, ranking quality,
and grounding checks on legal question-answer pairs.
"""

# Add evaluation functions here as the retrieval pipeline matures.
# Typical checks include recall@k, MRR, and answer-grounded scoring.


def chunk_id(metadata: dict) -> tuple:
    """Build a comparable identifier from a chunk's source metadata.

    Args:
        metadata: Chunk metadata containing ``page``, ``article``, and
            ``clause`` keys.

    Returns:
        A tuple of page, article, and clause values.
    """
    return (
        metadata["page"],
        metadata["article"],
        metadata["clause"],
    )

def precision_at_k(results, relevant_ids: set[str], k: int) -> float:
    """Calculate the fraction of the top ``k`` results labeled relevant.

    Args:
        results: Ordered retrieved chunks, each with a ``metadata`` mapping
            containing a ``chunk_id`` value.
        relevant_ids: Ground-truth identifiers for relevant chunks.
        k: Number of leading results included in the precision calculation.

    Returns:
        The number of relevant IDs among ``results[:k]`` divided by ``k``.
        The value is in the range 0.0 to 1.0 when ``k`` is positive.
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
    """Calculate the fraction of all relevant IDs found in the top ``k`` results.

    Args:
        results: Ordered retrieved chunks, each with a ``metadata`` mapping
            containing a ``chunk_id`` value.
        relevant_ids: Ground-truth identifiers for relevant chunks.
        k: Number of leading results checked for relevant IDs.

    Returns:
        The number of relevant IDs among ``results[:k]`` divided by the number
        of ground-truth IDs, or ``0.0`` when ``relevant_ids`` is empty.
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

def reciprocal_rank(
    results,
    relevant_ids: set[str],
    k: int,
) -> float:

    for rank, result in enumerate(results[:k], start=1):

        chunk_id = result.metadata["chunk_id"]

        if chunk_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    all_results,
    all_relevant_ids,
    k: int,
) -> float:

    if not all_results:
        return 0.0

    scores = [
        reciprocal_rank(
            results,
            relevant_ids,
            k,
        )
        for results, relevant_ids
        in zip(all_results, all_relevant_ids)
    ]

    return sum(scores) / len(scores)