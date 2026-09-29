"""Vector store interface for persisting and querying chunk embeddings in Chroma."""

import chromadb

from .rag import Chunk


class ChromaVectorStore:
    """Persist chunk embeddings in a local Chroma database and retrieve nearest matches."""

    def __init__(
        self,
        collection_name: str = "uae_legislation",
        persist_directory: str = "./chroma_db",
    ):
        """Create or open the persistent Chroma collection for legislation embeddings."""
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """Insert chunk text and metadata into the Chroma collection."""

        ids = [
            f"chunk-{i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:
        """Return the top matching chunk texts for a query embedding."""

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        return [
            Chunk(
                text=text,
                metadata=metadata,
            )
            for text, metadata in zip(documents, metadatas)
        ]