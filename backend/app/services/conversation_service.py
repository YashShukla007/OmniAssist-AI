from backend.app.services.conversation import (
    conversation_manager,
)


class ConversationService:

    def create(self):

        return conversation_manager.create()

    def get(
        self,
        conversation_id: str,
    ):

        return conversation_manager.get(
            conversation_id
        )

    def get_history(
        self,
        conversation_id: str,
    ):

        return conversation_manager.history(
            conversation_id
        )

    def get_all(self):

        return conversation_manager.all()

    def delete(
        self,
        conversation_id: str,
    ):

        conversation_manager.clear(
            conversation_id
        )


conversation_service = ConversationService()