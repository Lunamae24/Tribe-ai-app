"""AI endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

from app.core.config import settings
from app.services.ai_service import AIService

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    model: str
    tokens_used: int


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with AI model"""
    try:
        ai_service = AIService()
        
        model = request.model or settings.DEFAULT_MODEL
        temperature = request.temperature or settings.TEMPERATURE
        max_tokens = request.max_tokens or settings.MAX_TOKENS
        
        response = await ai_service.generate_response(
            message=request.message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return ChatResponse(
            response=response["text"],
            model=model,
            tokens_used=response.get("tokens_used", 0)
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available AI models"""
    return {
        "models": [
            "gpt-4",
            "gpt-3.5-turbo",
            "claude-3-opus",
            "claude-3-sonnet"
        ]
    }
