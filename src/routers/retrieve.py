from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag import MultilingualRAG

router = APIRouter(prefix="/retrieve", tags=["Retrieval"])

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def retrieve_docs(request: QueryRequest):
    try:
        rag = MultilingualRAG()
        results = rag.query(request.query, n_results=3)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
