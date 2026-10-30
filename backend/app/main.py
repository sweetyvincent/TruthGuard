from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.database import Base, engine
from app.routes import documents, questions

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0", description="Evidence-grounded document QA with adversarial checks")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(documents.router); app.include_router(questions.router)
@app.get("/")
def root(): return {"name": "TruthGuard API", "status": "running", "docs": "/docs"}
@app.get("/health")
def health(): return {"status": "ok"}
