"""Core abstractions and orchestration logic for the legislation RAG pipeline.

This module defines the data contracts and the high-level RAG workflow used to load,
chunk, embed, index, and retrieve legal text.
"""

from typing import Protocol
from dataclasses import dataclass


@dataclass
class Chunk:
    """A single searchable chunk of legal text with metadata for grounding."""

    text: str
    metadata: dict


# ---------- Abstractions ----------

class DocumentLoader(Protocol):
    """Contract for loaders that turn files into raw document pages or text."""

    def load(self, path: str) -> list[str]:
        """Return a list of documents or pages extracted from the given source path."""
        ...


class EmbeddingModel(Protocol):
    """Contract for models that convert text into embeddings."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return a vector embedding for each supplied text item."""
        ...


class Chunker(Protocol):
    """Contract for chunkers that split raw documents into searchable segments."""

    def split(self, documents: list[str]) -> list[Chunk]:
        """Return a list of chunk objects produced from the source documents."""
        ...


class Retriever(Protocol):
    """Contract for retrievers that return relevant chunks for a query."""

    def retrieve(self, question: str, top_k: int = 5) -> list[str]:
        """Return the most relevant text snippets for the question."""
        ...


class VectorStore(Protocol):
    """Contract for vector stores used to index and query chunk embeddings."""

    def add(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict]
    ) -> None:
        """Store chunk text, embeddings, and metadata for later retrieval."""
        ...

    def search(
        self,
        embedding: list[float],
        top_k: int = 5
    ) -> list[str]:
        """Search nearest neighbors for a query embedding and return matching chunks."""
        ...


# ---------- Implementations ----------

class SimpleDocumentLoader:
    """Minimal placeholder loader for document ingestion workflows."""

    def load(self, path: str) -> list[str]:
        """Read a file and return its text content in a simple list format."""
        # Read PDF / Markdown / TXT
        return []


class OpenAIEmbedding:
    """Minimal placeholder embedding class for external model integration."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Call an external embedding service and return vector encodings."""
        # Call embedding model
        return []


class SimpleChunker:
    """Minimal placeholder chunker for simple document splitting workflows."""

    def split(self, documents: list[str]) -> list[str]:
        """Split document text into smaller chunks without special legal parsing."""
        # Split documents into smaller chunks
        return []


class VectorRetriever:
    """Retrieve supporting chunks by turning the question into an embedding and querying the vector store."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore
    ):
        """Store the embedding model and vector store dependencies."""
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ) -> list[str]:
        """Encode the query and return the top matching chunks from the vector index."""

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k
        )


# ---------- RAG ----------

class RAG:
    """Coordinate loading, chunking, embedding, indexing, and retrieval for legal text."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: Chunker,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        retriever: Retriever
    ):
        """Capture the service dependencies needed to build the retrieval pipeline."""
        self.loader = loader
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.retriever = retriever

    def ingest(self, path: str) -> None:
        """Load a source file, split it into chunks, embed the chunks, and store them."""

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
        """Query the configured retriever for the most relevant legal passages."""

        return self.retriever.retrieve(
            question,
            top_k
        )

