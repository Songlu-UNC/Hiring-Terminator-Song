from __future__ import annotations

from pypdf import PdfReader


def extract_pdf_text(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile containing a PDF."""
    try:
        reader = PdfReader(uploaded_file)
        pages = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"\n--- Page {i} ---\n{text}")
        return "\n".join(pages).strip()
    except Exception as exc:
        raise ValueError(f"Could not read PDF file '{getattr(uploaded_file, 'name', 'uploaded file')}': {exc}") from exc


def truncate_text(text: str, max_chars: int = 18000) -> str:
    """Keep prompts within a practical size for small demo models."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[TRUNCATED FOR DEMO]"
