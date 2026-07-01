from fastapi import APIRouter

from backend.app.services.conversation_service import (
    conversation_service,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/")
async def create_conversation():

    conversation_id = conversation_service.create()

    return {
        "conversation_id": conversation_id,
    }


@router.get("/")
async def get_all_conversations():

    return conversation_service.get_all()


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
):

    conversation = conversation_service.get(
        conversation_id,
    )

    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
):

    conversation_service.delete(
        conversation_id,
    )

    return {
        "status": "deleted",
    }