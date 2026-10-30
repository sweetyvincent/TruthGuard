from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import hashlib, os
from app.database.database import get_db
from app.database.models import Document, Chunk
from app.config import settings
from app.ingestion.parsers import extract_file, chunk_pages

router = APIRouter(prefix="/api/documents", tags=["documents"])
ALLOWED = {".pdf", ".docx", ".txt"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED: raise HTTPException(400, "Only PDF, DOCX and TXT files are supported")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024: raise HTTPException(413, "File exceeds upload limit")
    os.makedirs(settings.upload_dir, exist_ok=True)
    digest = hashlib.sha256(content).hexdigest()
    existing = db.query(Document).filter_by(content_hash=digest).first()
    if existing: return {"id": existing.id, "filename": existing.filename, "chunks": len(existing.chunks), "duplicate": True}
    safe_name = Path(file.filename).name
    stored = os.path.join(settings.upload_dir, f"{digest}{suffix}")
    with open(stored, "wb") as f: f.write(content)
    try:
        pages = extract_file(stored, suffix)
        pieces = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)
    except Exception as e:
        os.remove(stored)
        raise HTTPException(400, f"Could not process document: {e}")
    if not pieces: raise HTTPException(400, "No extractable text found. Scanned PDFs need OCR before upload.")
    doc = Document(filename=safe_name, title=Path(safe_name).stem, content_hash=digest)
    db.add(doc); db.flush()
    db.add_all([Chunk(document_id=doc.id, text=t, page_number=p, chunk_index=i) for i, (t,p) in enumerate(pieces)])
    db.commit(); db.refresh(doc)
    return {"id": doc.id, "filename": doc.filename, "chunks": len(pieces), "duplicate": False}

@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [{"id": d.id, "filename": d.filename, "title": d.title, "uploaded_at": d.uploaded_at, "chunks": len(d.chunks)} for d in docs]

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    db.delete(doc); db.commit()
    return {"deleted": document_id}
