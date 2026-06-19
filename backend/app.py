from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import logging

from backend.api import routes, auth, meetings, users, billing
from backend.middleware.auth import AuthMiddleware
from backend.middleware.security_headers import SecurityHeadersMiddleware
from backend.security.csrf import CSRFMiddleware
from backend.utils.logger import setup_logging

# Setup logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="BQ AI Assistant API",
    description="Backend API for the BQ AI Assistant, providing AI assistance, transcription, and secure user management.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add security middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(CSRFMiddleware, secret_key=os.getenv("CSRF_SECRET_KEY"))

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="frontend/templates")

# Include API routers
app.include_router(routes.router)
app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(users.router)
app.include_router(billing.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "BQ AI Assistant"})

@app.get("/manifesto", response_class=HTMLResponse)
async def read_manifesto(request: Request):
    return templates.TemplateResponse("pages/manifesto.html", {"request": request, "title": "Manifesto"})

@app.get("/press", response_class=HTMLResponse)
async def read_press(request: Request):
    return templates.TemplateResponse("pages/press.html", {"request": request, "title": "Press"})

@app.get("/help", response_class=HTMLResponse)
async def read_help(request: Request):
    return templates.TemplateResponse("pages/help.html", {"request": request, "title": "Help"})

@app.get("/privacy", response_class=HTMLResponse)
async def read_privacy(request: Request):
    return templates.TemplateResponse("pages/privacy.html", {"request": request, "title": "Privacy Policy"})

@app.get("/terms", response_class=HTMLResponse)
async def read_terms(request: Request):
    return templates.TemplateResponse("pages/terms.html", {"request": request, "title": "Terms of Service"})

@app.get("/subprocessors", response_class=HTMLResponse)
async def read_subprocessors(request: Request):
    return templates.TemplateResponse("pages/subprocessors.html", {"request": request, "title": "Subprocessors"})


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    # Example: Initialize database connection or other services
    # from backend.database.connection import DatabaseConnection
    # db_conn = DatabaseConnection()
    # db_conn.test_connection()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
