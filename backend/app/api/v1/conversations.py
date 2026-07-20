from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_user
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.services.conversation_service import (
    conversation_service,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/")
async def create_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation_id = conversation_service.create(
        db=db,
        user_id=current_user.id,
    )

    return {
        "conversation_id": conversation_id,
    }


@router.get("/")
async def get_all_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return conversation_service.get_all(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return conversation_service.get(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation_service.delete(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    return {
        "status": "deleted",
    }