from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:
        """
        Generate a response from the LLM.
        """
        pass