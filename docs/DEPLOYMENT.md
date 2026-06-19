# Deployment Guide

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- API Keys (Groq, Gemini, OpenRouter)

## Local Deployment

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r security-requirements.txt
   ```
3. Set up environment variables in a `.env` file.
4. Run the application:
   ```bash
   uvicorn backend.app:app --reload
   ```

## Docker Deployment

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

## Render Deployment

1. Fork the repository to GitHub.
2. Connect your GitHub account to Render.
3. Create a new "Web Service" and select the repository.
4. Render will automatically detect the `render.yaml` file.
5. Add your environment variables in the Render dashboard.
