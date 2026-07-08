from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: Path) -> tuple[str, int]:
	reader = PdfReader(str(pdf_path))
	pages_text: list[str] = []
	for page in reader.pages:
		pages_text.append(page.extract_text() or "")
	return "\n\n".join(pages_text), len(reader.pages)