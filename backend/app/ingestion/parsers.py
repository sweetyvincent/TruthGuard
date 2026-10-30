from pathlib import Path
import fitz
from docx import Document as DocxDocument

def extract_file(path: str, suffix: str) -> list[tuple[str, int | None]]:
    suffix = suffix.lower()
    if suffix == ".pdf":
        doc = fitz.open(path)
        return [(page.get_text("text"), i + 1) for i, page in enumerate(doc)]
    if suffix == ".docx":
        doc = DocxDocument(path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return [(text, None)]
    if suffix == ".txt":
        return [(Path(path).read_text(encoding="utf-8", errors="replace"), None)]
    raise ValueError("Supported file types: PDF, DOCX and TXT")

def chunk_pages(pages, size=900, overlap=150):
    chunks = []
    for text, page in pages:
        clean = " ".join(text.split())
        if not clean: continue
        start = 0
        while start < len(clean):
            end = min(len(clean), start + size)
            piece = clean[start:end].strip()
            if piece: chunks.append((piece, page))
            if end == len(clean): break
            start = max(start + 1, end - overlap)
    return chunks
