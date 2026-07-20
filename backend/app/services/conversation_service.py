from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.models.conversation import Conversation
from backend.app.models.message import Message


class ConversationService:

    def create(
        self,
        db: Session,
        user_id: int,
    ) -> int:

        conversation = Conversation(
            user_id=user_id,
            title="New Chat",
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation.id

    def get(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
    ):

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        return conversation

    def get_all(
        self,
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
            )
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    def delete(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
    ):

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        db.delete(conversation)
        db.commit()

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
        role: str,
        content: str,
        domain: str | None = None,
        model: str | None = None,
    ):

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)

        if (
            conversation.title == "New Chat"
            and role == "user"
        ):
            conversation.title = (
                content[:30] + "..."
                if len(content) > 30
                else content
            )

        if domain is not None:
            conversation.domain = domain

        if model is not None:
            conversation.model = model

        db.commit()


conversation_service = ConversationService()