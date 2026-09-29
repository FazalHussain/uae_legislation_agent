"""Embedding helpers for converting legislative text into dense vector representations."""

from sentence_transformers import SentenceTransformer


class BGEEmbeddingModel:
    """Wrap the BGE multilingual embedding model for legal document search."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3"
    ):
        """Load the sentence-transformer model by name."""
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """Encode a list of texts into normalized embeddings for vector similarity search."""

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()