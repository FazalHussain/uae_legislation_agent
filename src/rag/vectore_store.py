"""Vector store interface for persisting and querying chunk embeddings in Chroma."""

import chromadb

from .rag import Chunk


class ChromaVectorStore:
    """Persist chunk embeddings in Chroma and retrieve nearest passages."""

    def __init__(
        self,
        collection_name: str = "uae_legislation",
        persist_directory: str = "./chroma_db",
    ):
        """Open or create a persistent Chroma collection for legislation.

        Args:
            collection_name: Name of the Chroma collection to open or create.
            persist_directory: Filesystem directory used to persist the database.

        Returns:
            None.
        """
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
        """Add chunk documents and their vectors and metadata to the collection.

        Args:
            chunks: Text documents to store.
            embeddings: Embedding vectors aligned with ``chunks``.
            metadata: Metadata dictionaries aligned with ``chunks``.

        Returns:
            None.
        """

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
        """Query Chroma and return the nearest stored chunks.

        Args:
            embedding: Query vector used for nearest-neighbor search.
            top_k: Maximum number of matches requested from Chroma.

        Returns:
            Chunk objects containing each matched document and its metadata,
            ordered as returned by Chroma.
        """

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