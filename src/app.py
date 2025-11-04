from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from routers import ingest, retrieve, generate
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "testkey")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

app = FastAPI(title="Healthcare RAG Backend", version="1.0")

def verify_api_key_dependency(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


app.include_router(ingest.router)
app.include_router(retrieve.router)
app.include_router(generate.router)

@app.get("/")
def root(api_key: str = Depends(verify_api_key_dependency)):
    return {"status": "ok", "message": "Healthcare RAG backend running"}
