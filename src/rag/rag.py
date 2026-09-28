from typing import Protocol
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    metadata: dict


# ---------- Abstractions ----------

class DocumentLoader(Protocol):

    def load(self, path: str) -> list[str]:
        ...


class EmbeddingModel(Protocol):

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...

class Chunker(Protocol):

    def split(self, documents: list[str]) -> list[Chunk]:
        ...


class Retriever(Protocol):

    def retrieve(self, question: str, top_k: int = 5) -> list[str]:
        ...

class VectorStore(Protocol):

    def add(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict]
    ) -> None:
        ...

    def search(
        self,
        embedding: list[float],
        top_k: int = 5
    ) -> list[str]:
        ...




# ---------- Implementations ----------

class SimpleDocumentLoader:

    def load(self, path: str) -> list[str]:
        # Read PDF / Markdown / TXT
        return []


class OpenAIEmbedding:

    def embed(self, texts: list[str]) -> list[list[float]]:
        # Call embedding model
        return []

class SimpleChunker:

    def split(self, documents: list[str]) -> list[str]:
        # Split documents into smaller chunks
        return []

class VectorRetriever:

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ) -> list[str]:

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k
        )

# ---------- RAG ----------

class RAG:

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: Chunker,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        retriever: Retriever
    ):
        self.loader = loader
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.retriever = retriever

    def ingest(self, path: str) -> None:

        documents = self.loader.load(path)

        chunks = self.chunker.split(documents)

        embeddings = self.embedding_model.embed(chunks)

        self.vector_store.add(
            chunks,
            embeddings
        )
        
    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ) -> list[str]:

        return self.retriever.retrieve(
            question,
            top_k
        )

