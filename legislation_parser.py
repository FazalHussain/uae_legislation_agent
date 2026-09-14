"""
Structure parser for UAE legislation documents.
Extracts hierarchical structure: metadata, preamble, articles, paragraphs.
Supports both English and Arabic versions.
"""

import hashlib
from pathlib import Path
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Article:
    """Represents a single article with its paragraphs."""
    number: int
    title: Optional[str] = None
    text: str = ""
    paragraphs: list[str] = field(default_factory=list)
    article_id: str = ""


@dataclass
class DocumentStructure:
    """Complete parsed document structure."""
    doc_id: str
    language: str
    metadata: dict = field(default_factory=dict)
    preamble: str = ""
    articles: list[Article] = field(default_factory=list)


def extract_metadata(text: str, language: str) -> dict:
    """
    Extract document-level metadata from the legislation text.

    Args:
        text: Full document text
        language: 'en' or 'ar'

    Returns:
        Dictionary with law_number, year, title_en/ar, issuing_authority, effective_date
    """
    metadata = {
        "law_number": "",
        "year": "",
        "title_en": "",
        "title_ar": "",
        "issuing_authority": "",
        "effective_date": "",
    }

    if language == "en":
        # Extract law number and year from various patterns
        # Pattern 1: "Federal Decree by Law No. (25) of 2024"
        law_match = re.search(r"Federal Decree by Law No\.?\s*\(?\s*(\d+)\s*\)?\s+of\s+(\d{4})", text, re.IGNORECASE)
        # Pattern 2: "Federal Decree-Law No. (51) of 2023"
        if not law_match:
            law_match = re.search(r"Federal Decree.?Law No\.?\s*\(?\s*(\d+)\s*\)?\s+of\s+(\d{4})", text, re.IGNORECASE)
        # Pattern 3: "Federal Decree by Law No. 51 of 2023" (no parentheses)
        if not law_match:
            law_match = re.search(r"Federal Decree by Law No\.?\s*(\d+)\s+of\s+(\d{4})", text, re.IGNORECASE)
        if law_match:
            metadata["law_number"] = law_match.group(1)
            metadata["year"] = law_match.group(2)

        # Extract title (after "Concerning" or "Regarding" or "Promulgating")
        title_match = re.search(r"(?:Concerning|Regarding|Promulgating)\s+(.+?)(?:\n|$)", text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            # Remove trailing page numbers like "1" or "2"
            title = re.sub(r"\s+\d+\s*$", "", title)
            metadata["title_en"] = title

        # Extract issuing authority
        auth_match = re.search(r"President of the\s+([A-Za-z\s]+)", text, re.IGNORECASE)
        if auth_match:
            metadata["issuing_authority"] = f"President of the {auth_match.group(1).strip()}"
        else:
            metadata["issuing_authority"] = "President of the UAE"

        # Extract effective date
        date_match = re.search(r"(?:effective|comes into force).*?(\d{1,2}\s+\w+\s+\d{4})", text, re.IGNORECASE)
        if not date_match:
            # Try alternative format: "Corresponding: 30 / September / 2024 AD"
            date_match = re.search(r"Corresponding:\s*(\d{1,2}\s*/\s*\w+\s*/\s*\d{4})", text, re.IGNORECASE)
        if date_match:
            metadata["effective_date"] = date_match.group(1).replace(" / ", " ")

    else:  # Arabic
        # Extract law number and year from Arabic patterns
        # Pattern 1: "مرسوم بقانون اتحادي رقـــم (25) لسنة2024" (with special Unicode chars)
        law_match = re.search(r"\(?\s*(\d+)\s*\)?\s+لسنة\s*(\d{4})", text)
        # Pattern 2: "رقم 51( لسنة2023" (without parentheses around number)
        if not law_match:
            law_match = re.search(r"رقم\s+(\d+)\(?\s*لسنة\s*(\d{4})", text)
        # Pattern 3: Just year pattern "لسنة2023"
        if not law_match:
            law_match = re.search(r"لسنة\s*(\d{4})", text)
            if law_match:
                metadata["year"] = law_match.group(1)
        if law_match:
            metadata["law_number"] = law_match.group(1)
            metadata["year"] = law_match.group(2)

        # Extract title in Arabic
        title_match = re.search(r"في\s+شأن\s+(.+?)(?:\n|$)", text)
        if title_match:
            metadata["title_ar"] = title_match.group(1).strip()

        # Issuing authority in Arabic
        auth_match = re.search(r"رئيس\s+دولة\s+الإمارات", text)
        if auth_match:
            metadata["issuing_authority"] = "رئيس دولة الإمارات"
        else:
            metadata["issuing_authority"] = "President of the UAE"

        # Effective date in Arabic
        date_match = re.search(r"الموافق\s*:\s*(\d{1,2}\s*/\s*\w+\s*/\s*\d{4})", text)
        if date_match:
            metadata["effective_date"] = date_match.group(1).replace(" / ", " ")

    return metadata


def extract_preamble(text: str) -> str:
    """
    Extract the preamble text (everything before Article 1).

    Args:
        text: Full document text

    Returns:
        Preamble text
    """
    # Find the start of Article 1 (English or Arabic)
    article1_patterns = [
        r"\n\s*Article\s*\(?\s*1\s*\)?",           # English: "Article (1)" or "Article 1"
        r"\n\s*المادة\s*\(?\s*(?:1|الأولى)\s*\)?",  # Arabic: "المادة (1)" or "المادة الأولى"
    ]

    earliest_pos = len(text)
    for pattern in article1_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()

    preamble = text[:earliest_pos].strip()
    return preamble


def extract_articles(text: str, doc_id: str) -> list[Article]:
    """
    Extract all articles with their paragraphs from the document text.

    Args:
        text: Full document text
        doc_id: Document identifier for generating article_id

    Returns:
        List of Article objects
    """
    articles = []

    # Patterns to find articles (English and Arabic)
    article_patterns = [
        (r"Article\s*\(?\s*(\d+)\s*\)?", "en"),  # "Article (1)" or "Article 1"
        (r"المادة\s*\(?\s*(?:(\d+)|(الأولى)|(الثانية)|(الثالثة))\s*\)?", "ar"),  # Arabic
    ]

    # Find all article starts
    article_starts = []
    for pattern, lang in article_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            groups = match.groups()
            if lang == "en":
                article_num = int(groups[0])
            else:
                # Arabic: check which group matched
                if groups[0]:  # digit
                    article_num = int(groups[0])
                elif groups[1]:  # الأولى
                    article_num = 1
                elif groups[2]:  # الثانية
                    article_num = 2
                elif groups[3]:  # الثالثة
                    article_num = 3
                else:
                    continue
            article_starts.append((match.start(), article_num, lang))

    # Sort by position
    article_starts.sort(key=lambda x: x[0])

    # Extract each article
    for i, (start_pos, article_num, lang) in enumerate(article_starts):
        # Determine end position (start of next article or end of text)
        if i + 1 < len(article_starts):
            end_pos = article_starts[i + 1][0]
        else:
            end_pos = len(text)

        article_text = text[start_pos:end_pos].strip()

        # Split into paragraphs (by double newline or numbered paragraphs)
        paragraphs = split_into_paragraphs(article_text, lang)

        # Generate article_id
        article_id = f"{doc_id}-art-{article_num}"

        article = Article(
            number=article_num,
            text=article_text,
            paragraphs=paragraphs,
            article_id=article_id,
        )
        articles.append(article)

    return articles


def split_into_paragraphs(article_text: str, lang: str) -> list[str]:
    """
    Split article text into paragraphs.

    Args:
        article_text: Text of a single article
        lang: Language code ('en' or 'ar')

    Returns:
        List of paragraph strings
    """
    # First, try to split by double newlines
    paragraphs = [p.strip() for p in article_text.split("\n\n") if p.strip()]

    # If that gives only 1 paragraph, try other patterns
    if len(paragraphs) <= 1:
        # Try numbered paragraphs (1., 2., etc.) or Arabic equivalents
        if lang == "en":
            # Split on numbered paragraphs like "1. " or "(1) "
            paragraphs = re.split(r"\n\s*(?:\d+\.|\(\d+\))\s+", article_text)
        else:
            # Arabic numbered paragraphs
            paragraphs = re.split(r"\n\s*(?:\d+\.|\(\d+\))\s+", article_text)

        paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Remove the article header from first paragraph
    if paragraphs:
        # Remove "Article X" or "المادة X" from first paragraph
        first_para = paragraphs[0]
        first_para = re.sub(r"^Article\s+\d+\b\.?\s*", "", first_para, flags=re.IGNORECASE)
        first_para = re.sub(r"^المادة\s*\(?\s*\d+\s*\)?\b\.?\s*", "", first_para)
        paragraphs[0] = first_para.strip()

    return paragraphs


def split_long_paragraph(paragraph: str, max_chars: int, overlap: int) -> list[str]:
    """
    Split a long paragraph into smaller chunks with overlap.

    Args:
        paragraph: Text to split
        max_chars: Maximum characters per chunk
        overlap: Overlap characters between chunks

    Returns:
        List of text chunks
    """
    if len(paragraph) <= max_chars:
        return [paragraph]

    chunks = []
    start = 0

    while start < len(paragraph):
        end = start + max_chars

        # Try to break at sentence boundary
        if end < len(paragraph):
            # Look for sentence ending near the cutoff
            search_start = max(start, end - 100)
            sentence_end = paragraph.rfind(". ", search_start, end)
            if sentence_end == -1:
                sentence_end = paragraph.rfind(".\n", search_start, end)
            if sentence_end == -1:
                sentence_end = paragraph.rfind("؟ ", search_start, end)  # Arabic question mark
            if sentence_end != -1:
                end = sentence_end + 1  # Include the period

        chunk = paragraph[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position with overlap
        start = end - overlap
        if start <= 0:
            start = end

    return chunks


def parse_document(text: str, language: str, filename: str) -> DocumentStructure:
    """
    Parse a full document into its hierarchical structure.

    Args:
        text: Full document text
        language: 'en' or 'ar'
        filename: PDF filename (e.g., "1-en.pdf")

    Returns:
        DocumentStructure with metadata, preamble, and articles
    """
    # Extract document metadata
    metadata = extract_metadata(text, language)

    # Generate doc_id from filename and metadata
    doc_id = generate_doc_id(filename, metadata)

    # Extract preamble
    preamble = extract_preamble(text)

    # Extract articles
    articles = extract_articles(text, doc_id)

    return DocumentStructure(
        doc_id=doc_id,
        language=language,
        metadata=metadata,
        preamble=preamble,
        articles=articles,
    )


def generate_doc_id(filename: str, metadata: dict | None = None) -> str:
    """
    Generate a consistent, human-readable document ID.

    Args:
        filename: PDF filename (e.g., "1-en.pdf")
        metadata: Optional extracted metadata with law_number, year

    Returns:
        Normalized doc_id (e.g., "federal-decree-law-25-2024")
    """
    # Prefer metadata for stable cross-language IDs
    if metadata and metadata.get("law_number") and metadata.get("year"):
        return f"legislation-{metadata['law_number']}-{metadata['year']}"

    # Remove extension and language suffix
    base = Path(filename).stem.lower().strip()
    for suffix in ("-en", "-ar"):
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break

    # Fallback: deterministic hash of filename base
    hash_value = hashlib.sha256(base.encode("utf-8")).hexdigest()[:8]
    return f"doc-{hash_value}"