"""
Chunking utilities for splitting legal text into retrieval-friendly segments.

This module turns long legislative pages into article, clause, and sub-clause chunks
that can be indexed and searched efficiently.
"""

import re

from .rag import Chunk


class SmartChunker:
    """Split legal documents into article- and clause-aware chunks."""

    def __init__(self, max_chars: int = 2000):
        """Store the maximum character length allowed for each chunk."""
        self.max_chars = max_chars

    def split(self, documents: list[str]) -> list[Chunk]:
        """Return text chunks with metadata describing their source page and article."""
        chunks: list[Chunk] = []

        for page_number, page in enumerate(documents, start=1):

            articles = self._extract_articles(page)

            for article_title, article_text in articles:

                clauses = self._extract_clauses(article_text)

                for clause_number, clause_text in clauses:

                    if len(clause_text) <= self.max_chars:
                        chunks.append(
                            Chunk(
                                text=clause_text,
                                metadata={
                                    "page": page_number,
                                    "article": article_title,
                                    "clause": clause_number,
                                },
                            )
                        )

                    else:
                        smaller_chunks = self._split_large_clause(
                            clause_text
                        )

                        for index, smaller_chunk in enumerate(
                            smaller_chunks,
                            start=1,
                        ):
                            chunks.append(
                                Chunk(
                                    text=smaller_chunk,
                                    metadata={
                                        "page": page_number,
                                        "article": article_title,
                                        "clause": clause_number,
                                        "part": index,
                                    },
                                )
                            )

        return chunks

    # ---------------------------------------------------------
    # Articles
    # ---------------------------------------------------------

    def _extract_articles(
        self,
        text: str,
    ) -> list[tuple[str, str]]:
        """Find article boundaries and return text grouped by article heading."""

        pattern = r"(?mi)^\s*Article\s*\(\s*(\d+)\s*\)\s*$"

        matches = list(re.finditer(pattern, text))

        if not matches:
            return []

        articles = []

        for i, match in enumerate(matches):

            article_number = match.group(1)

            start = match.end()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            article_text = text[start:end].strip()

            if article_text:
                articles.append(
                    (
                        f"Article ({article_number})",
                        article_text,
                    )
                )

        return articles

    # ---------------------------------------------------------
    # Clauses
    # ---------------------------------------------------------

    def _extract_clauses(
        self,
        article_text: str,
    ) -> list[tuple[str, str]]:
        """Extract numbered clauses inside an article, or treat the article as one block."""

        # Supports:
        #
        # 1. Text
        # 2. Text
        #
        # and PDF extraction such as:
        #
        # 1\. Text
        #
        pattern = r"(?m)^\s*(\d+)\s*\\?\.\s+"

        matches = list(re.finditer(pattern, article_text))

        # Article has no numbered clauses.
        # Treat the whole article as one unit.
        if not matches:
            return [
                ("1", article_text.strip())
            ]

        clauses = []

        for i, match in enumerate(matches):

            clause_number = match.group(1)

            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(article_text)

            clause_text = article_text[start:end].strip()

            if clause_text:
                clauses.append(
                    (
                        clause_number,
                        clause_text,
                    )
                )

        return clauses

    # ---------------------------------------------------------
    # Large Clause
    # ---------------------------------------------------------

    def _split_large_clause(
        self,
        clause: str,
    ) -> list[str]:
        """Break oversized clauses into paragraph and sub-clause chunks that fit the size limit."""

        paragraphs = self._split_paragraphs(clause)

        chunks = []
        current = ""

        for paragraph in paragraphs:

            if not current:
                current = paragraph
                continue

            candidate = f"{current}\n\n{paragraph}"

            if len(candidate) <= self.max_chars:
                current = candidate

            else:
                chunks.append(current)
                current = paragraph

        if current:
            chunks.append(current)

        # A single paragraph can still be larger
        # than max_chars.
        final_chunks = []

        for chunk in chunks:

            if len(chunk) <= self.max_chars:
                final_chunks.append(chunk)

            else:
                final_chunks.extend(
                    self._split_by_sub_clauses(chunk)
                )

        return final_chunks

    # ---------------------------------------------------------
    # Paragraphs
    # ---------------------------------------------------------

    def _split_paragraphs(
        self,
        text: str,
    ) -> list[str]:
        """Normalize spacing and split the text into paragraph units."""

        # Normalize excessive whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Preserve paragraph boundaries
        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]

    # ---------------------------------------------------------
    # Sub-clauses
    # ---------------------------------------------------------

    def _split_by_sub_clauses(
        self,
        text: str,
    ) -> list[str]:
        """Split a large clause by alphabetic sub-items such as a., b., or (a)."""

        # Examples:
        #
        # a. Something
        # b. Something
        #
        # (a) Something
        # (b) Something
        #
        pattern = r"(?m)^\s*(?:\([a-zA-Z]\)|[a-zA-Z]\.)\s+"

        matches = list(
            re.finditer(pattern, text)
        )

        if not matches:
            return self._hard_split(text)

        chunks = []

        for i, match in enumerate(matches):

            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            sub_clause = text[start:end].strip()

            if sub_clause:
                chunks.append(sub_clause)

        return self._merge_small_chunks(chunks)

    # ---------------------------------------------------------
    # Hard split - final fallback
    # ---------------------------------------------------------

    def _hard_split(
        self,
        text: str,
    ) -> list[str]:
        """Fallback splitter that cuts oversized text at sentence boundaries or a hard character limit."""

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.max_chars

            if end >= len(text):
                chunks.append(
                    text[start:].strip()
                )
                break

            # Try to break at a sentence boundary.
            split_position = text.rfind(
                ". ",
                start,
                end,
            )

            if split_position <= start:
                split_position = end

            else:
                split_position += 1

            chunks.append(
                text[start:split_position].strip()
            )

            start = split_position

        return [
            chunk
            for chunk in chunks
            if chunk
        ]

    # ---------------------------------------------------------
    # Merge small sub-clause chunks
    # ---------------------------------------------------------

    def _merge_small_chunks(
        self,
        chunks: list[str],
    ) -> list[str]:
        """Combine nearby short sub-clause fragments into a single chunk when possible."""

        merged = []

        current = ""

        for chunk in chunks:

            if not current:
                current = chunk
                continue

            candidate = f"{current}\n\n{chunk}"

            if len(candidate) <= self.max_chars:
                current = candidate

            else:
                merged.append(current)
                current = chunk

        if current:
            merged.append(current)

        return merged