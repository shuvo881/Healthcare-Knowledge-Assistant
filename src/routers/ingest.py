from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from rag import MultilingualRAG
from pathlib import Path

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

UPLOAD_DIR = Path("media") / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def ingest_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file as binary to avoid encoding issues
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        # Process the file
        rag = MultilingualRAG()
        rag.add_txt_files([file_path])

        return {"status": "success", "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
