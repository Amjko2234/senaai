from typing import Any, Dict, List, Optional, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ai.interface.ai_provider import AIProvider
from ai.interface.embedding_provider import EmbeddingProvider
from database.interface.database_provider import DatabaseProvider


class OpenAIClient:
    """Concrete implementation of AIProvider using OpenAI"""

    def __init__(self, api_key: str, db_manager: Optional[DatabaseProvider] = None):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = "gpt-4.1-mini"
        self._embedding_model = "text-embedding-3-small"

        self.db_manager = db_manager

        self._initialized = False

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    @property
    def model(self) -> str:
        return self._model

    @property
    def embedding_model(self) -> str:
        return self._embedding_model

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(self, db_manager: Optional[DatabaseProvider] = None) -> None:
        self.db_manager = db_manager

        if self.db_manager is None:
            raise ValueError("DatabaseProvider must be provided")

        self._initialized = True

    async def fetch_response(self, prompt: str, context: str = "") -> Optional[str]:
        if not self.is_initialized:
            await self.initialize()

        system_prompt = """
            You are AmjkoAI, an AI assistant in a Discord server.
            Don't be too friendly, be like the usual friend.
        """

        if context:
            system_prompt += f"\n\n{context}"

        full_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            messages=cast(List[ChatCompletionMessageParam], full_message),
            store=True,
        )

        return response.choices[0].message.content

    async def close(self):
        if self.client:
            await self.client.close()
