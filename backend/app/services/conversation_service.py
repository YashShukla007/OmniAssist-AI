from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.conversation import Conversation
from backend.app.models.message import Message


class ConversationService:

    def create(
        self,
        user_id: int,
    ) -> int:

        db: Session = SessionLocal()

        try:
            conversation = Conversation(
                user_id=user_id,
                title="New Chat",
            )

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            return conversation.id

        finally:
            db.close()

    def get(
        self,
        conversation_id: int,
        user_id: int,
    ):

        db: Session = SessionLocal()

        try:
            return (
                db.query(Conversation)
                .filter(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
                .first()
            )

        finally:
            db.close()

    def get_all(
        self,
        user_id: int,
    ):

        db: Session = SessionLocal()

        try:
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

        finally:
            db.close()

    def delete(
        self,
        conversation_id: int,
        user_id: int,
    ):

        db: Session = SessionLocal()

        try:
            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
                .first()
            )

            if conversation:
                db.delete(conversation)
                db.commit()

        finally:
            db.close()

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ):

        db: Session = SessionLocal()

        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
            )

            db.add(message)

            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id == conversation_id,
                )
                .first()
            )

            if conversation:

                if (
                    conversation.title == "New Chat"
                    and role == "user"
                ):
                    conversation.title = (
                        content[:30] + "..."
                        if len(content) > 30
                        else content
                    )

            db.commit()

        finally:
            db.close()


conversation_service = ConversationService()