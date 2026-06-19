from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/api/meetings")
async def create_meeting(request: Request):
    try:
        data = await request.json()
        # In a real app, save meeting to DB
        logger.info(f"Meeting created: {data.get('title')}")
        return JSONResponse({
            "success": True,
            "message": "Meeting created successfully",
            "meeting_id": "mock_meeting_id_123",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error creating meeting: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.get("/api/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    try:
        # In a real app, retrieve meeting from DB
        return JSONResponse({
            "success": True,
            "meeting_id": meeting_id,
            "title": "Mock Meeting Title",
            "transcript": [
                {"speaker": "John", "text": "Hello team", "timestamp": datetime.utcnow().isoformat()},
                {"speaker": "Jane", "text": "Hi John", "timestamp": datetime.utcnow().isoformat()}
            ],
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting meeting {meeting_id}: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)
