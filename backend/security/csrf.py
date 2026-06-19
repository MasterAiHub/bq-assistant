from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os
import secrets
import logging

logger = logging.getLogger(__name__)

class CSRFMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware"""

    def __init__(self, app, secret_key: str = None):
        super().__init__(app)
        self.secret_key = secret_key or os.getenv("CSRF_SECRET_KEY", secrets.token_hex(32))
        if not secret_key:
            logger.warning("CSRF_SECRET_KEY not set, using a randomly generated key. This is not persistent across restarts.")

    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            if "X-CSRF-Token" not in request.headers:
                raise HTTPException(status_code=403, detail="CSRF token missing")

            client_csrf_token = request.headers["X-CSRF-Token"]
            server_csrf_token = request.cookies.get("csrf_token")

            if not server_csrf_token or client_csrf_token != server_csrf_token:
                raise HTTPException(status_code=403, detail="CSRF token mismatch")

        response = await call_next(request)

        if "csrf_token" not in request.cookies:
            csrf_token = secrets.token_hex(32)
            response.set_cookie("csrf_token", csrf_token, httponly=True, secure=True, samesite="lax")

        return response
