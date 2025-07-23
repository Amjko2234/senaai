from typing import Optional

from ai.interface.ai_provider import AIProvider
from ai.interface.embedding_provider import EmbeddingProvider
from ai.src.openai_client import OpenAIClient
from ai.src.openai_embedding import OpenAIEmbedding
from database.interface.database_provider import DatabaseProvider


class AIClientFactory:

    _instance: Optional["AIClientFactory"] = None
    _ai_client: Optional[AIProvider] = None
    _embedding_generator: Optional[EmbeddingProvider] = None
    _db_provider: Optional[DatabaseProvider] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_openai(self, api_key: str):
        """Initialize with OpenAI provider"""

        self._ai_client = OpenAIClient(api_key)

    def init_embedding(self):
        """Initialize OpenAI embedding generator"""

        # if self._ai_client.is_initialized:
        self._embedding_generator = OpenAIEmbedding()

    async def get_client(
        self, db_manager: Optional[DatabaseProvider] = None
    ) -> AIProvider:
        """Get the current AI client"""

        if self._ai_client is None:
            raise RuntimeError("AI Client not initialized")

        if not self._ai_client.is_initialized:
            await self._ai_client.initialize(db_manager)

        return self._ai_client

    async def get_embedding(
        self, ai_client: Optional[AIProvider] = None
    ) -> EmbeddingProvider:
        """Get the current AI embedding"""

        if self._embedding_generator is None:
            raise RuntimeError("AI embedding not initialized")

        if not self._embedding_generator.is_initialized:
            await self._embedding_generator.initialize(ai_client)

        return self._embedding_generator

    async def close(self):
        """Clean up all resources"""

        if self._ai_client:
            await self._ai_client.close()
