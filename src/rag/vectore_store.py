import chromadb


class ChromaVectorStore:

    def __init__(
        self,
        collection_name: str = "uae_legislation",
        persist_directory: str = "./chroma_db",
    ):
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
    ) -> list[str]:

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        return results["documents"][0]