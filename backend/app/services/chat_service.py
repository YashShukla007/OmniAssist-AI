import time
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.domain_router import domain_router
from backend.app.services.conversation import conversation_manager
from backend.app.core.logger import logger


class ChatService:

    async def generate_response(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        logger.info(
            f"Domain={request.domain} | Prompt={request.message}"
        )

        # Store user message
        conversation_manager.add(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
            domain=request.domain,
        )

        # Generate AI response
        start = time.perf_counter()

        result = await domain_router.route(
            prompt=request.message,
            domain=request.domain,
        )

        response_time = round(
            time.perf_counter() - start,
            2,
        )

        # Store AI response
        conversation_manager.add(
            conversation_id=request.conversation_id,
            role="assistant",
            content=result["answer"],
            model=result["model"],
            provider="OpenRouter",
            response_time=response_time,
        )

        return ChatResponse(
            answer=result["answer"],
            model=result["model"],
            domain=request.domain,
            provider="OpenRouter",
            response_time=response_time,
        )


chat_service = ChatService()