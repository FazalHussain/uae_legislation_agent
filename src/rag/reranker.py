"""Rerank vector-search candidates with a BGE cross-encoder model."""
from sentence_transformers import CrossEncoder

from .rag import Chunk

class BGEReranker:
    """Score query and passage pairs to order retrieved legal chunks."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
    ):
        """Load the cross-encoder used to score query-passage pairs.

        Args:
            model_name: Hugging Face model identifier or local model path.

        Returns:
            None.
        """
        self.model = CrossEncoder(model_name, device="cpu")

    def rerank(
        self,
        query: str,
        results: list[Chunk],
        top_k: int = 5,
    ) -> list[Chunk]:
        """Return the candidate chunks with the highest cross-encoder scores.

        Args:
            query: Search question used to score each candidate passage.
            results: Candidate chunks to score and rank.
            top_k: Maximum number of ranked chunks to return.

        Returns:
            Up to ``top_k`` chunks ordered from highest to lowest score.
        """

        pairs = [
            (query, result.text)
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(results, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            result
            for result, _ in ranked[:top_k]
        ]