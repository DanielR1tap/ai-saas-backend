from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AiCompletionRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    system: str | None = Field(default=None, max_length=2000)
    estimated_credits: int = Field(default=1, ge=1, le=100)


class AiCompletionResponse(BaseModel):
    request_id: int
    text: str
    provider: str
    model: str
    used_credits: int


class AiRequestRead(BaseModel):
    id: int
    prompt: str
    system: str | None
    response_text: str
    provider: str
    ai_model: str
    credits: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
