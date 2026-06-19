import os
import httpx
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AIService:
    """AI Service that gives super concise, direct answers - perfect for interviews"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
    async def get_direct_answer(self, question: str, context: str = "") -> str:
        """Get extremely concise, direct answer - no fluff"""
        
        system_prompt = """You are BQ, an undetectable AI assistant for live interviews.
        
        CRITICAL RULES:
        1. Give SHORT, DIRECT answers (max 2-3 sentences)
        2. NO fluff, NO introductions, NO explanations
        3. Get straight to the point
        4. Sound natural and conversational
        5. NEVER say "as an AI" or "I don't have personal experience"
        6. Be confident and authoritative
        7. Directly answer the question - no preamble
        
        Now answer the question directly:"""
        
        full_prompt = f"{system_prompt}\n\nQuestion: {question}\n\nContext: {context}\n\nAnswer:"
        
        try:
            if self.groq_api_key:
                return await self._call_groq(full_prompt)
            elif self.gemini_api_key:
                return await self._call_gemini(full_prompt)
            elif self.openrouter_api_key:
                return await self._call_openrouter(full_prompt)
            else:
                return self._fallback_response(question)
        except Exception as e:
            logger.error(f"AI service error: {str(e)}")
            return self._fallback_response(question)
    
    async def _call_groq(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 100,
                    "top_p": 0.9
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"Groq API error: {response.status_code}")
    
    async def _call_gemini(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 100,
                        "topP": 0.9
                    }
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                raise Exception(f"Gemini API error: {response.status_code}")
    
    async def _call_openrouter(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3-8b-instruct",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 100
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"OpenRouter API error: {response.status_code}")
    
    def _fallback_response(self, question: str) -> str:
        fallbacks = {
            "experience": "I have 5+ years of experience leading technical teams.",
            "prioritize": "I prioritize by impact and urgency, then communicate clearly.",
            "handled": "I take ownership, communicate transparently, and find solutions.",
            "technical": "I break problems down and deliver clean, scalable solutions."
        }
        for key, response in fallbacks.items():
            if key in question.lower():
                return response
        return "I focus on understanding the core problem, then deliver a clear solution."
