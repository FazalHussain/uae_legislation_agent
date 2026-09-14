"""
Document loader for UAE legislation documents.
Supports PDF loading via DirectoryLoader + PyPDFLoader, bilingual processing,
and hierarchical chunking with rich metadata.
"""

from pathlib import Path
from typing import Optional

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document

from hierarchical_chunker import HierarchicalLegalChunker, create_chunker
from legislation_parser import (
    DocumentStructure,
    parse_document,
)


def load_pdfs_from_directory(directory: str) -> list[Document]:
    """
    Load PDF documents from a directory using DirectoryLoader with PyPDFLoader.

    Args:
        directory: Path to directory containing PDF files

    Returns:
        List of LangChain Document objects (one per PDF file)
    """
    loader = DirectoryLoader(
        directory,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    documents = loader.load()
    return documents


def process_legislation_directory(
    directory: str,
    max_chunk_size: int = 500,
    overlap: int = 50,
) -> list[Document]:
    """
    Process a directory of legislation PDFs through the full pipeline:
    1. Load PDFs using DirectoryLoader + PyPDFLoader
    2. Group by doc_id (derived from filename)
    3. Combine all pages of each PDF file
    4. For each language version: parse → chunk → attach doc_metadata
    5. Return all chunks with rich hierarchical metadata

    Args:
        directory: Path to directory containing legislation PDFs
        max_chunk_size: Maximum chunk size for paragraph splitting
        overlap: Overlap for recursive paragraph splits

    Returns:
        List of chunked Document objects with full metadata
    """
    # Step 1: Load all PDFs (one Document per page)
    raw_docs = load_pdfs_from_directory(directory)

    # Step 2: Group by doc_id and language, then combine pages
    # Structure: docs_by_id[doc_id][language] = full_text
    docs_by_id = {}
    for doc in raw_docs:
        source_path = Path(doc.metadata.get("source", ""))
        filename = source_path.name
        language = "en" if filename.endswith("-en.pdf") else "ar"

        # Use filename base (without -en/-ar suffix) as grouping key
        base = Path(filename).stem.lower().strip()
        for suffix in ("-en", "-ar"):
            if base.endswith(suffix):
                base = base[:-len(suffix)]
                break
        doc_id = base

        if doc_id not in docs_by_id:
            docs_by_id[doc_id] = {}
        if language not in docs_by_id[doc_id]:
            docs_by_id[doc_id][language] = ""
        docs_by_id[doc_id][language] += doc.page_content + "\n"

    # Step 3: Process each document through the pipeline
    all_chunks = []
    chunker = create_chunker(max_chunk_size=max_chunk_size, overlap=overlap)

    for doc_id, lang_texts in docs_by_id.items():
        # Process each language version independently
        for language, full_text in lang_texts.items():
            # Use the first available filename for this doc_id
            source_filename = f"{doc_id}-{language}.pdf"
            # Parse document structure
            doc_structure = parse_document(
                text=full_text,
                language=language,
                filename=source_filename,
            )

            # Extract document metadata for attachment to all chunks
            doc_metadata = doc_structure.metadata

            # Chunk the document
            chunks = chunker.chunk_document(doc_structure, doc_metadata)

            # Ensure language is set on all chunks
            for chunk in chunks:
                chunk.metadata["language"] = language

            all_chunks.extend(chunks)

    return all_chunks


def load_documents_from_directory(
    directory: str,
    max_chunk_size: int = 500,
    overlap: int = 50,
) -> list[Document]:
    """
    Main entry point - maintains backward compatibility with existing code.

    For PDF legislation documents: uses hierarchical chunking with metadata.
    For text files: falls back to original RecursiveCharacterTextSplitter behavior.

    Args:
        directory: Path to directory containing documents
        max_chunk_size: Maximum chunk size (for legislation chunking)
        overlap: Overlap for recursive splits (for legislation chunking)

    Returns:
        List of Document objects ready for embedding/storage
    """
    dir_path = Path(directory)

    # Check if directory contains PDFs
    pdf_files = list(dir_path.glob("*.pdf"))
    if pdf_files:
        # Use new hierarchical pipeline for legislation PDFs
        return process_legislation_directory(
            directory,
            max_chunk_size=max_chunk_size,
            overlap=overlap,
        )

    # Fallback: original behavior for text files
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = DirectoryLoader(
        directory,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " "],
    )
    return text_splitter.split_documents(documents)


if __name__ == "__main__":
    # Manual testing
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else "legislations"
    docs = load_documents_from_directory(test_dir)[:5]

    print(f"Loaded {len(docs)} chunks from {test_dir}")
    print("-" * 80)

    for i, doc in enumerate(docs):
        meta = doc.metadata
        print(f"Chunk {i + 1}:")
        print(f"  chunk_type: {meta.get('chunk_type')}")
        print(f"  hierarchy_level: {meta.get('hierarchy_level')}")
        print(f"  article_number: {meta.get('article_number')}")
        print(f"  paragraph_number: {meta.get('paragraph_number')}")
        print(f"  language: {meta.get('language')}")
        print(f"  doc_id: {meta.get('doc_id')}")
        print(f"  article_id: {meta.get('article_id')}")
        print(f"  law_number: {meta.get('law_number')}")
        print(f"  year: {meta.get('year')}")
        print(f"  content: {doc.page_content[:150]}...")
        print()