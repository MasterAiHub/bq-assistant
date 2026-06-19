# API Documentation

## Authentication

All API requests except for `/api/auth/login` and `/api/health` require a Bearer token in the `Authorization` header.

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns the status of the API.

### AI Assistance
- **POST** `/api/ai/assist`
- Body: `{ "question": "string", "context": "string" }`
- Returns AI-generated response.

### Transcription
- **POST** `/api/transcribe`
- Body: `{ "audio": "base64_string" }`
- Returns transcript of the audio.

### Authentication
- **POST** `/api/auth/login`
- Body: `{ "email": "string", "password": "string" }`
- Returns access and refresh tokens.

### Meetings
- **POST** `/api/meetings` - Create a meeting.
- **GET** `/api/meetings/{id}` - Get meeting details.

### Users
- **GET** `/api/users/me` - Get current user profile.
- **POST** `/api/users/register` - Register a new user.

### Billing
- **POST** `/api/billing/subscribe` - Subscribe to a plan.
