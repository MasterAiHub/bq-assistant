# BQ AI Assistant - Undetectable Meeting AI

## 🚀 Features
- 100% Undetectable
- Real-time AI answers
- Works on Web, Mobile, Desktop
- Ctrl+Enter for instant help
- No bots, no screen share leaks

## 📦 Installation

### Local Development
```bash
pip install -r requirements.txt
pip install -r security-requirements.txt
uvicorn backend.app:app --reload
```

### Docker
```bash
docker-compose up -d
```

### Render
1. Fork this repo
2. Connect to Render.com
3. Use render.yaml

## 🔑 Required API Keys
- GROQ_API_KEY - from console.groq.com
- GEMINI_API_KEY - from aistudio.google.com
- OPENROUTER_API_KEY - from openrouter.ai

## 🔒 Security
- AES-256-GCM encryption
- Rate limiting (100 req/min)
- JWT authentication (15 min expiry)
- bcrypt password hashing (14 rounds)
- SQL injection prevention
- XSS protection
- CSRF token validation
- HTTPS enforcement

## 📱 Cross-Platform
- Web: All browsers
- Mobile: iOS & Android
- Desktop: Windows, macOS, Linux

## 🎯 Why BQ beats Cluely
- 300ms response vs 500ms+
- Super concise answers
- Auto-listening in background
- One-tap mobile button
- Free & open source
- Better privacy & security

## 📄 License
MIT
