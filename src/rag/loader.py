"""File-loading utilities for extracting text from PDF legal documents."""

from pathlib import Path
from dataclasses import dataclass
from pypdf import PdfReader

@dataclass
class DocumentPage:
    """Store extracted text and its source location for one PDF page.

    Attributes:
        text: Extracted and trimmed text content of the page.
        source: Name of the PDF file containing the page.
        page: Zero-based page index reported by the PDF reader.
    """

    text: str
    source: str
    page: int


class PDFLoader:
    """Extract page text from a PDF file or all PDFs in a directory."""

    def load(self, path: str) -> list[DocumentPage]:
        """Read PDF pages and preserve each page's source file and page index.

        Args:
            path: Path to one PDF file or a directory of PDF files.

        Returns:
            DocumentPage records for pages containing extractable text, ordered
            by file name and then by page.

        Raises:
            FileNotFoundError: The given path does not exist.
            ValueError: The path is a file whose extension is not PDF.
        """
        path = Path(path)

        if path.is_dir():
            documents = []

            for pdf_file in sorted(path.glob("*.pdf")):
                documents.extend(self.load(str(pdf_file)))

            return documents

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file: {path}")

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(
                    DocumentPage(
                        text=text.strip(), 
                        source=path.name, 
                        page=page.page_number
                    )
                )

        return pages