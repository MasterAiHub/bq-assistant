FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt security-requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r security-requirements.txt

COPY . .

ENV PORT=8000
EXPOSE $PORT

CMD uvicorn backend.app:app --host 0.0.0.0 --port $PORT
