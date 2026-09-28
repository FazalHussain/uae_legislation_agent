from pathlib import Path
from pypdf import PdfReader


class PDFLoader:

    def load(self, path: str) -> list[str]:
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
                pages.append(text.strip())

        return pages