import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TranscriptionService:
    """Handles audio transcription using external APIs"""
    
    def __init__(self):
        self.assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        
    async def transcribe(self, audio_data: str) -> str:
        """Transcribes audio data to text"""
        try:
            if self.assemblyai_api_key:
                return await self._call_assemblyai(audio_data)
            elif self.deepgram_api_key:
                return await self._call_deepgram(audio_data)
            else:
                return self._fallback_transcription()
        except Exception as e:
            logger.error(f"Transcription service error: {str(e)}")
            return self._fallback_transcription()
            
    async def _call_assemblyai(self, audio_data: str) -> str:
        # This is a simplified example. Real implementation would involve
        # uploading audio and polling for results.
        logger.info("Calling AssemblyAI for transcription")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.assemblyai.com/v2/transcript",
                headers={
                    "authorization": self.assemblyai_api_key,
                    "content-type": "application/json"
                },
                json={
                    "audio_url": "https://example.com/audio.wav" # Placeholder
                }
            )
            response.raise_for_status()
            data = response.json()
            # Simulate polling for result
            return data.get("text", "Mock AssemblyAI transcript")
            
    async def _call_deepgram(self, audio_data: str) -> str:
        # This is a simplified example. Real implementation would involve
        # streaming audio or uploading and polling.
        logger.info("Calling Deepgram for transcription")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.deepgram.com/v1/listen",
                headers={
                    "Authorization": f"Token {self.deepgram_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "url": "https://example.com/audio.wav" # Placeholder
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "Mock Deepgram transcript")

    def _fallback_transcription(self) -> str:
        return "This is a mock transcript from the fallback service."
