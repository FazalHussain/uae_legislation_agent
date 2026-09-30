"""
Chunking utilities for splitting legal text into retrieval-friendly segments.

This module turns long legislative pages into article, clause, and sub-clause chunks
that can be indexed and searched efficiently.
"""

import re

from .rag import Chunk
from .loader import DocumentPage


class SmartChunker:
    """Split legal pages into article- and clause-aware searchable chunks."""

    def __init__(self, max_chars: int = 2000):
        """Configure the maximum preferred size for each output chunk.

        Args:
            max_chars: Maximum character count used when combining or splitting
                passage text.

        Returns:
            None.
        """
        self.max_chars = max_chars

    def split(self, documents: list[str]) -> list[Chunk]:
        """Create chunks for the articles and clauses in the supplied pages.

        Args:
            documents: DocumentPage records whose text and source metadata are
                used to create chunks.

        Returns:
            Chunk objects containing passage text and metadata for the source
            page, article, clause, and any split-part index.
        """
        chunks: list[Chunk] = []

        for document in documents:
            page_number = document.page
            source = document.source
            page = document.text

            articles = self._extract_articles(page)

            for article_title, article_text in articles:

                clauses = self._extract_clauses(article_text)

                for clause_number, clause_text in clauses:

                    if len(clause_text) <= self.max_chars:
                        chunks.append(
                            Chunk(
                                text=clause_text,
                                metadata={
                                    "chunk_id": (
                                        f"{source}:{page_number}:"
                                        f"{article_title}:{clause_number}"
                                    ),
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
                                        "chunk_id": (
                                            f"{source}:{page_number}:"
                                            f"{article_title}:{clause_number}:part{index}"
                                        ),
                                        "source": source,
                                        "page": page_number,
                                        "article": article_title,
                                        "clause": clause_number,
                                        "part": index,
                                    }
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
        """Locate article headings and separate their associated text.

        Args:
            text: Full text of a legislative page.

        Returns:
            Pairs of article heading and article body; returns an empty list if
            no article headings are found.
        """

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
        """Separate an article into numbered clauses when clause headings exist.

        Args:
            article_text: Body text belonging to one article.

        Returns:
            Pairs of clause number and clause text. If no numbered clauses are
            found, returns the entire article as clause ``1``.
        """

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
        """Split a long clause into smaller paragraph- or sub-clause chunks.

        Args:
            clause: Clause text that exceeds the configured chunk size.

        Returns:
            Ordered text chunks assembled to fit the configured size where
            possible, using the hard splitter as a final fallback.
        """

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
        """Normalize horizontal whitespace and separate nonempty paragraphs.

        Args:
            text: Text that may contain repeated spaces and paragraph breaks.

        Returns:
            A list of trimmed, nonempty paragraph strings in source order.
        """

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
        """Split text at alphabetic sub-clause markers and merge small pieces.

        Args:
            text: Oversized passage that may contain alphabetic sub-items.

        Returns:
            Ordered chunks split at recognized markers; if none are found,
            returns chunks produced by the hard-split fallback.
        """

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
        """Split text at sentence boundaries or the configured character limit.

        Args:
            text: Text to divide when structural splitting is unavailable.

        Returns:
            Ordered, trimmed, nonempty text chunks no longer than the configured
            limit, except where an indivisible boundary requires otherwise.
        """

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
        """Combine adjacent chunks while their joined text fits the size limit.

        Args:
            chunks: Ordered sub-clause text fragments to combine.

        Returns:
            Ordered merged chunks whose combined text does not exceed the
            configured character limit.
        """

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