from fastapi import FastAPI
from app.schemas.document import DocumentCreate, SearchRequest

app = FastAPI(
    title="AI-Powered Semantic Search API",
    description="Multi-tenant B2B search engine with Qdrant and Redis",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "online", "version": "1.0.0"}

@app.post("/index")
async def index_document(doc: DocumentCreate):
    # This is where we will call Celery and Qdrant next
    return {"message": "Document received for indexing", "tenant": doc.tenant_id}