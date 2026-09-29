"""Concrete retrieval layer that uses embeddings and a Chroma vector store."""

from .embeddings import BGEEmbeddingModel
from .vectore_store import ChromaVectorStore


class VectorRetriever:
    """Use a text embedding model to search the vector store for relevant legislation chunks."""

    def __init__(
        self,
        embedding_model: BGEEmbeddingModel,
        vector_store: ChromaVectorStore,
    ):
        """Store the embedding model and the underlying Chroma collection."""
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """Embed the question and return the top matching results from the vector store."""

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k,
        )