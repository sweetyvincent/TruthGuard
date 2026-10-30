from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from app.database.database import get_db
from app.database.models import Chunk, QueryLog
from app.retrieval.search import retrieve
from app.agents.synthesizer import synthesize
from app.verification.adversary import challenge
from app.resolution.engine import resolve

router = APIRouter(prefix="/api", tags=["questions"])
class QueryRequest(BaseModel): question: str = Field(min_length=3, max_length=2000)

@router.post("/query")
def ask(req: QueryRequest, db: Session = Depends(get_db)):
    chunks = db.query(Chunk).options(joinedload(Chunk.document)).all()
    ranked = retrieve(req.question, chunks)
    evidence = [c for _, c in ranked]
    draft = synthesize(req.question, evidence)
    findings = challenge(evidence)
    resolution = resolve(findings)
    answer = draft if not findings else draft + "\n\nVerification note: potential conflicts require human review."
    citations = [{"document_id": c.document_id, "filename": c.document.filename, "page": c.page_number, "chunk_id": c.id, "text": c.text, "score": round(score, 4)} for score,c in ranked]
    result = {"question": req.question, "answer": answer, "status": resolution["status"], "resolution": resolution, "conflicts": findings, "citations": citations,
              "method": "Lexical retrieval + extractive synthesis + heuristic adversarial checks (no LLM is simulated)."}
    log = QueryLog(question=req.question, answer=answer, status=resolution["status"], details=result)
    db.add(log); db.commit(); db.refresh(log)
    result["query_id"] = log.id
    return result

@router.get("/history")
def history(db: Session = Depends(get_db)):
    return [{"id": q.id, "question": q.question, "answer": q.answer, "status": q.status, "created_at": q.created_at} for q in db.query(QueryLog).order_by(QueryLog.created_at.desc()).limit(50)]
