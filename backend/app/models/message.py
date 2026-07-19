from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    role: Mapped[str] = mapped_column()

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id")
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )