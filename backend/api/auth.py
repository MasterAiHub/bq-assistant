from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.post("/api/auth/login")
async def login(request: Request):
    try:
        data = await request.json()
        email = data.get("email", "")
        password = data.get("password", "")
        
        # Validate user (simplified - should check database)
        if email and password:
            access_token = jwt.encode(
                {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            refresh_token = jwt.encode(
                {"sub": email, "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)},
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            return JSONResponse({
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            })
        else:
            return JSONResponse({
                "success": False,
                "error": "Invalid credentials"
            }, status_code=401)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)
