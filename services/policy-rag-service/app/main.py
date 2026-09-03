from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="LedgerGuard Policy RAG Service", version="1.0.0")

class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=20)
    filters: dict[str, str] = Field(default_factory=dict)

class ContextChunk(BaseModel):
    text: str
    source: str
    score: float

class QueryResponse(BaseModel):
    query: str
    matches: list[ContextChunk]

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "policy-rag-service"}

@app.post("/query", response_model=QueryResponse)
def query_policy(request: QueryRequest) -> QueryResponse:
    # Integration seam: call Gemini embeddings + Pinecone here in production.
    return QueryResponse(query=request.query, matches=[ContextChunk(
        text="Amount drift above the configured tolerance requires review; safe corrections must be auditable.",
        source="finance_policy.md", score=0.0,
    )])
