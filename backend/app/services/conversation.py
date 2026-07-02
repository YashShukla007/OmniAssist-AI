from uuid import uuid4
from datetime import datetime


class ConversationManager:

    def __init__(self):
        self.conversations = {}

    def create(self):

        conversation_id = str(uuid4())

        self.conversations[conversation_id] = {
            "id": conversation_id,
            "title": "New Chat",
            "domain": None,
            "model": None,
            "provider": None,
            "response_time": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "messages": [],
        }

        return conversation_id

    def add(
        self,
        conversation_id: str,
        role: str,
        content: str,
        domain: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        response_time: float | None = None,
    ):

        if conversation_id not in self.conversations:

            self.conversations[conversation_id] = {
                "id": conversation_id,
                "title": "New Chat",
                "domain": None,
                "model": None,
                "provider": None,
                "response_time": None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "messages": [],
            }

        conversation = self.conversations[conversation_id]

        conversation["messages"].append(
            {
                "role": role,
                "content": content,
            }
        )

        if (
            conversation["title"] == "New Chat"
            and role == "user"
        ):
            conversation["title"] = (
                content[:30] + "..."
                if len(content) > 30
                else content
            )

        if domain:
            conversation["domain"] = domain

        if model:
            conversation["model"] = model

        if provider:
            conversation["provider"] = provider

        if response_time is not None:
            conversation["response_time"] = response_time

        conversation["updated_at"] = datetime.utcnow().isoformat()

    def history(
        self,
        conversation_id: str,
    ):

        conversation = self.conversations.get(
            conversation_id
        )

        if not conversation:
            return []

        return conversation["messages"]

    def get(
        self,
        conversation_id: str,
    ):

        return self.conversations.get(
            conversation_id
        )

    def all(self):

        return sorted(
            self.conversations.values(),
            key=lambda x: x["updated_at"],
            reverse=True,
        )

    def clear(
        self,
        conversation_id: str,
    ):

        self.conversations.pop(
            conversation_id,
            None,
        )


conversation_manager = ConversationManager()