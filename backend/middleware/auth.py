from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
import os
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for JWT token validation"""

    def __init__(self, app):
        super().__init__(app)
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm = "HS256"

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public routes like health check, login, and static files
        if request.url.path.startswith("/api/health") or \
           request.url.path.startswith("/api/auth/login") or \
           request.url.path.startswith("/api/users/register") or \
           request.url.path.startswith("/static/") or \
           request.url.path == "/":
            response = await call_next(request)
            return response

        token = request.headers.get("Authorization")

        if not token:
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)

        try:
            scheme, credentials = token.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            
            payload = jwt.decode(credentials, self.secret_key, algorithms=[self.algorithm])
            request.state.user_email = payload.get("sub")
            if not request.state.user_email:
                raise HTTPException(status_code=401, detail="Invalid token payload")

        except jwt.ExpiredSignatureError:
            logger.warning("Expired token attempt")
            return JSONResponse({"detail": "Token has expired"}, status_code=401)
        except jwt.InvalidTokenError:
            logger.warning("Invalid token attempt")
            return JSONResponse({"detail": "Invalid token"}, status_code=401)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JSONResponse({"detail": "Authentication failed"}, status_code=401)

        response = await call_next(request)
        return response
