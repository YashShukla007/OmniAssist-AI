import time

from sqlalchemy.orm import Session

from backend.app.core.logger import logger
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.conversation_service import (
    conversation_service,
)
from backend.app.services.domain_router import domain_router


class ChatService:

    async def generate_response(
        self,
        request: ChatRequest,
        current_user,
        db: Session,
    ) -> ChatResponse:

        # Do not write user prompts to logs: they may contain sensitive data.
        logger.info("Domain=%s | request_length=%s", request.domain, len(request.message))

        conversation_service.get(
            db=db,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
        )

        conversation_service.add_message(
            db=db,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
            role="user",
            content=request.message,
            domain=request.domain,
        )

        start = time.perf_counter()

        result = await domain_router.route(
            prompt=request.message,
            domain=request.domain,
        )

        response_time = round(
            time.perf_counter() - start,
            2,
        )

        conversation_service.add_message(
            db=db,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
            role="assistant",
            content=result["answer"],
            model=result["model"],
        )

        return ChatResponse(
            answer=result["answer"],
            model=result["model"],
            domain=request.domain,
            provider="OpenRouter",
            response_time=response_time,
        )


chat_service = ChatService()
