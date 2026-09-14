"""
Hierarchical chunker for UAE legislation documents.
Creates chunks aligned with legal hierarchy (Preamble → Articles → Paragraphs)
while preserving document-level metadata on every chunk.
"""

from dataclasses import dataclass
from typing import Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from legislation_parser import DocumentStructure, Article, split_long_paragraph


@dataclass
class ChunkConfig:
    """Configuration for chunking behavior."""
    max_chunk_size: int = 500
    overlap: int = 50


class HierarchicalLegalChunker:
    """
    Custom chunker that produces chunks with rich metadata aligned
    to the legal document hierarchy.
    """

    def __init__(self, max_chunk_size: int = 500, overlap: int = 50):
        """
        Initialize the chunker.

        Args:
            max_chunk_size: Soft limit for paragraph splitting (default 500)
            overlap: Overlap for recursive paragraph splits (default 50)
        """
        self.config = ChunkConfig(max_chunk_size=max_chunk_size, overlap=overlap)
        # Recursive splitter for long paragraphs only
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ". ", "؟ ", " ", ""],
            keep_separator=True,
        )

    def chunk_document(
        self,
        doc_structure: DocumentStructure,
        doc_metadata: dict,
    ) -> list[Document]:
        """
        Chunk a document into hierarchical chunks with full metadata.

        Args:
            doc_structure: Parsed document structure
            doc_metadata: Document-level metadata (law_number, year, titles, etc.)

        Returns:
            List of LangChain Document objects with page_content and metadata
        """
        chunks = []

        # Build base metadata that goes on EVERY chunk
        base_metadata = {
            "doc_id": doc_structure.doc_id,
            "law_number": doc_metadata.get("law_number", ""),
            "year": doc_metadata.get("year", ""),
            "title_en": doc_metadata.get("title_en", ""),
            "title_ar": doc_metadata.get("title_ar", ""),
            "issuing_authority": doc_metadata.get("issuing_authority", ""),
            "effective_date": doc_metadata.get("effective_date", ""),
            "language": doc_structure.language,
        }

        # 1. Preamble chunk (single chunk, full preamble)
        if doc_structure.preamble.strip():
            preamble_chunk = self._create_chunk(
                content=doc_structure.preamble.strip(),
                base_metadata=base_metadata,
                chunk_type="preamble",
                hierarchy_level="preamble",
                article_number=None,
                paragraph_number=None,
                article_id=None,
                parent_article_id=None,
            )
            chunks.append(preamble_chunk)

        # 2. Article chunks
        for article in doc_structure.articles:
            article_chunks = self._chunk_article(article, base_metadata)
            chunks.extend(article_chunks)

        return chunks

    def _chunk_article(self, article: Article, base_metadata: dict) -> list[Document]:
        """
        Chunk a single article based on its length and structure.

        Strategy:
        - Short article (full text <= max_chunk_size): single chunk
        - Long article: one chunk per paragraph
        - Very long paragraph: recursively split with overlap
        """
        chunks = []

        # Check if article is short enough to keep as single chunk
        full_article_text = article.text.strip()
        if len(full_article_text) <= self.config.max_chunk_size:
            # Single chunk for the entire article
            chunk = self._create_chunk(
                content=full_article_text,
                base_metadata=base_metadata,
                chunk_type="article",
                hierarchy_level="article",
                article_number=article.number,
                paragraph_number=None,
                article_id=article.article_id,
                parent_article_id=None,
            )
            chunks.append(chunk)
            return chunks

        # Long article: split by paragraphs
        for para_idx, paragraph in enumerate(article.paragraphs):
            para_text = paragraph.strip()
            if not para_text:
                continue

            if len(para_text) <= self.config.max_chunk_size:
                # Paragraph fits in one chunk
                chunk = self._create_chunk(
                    content=para_text,
                    base_metadata=base_metadata,
                    chunk_type="paragraph",
                    hierarchy_level="paragraph",
                    article_number=article.number,
                    paragraph_number=para_idx + 1,
                    article_id=article.article_id,
                    parent_article_id=article.article_id,
                )
                chunks.append(chunk)
            else:
                # Long paragraph: recursive split preserving metadata
                sub_chunks = split_long_paragraph(
                    para_text,
                    self.config.max_chunk_size,
                    self.config.overlap,
                )
                for sub_idx, sub_chunk in enumerate(sub_chunks):
                    chunk = self._create_chunk(
                        content=sub_chunk,
                        base_metadata=base_metadata,
                        chunk_type="paragraph",
                        hierarchy_level="paragraph",
                        article_number=article.number,
                        paragraph_number=para_idx + 1,
                        article_id=article.article_id,
                        parent_article_id=article.article_id,
                    )
                    # Add sub-chunk info to metadata
                    chunk.metadata["sub_chunk_index"] = sub_idx
                    chunk.metadata["sub_chunk_total"] = len(sub_chunks)
                    chunks.append(chunk)

        return chunks

    def _create_chunk(
        self,
        content: str,
        base_metadata: dict,
        chunk_type: str,
        hierarchy_level: str,
        article_number: Optional[int],
        paragraph_number: Optional[int],
        article_id: Optional[str],
        parent_article_id: Optional[str],
    ) -> Document:
        """
        Create a LangChain Document with full metadata.

        Args:
            content: Chunk text content
            base_metadata: Document-level metadata (copied to every chunk)
            chunk_type: Type of chunk (preamble|article|paragraph)
            hierarchy_level: Same as chunk_type for filtering
            article_number: Article number (None for preamble)
            paragraph_number: Paragraph number within article (None for article-level)
            article_id: Shared article ID for cross-lingual linking
            parent_article_id: Parent article ID for paragraph chunks

        Returns:
            LangChain Document with page_content and metadata
        """
        metadata = base_metadata.copy()
        metadata.update({
            "chunk_type": chunk_type,
            "hierarchy_level": hierarchy_level,
            "article_number": article_number,
            "paragraph_number": paragraph_number,
            "article_id": article_id,
            "parent_article_id": parent_article_id,
        })

        # Remove None values for cleaner metadata
        metadata = {k: v for k, v in metadata.items() if v is not None}

        return Document(page_content=content, metadata=metadata)


def create_chunker(max_chunk_size: int = 500, overlap: int = 50) -> HierarchicalLegalChunker:
    """Factory function to create a configured chunker."""
    return HierarchicalLegalChunker(max_chunk_size=max_chunk_size, overlap=overlap)