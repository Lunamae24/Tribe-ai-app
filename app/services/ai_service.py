"""AI service for handling AI model interactions"""

import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI model interactions"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def generate_response(
        self,
        message: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Generate AI response"""
        
        try:
            if model.startswith("gpt"):
                return await self._openai_response(message, model, temperature, max_tokens)
            elif model.startswith("claude"):
                return await self._anthropic_response(message, model, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as e:
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            raise
    
    async def _openai_response(
        self,
        message: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate OpenAI response"""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "text": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens
        }
    
    async def _anthropic_response(
        self,
        message: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Generate Anthropic response"""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
        
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": message}]
        )
        
        return {
            "text": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens
        }
