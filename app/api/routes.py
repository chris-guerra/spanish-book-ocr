from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from typing import List
from ..core.ocr import OCRProcessor
from ..core.config import settings

router = APIRouter()
ocr_processor = OCRProcessor()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF file for OCR processing."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_path = settings.INPUT_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return {"filename": file.filename, "status": "uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_languages() -> List[str]:
    """Get list of available OCR languages."""
    return ocr_processor.get_available_languages()

@router.post("/download-language/{language}")
async def download_language(language: str):
    """Download a new language data file."""
    success = ocr_processor.download_language_data(language)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to download language data for {language}")
    return {"language": language, "status": "downloaded"} 