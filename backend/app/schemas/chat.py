from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    domain: str


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    model: str