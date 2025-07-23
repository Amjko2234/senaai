from typing import Optional

from ai.interface.ai_provider import AIProvider
from ai.src.openai_client import OpenAIClient
from database.interface.database_provider import DatabaseProvider


class AIClientFactory:

    _instance: Optional["AIClientFactory"] = None
    _ai_client: Optional[AIProvider] = None
    _db_provider: Optional[DatabaseProvider] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_openai(self, api_key: str):
        """Initialize with OpenAI provider"""

        self._ai_client = OpenAIClient(api_key)

    async def get_client(self) -> AIProvider:
        """Get the current AI client"""

        if self._ai_client is None:
            raise RuntimeError("AI Client not initialized")

        if not self._ai_client.is_initialized:
            await self._ai_client.initialize()

        return self._ai_client

    async def close(self):
        """Clean up all resources"""

        if self._ai_client:
            await self._ai_client.close()
