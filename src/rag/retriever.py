from .embeddings import BGEEmbeddingModel
from .vectore_store import ChromaVectorStore


class VectorRetriever:

    def __init__(
        self,
        embedding_model: BGEEmbeddingModel,
        vector_store: ChromaVectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k,
        )