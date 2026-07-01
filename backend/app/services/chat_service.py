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
        result = await domain_router.route(
            prompt=request.message,
            domain=request.domain,
        )

        # Store AI response
        conversation_manager.add(
            conversation_id=request.conversation_id,
            role="assistant",
            content=result["answer"],
            model=result["model"],
        )

        return ChatResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            model=result["model"],
        )


chat_service = ChatService()