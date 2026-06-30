from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    domain: str


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    model: str