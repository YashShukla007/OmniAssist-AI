from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    domain: str


class ChatResponse(BaseModel):
    answer: str
    model: str
    domain: str
    provider: str
    response_time: float