"""File-loading utilities for extracting text from PDF legal documents."""

from pathlib import Path
from dataclasses import dataclass
from pypdf import PdfReader

@dataclass
class DocumentPage:
    text: str
    source: str
    page: int


class PDFLoader:
    """Load one or more PDF files and return their page text as strings."""

    def load(self, path: str) -> list[DocumentPage]:
        """Read a PDF file or a directory of PDFs and return all extracted page texts."""
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