from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag import MultilingualRAG

router = APIRouter(prefix="/generate", tags=["Generation"])

class GenerateRequest(BaseModel):
    query: str


@router.post("/")
def generate_response(request: GenerateRequest):
    try:
        rag = MultilingualRAG()
        retraived_info = rag.query(request.query, n_results=3,)
        lang = retraived_info["query_language"]
        combined_text = " ".join([doc["content"] for doc in retraived_info["results"]])
        mock_response = f"Based on retrieved documents, here’s the summary: {combined_text}..."

        
        return {
            "input_language": lang,
            "output_language": lang,
            "response": mock_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
