from fastapi import APIRouter

from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.conversations import (
    router as conversations_router,
)

router = APIRouter()

router.include_router(
    health_router,
    tags=["Health"],
)

router.include_router(
    chat_router,
    tags=["Chat"],
)

router.include_router(
    conversations_router,
    tags=["Conversations"],
)