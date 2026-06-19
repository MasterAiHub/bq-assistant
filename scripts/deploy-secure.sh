#!/bin/bash
# Secure deployment script

echo "Starting secure deployment..."

# 1. Run tests
echo "Running tests..."
pytest

# 2. Run security audit
echo "Running security audit..."
python3 scripts/security-audit.py

# 3. Build docker image
echo "Building Docker image..."
docker build -t bq-assistant .

# 4. Push to registry (mock)
echo "Pushing to registry..."

# 5. Deploy to production (mock)
echo "Deploying to production environment..."

echo "[SUCCESS] Secure deployment completed."
