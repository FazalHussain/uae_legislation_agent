"""Embed legislation questions and retrieve matching chunks from Chroma."""

from .rag import Chunk

from .embeddings import BGEEmbeddingModel
from .vectore_store import ChromaVectorStore


class VectorRetriever:
    """Retrieve legislation chunks by embedding a query and searching a vector store.

    Args:
        embedding_model: Model used to convert the question into a vector.
        vector_store: Store queried with the question vector.
    """

    def __init__(
        self,
        embedding_model: BGEEmbeddingModel,
        vector_store: ChromaVectorStore,
    ):
        """Initialize the retriever with its embedding and storage dependencies.

        Args:
            embedding_model: Model used to embed question text.
            vector_store: Store used to find chunks nearest to the question vector.

        Returns:
            None.
        """
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 20,
    ) -> list[Chunk]:
        """Find the most relevant chunks for a question.

        Args:
            question: Natural-language query to embed and search for.
            top_k: Maximum number of matching chunks to request.

        Returns:
            A list of matching chunks returned by the vector store.
        """

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k,
        )