"""Core abstractions and orchestration logic for the legislation RAG pipeline.

This module defines the data contracts and the high-level RAG workflow used to load,
chunk, embed, index, and retrieve legal text.
"""

from typing import Protocol
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represent one searchable legal-text passage and its source metadata.

    Attributes:
        text: Passage text indexed and returned by the retrieval pipeline.
        metadata: Source fields such as chunk ID, page, article, and clause.
    """

    text: str
    metadata: dict


# ---------- Abstractions ----------

class DocumentLoader(Protocol):
    """Contract for loaders that turn files into raw document pages or text."""

    def load(self, path: str) -> list[str]:
        """Load source content from a file or directory path.

        Args:
            path: File or directory from which source documents are loaded.

        Returns:
            A list of extracted documents or page records.
        """
        ...


class EmbeddingModel(Protocol):
    """Contract for models that convert text into embeddings."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Convert each supplied text into a numeric embedding vector.

        Args:
            texts: Text values to encode.

        Returns:
            One floating-point vector for each input text, in input order.
        """
        ...


class Chunker(Protocol):
    """Contract for chunkers that split raw documents into searchable segments."""

    def split(self, documents: list[str]) -> list[Chunk]:
        """Divide source documents into searchable text chunks.

        Args:
            documents: Source documents or page records to divide.

        Returns:
            Chunk objects containing passage text and source metadata.
        """
        ...


class Retriever(Protocol):
    """Contract for retrievers that return relevant chunks for a query."""

    def retrieve(self, question: str, top_k: int = 5) -> list[str]:
        """Find the highest-ranked passages for a natural-language question.

        Args:
            question: Query used to find relevant legislation.
            top_k: Maximum number of results requested.

        Returns:
            The retrieved passages, ordered by relevance.
        """
        ...

class Reranker(Protocol):
    """Define the interface for sorting retrieved chunks by query relevance."""
    def rerank(self, query: str, results: list["Chunk"], top_k: int = 5,) -> list["Chunk"]:
        """Rescore candidate chunks against a query and select the top results.

        Args:
            query: Search question used to score candidate passages.
            results: Candidate chunks to score and order.
            top_k: Maximum number of ranked chunks to return.

        Returns:
            The highest-scoring chunks in descending relevance order.
        """
        ...


class VectorStore(Protocol):
    """Contract for vector stores used to index and query chunk embeddings."""

    def add(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict]
    ) -> None:
        """Persist chunk content, vectors, and metadata for later search.

        Args:
            chunks: Text content corresponding to the supplied embeddings.
            embeddings: Numeric vectors aligned with the chunk texts.
            metadata: Metadata dictionaries aligned with the chunk texts.

        Returns:
            None.
        """
        ...

    def search(
        self,
        embedding: list[float],
        top_k: int = 5
    ) -> list[str]:
        """Find stored passages nearest to a query embedding.

        Args:
            embedding: Numeric vector representing the search query.
            top_k: Maximum number of nearest results requested.

        Returns:
            Matching passages ordered by their vector-search relevance.
        """
        ...


# ---------- RAG ----------

class RAG:
    """Coordinate ingestion and retrieval across the legislation search services."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: Chunker,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        retriever: Retriever,
        reranker: Reranker,
    ):
        """Initialize the pipeline with its loader, search, and ranking services.

        Args:
            loader: Service that extracts pages from source paths.
            chunker: Service that divides pages into searchable chunks.
            embedding_model: Service that converts text into vectors.
            vector_store: Service that persists text, vectors, and metadata.
            retriever: Service that fetches candidate chunks for a question.
            reranker: Service that orders candidates by query relevance.

        Returns:
            None.
        """
        self.loader = loader
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.retriever = retriever
        self.reranker = reranker

    def ingest(self, path: str) -> None:
        """Load, chunk, embed, and index the documents found at a source path.

        Args:
            path: File or directory containing source documents to index.

        Returns:
            None.
        """

        documents = self.loader.load(path)

        chunks = self.chunker.split(documents)

        texts = [chunk.text for chunk in chunks]

        embeddings = self.embedding_model.embed(texts)

        self.vector_store.add(
            texts,
            embeddings,
            metadata=[chunk.metadata for chunk in chunks],
        )

    def retrieve(self, question: str, top_k: int = 5) -> list[Chunk]:
        """Retrieve candidate passages and rerank them for a legal question.

        Args:
            question: Natural-language question to answer with legislation.
            candidate_k: Maximum number of candidates requested before reranking.
            top_k: Maximum number of reranked chunks to return.

        Returns:
            The highest-ranked chunks, including their text and source metadata.
        """

        return self.retriever.retrieve(question, top_k=top_k)

    def rerank(
        self,
        question: str,
        chunks: list,
        top_k: int = 5,
    ) -> list[Chunk]:
        """Rescore candidate chunks against a question and return the top results.

        Args:
            question: Natural-language question used to score candidate passages.
            chunks: Candidate chunks to score and order.
            top_k: Maximum number of ranked chunks to return.

        Returns:
            The highest-scoring chunks in descending relevance order.
        """

        return self.reranker.rerank(
            question,
            chunks,
            top_k=top_k,
        )

    def format_context(self, chunks) -> str:
        """Format retrieved chunks into LLM-friendly context."""

        formatted_chunks = []

        for index, chunk in enumerate(chunks, start=1):
            formatted_chunks.append(f"--- Context {index} ---\n" f"{chunk}")

        return "\n\n".join(formatted_chunks)
