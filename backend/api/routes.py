from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.post("/api/ai/assist")
async def ai_assist(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")
        context = data.get("context", "")
        
        from backend.services.ai_service import AIService
        ai_service = AIService()
        answer = await ai_service.get_direct_answer(question, context)
        
        return JSONResponse({
            "success": True,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"AI assist error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.post("/api/transcribe")
async def transcribe_audio(request: Request):
    try:
        data = await request.json()
        audio_data = data.get("audio", "")
        
        from backend.services.transcription_service import TranscriptionService
        ts = TranscriptionService()
        transcript = await ts.transcribe(audio_data)
        
        return JSONResponse({
            "success": True,
            "transcript": transcript,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)
