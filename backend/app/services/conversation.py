from uuid import uuid4


class ConversationManager:

    def __init__(self):
        self.conversations = {}

    def create(self):

        conversation_id = str(uuid4())

        self.conversations[conversation_id] = []

        return conversation_id

    def add(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def history(
        self,
        conversation_id: str,
    ):

        return self.conversations.get(
            conversation_id,
            [],
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