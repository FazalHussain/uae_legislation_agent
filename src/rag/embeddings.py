"""Embedding helpers for converting legislative text into dense vector representations."""

from sentence_transformers import SentenceTransformer


class BGEEmbeddingModel:
    """Encode legal text with the multilingual BGE sentence-transformer model."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3"
    ):
        """Load the configured sentence-transformer embedding model.

        Args:
            model_name: Hugging Face model identifier or local model path.

        Returns:
            None.
        """
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """Encode texts as normalized vectors for similarity search.

        Args:
            texts: Text strings to encode, in the desired output order.

        Returns:
            A list of floating-point embedding vectors aligned with the inputs.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()