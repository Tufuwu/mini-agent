import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import ModelConfig
from app.services.llm_service import LLMService


router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    config = _build_model_config(req)

    try:
        llm_service = LLMService(config)
        answer = await llm_service.chat(req.message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="LLM request failed") from exc

    return ChatResponse(answer=answer)


def _build_model_config(req: ChatRequest) -> ModelConfig:
    provider = req.provider or os.getenv("LLM_PROVIDER", "openai")
    model = req.model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    temperature = req.temperature

    if temperature is None:
        temperature = float(os.getenv("LLM_TEMPERATURE", "1.0"))

    return ModelConfig(
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=req.max_tokens or _get_env_int("LLM_MAX_TOKENS"),
    )


def _get_env_int(name: str) -> int | None:
    value = os.getenv(name)
    if value is None or value == "":
        return None
    return int(value)
