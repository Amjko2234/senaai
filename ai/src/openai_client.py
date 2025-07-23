from typing import Any, Dict, List, Optional, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ai.interface.ai_provider import AIProvider
from database.database_factory import DatabaseFactory
from database.interface.database_provider import DatabaseProvider


class OpenAIClient:
    """Concrete implementation of AIProvider using OpenAI"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"
        self.embedding_model = "text-embedding-3-small"
        self.db_manager: Optional[DatabaseProvider] = None
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(self) -> None:
        db_factory = DatabaseFactory()
        self.db_manager = await db_factory.get_db_manager()
        self._initialized = True

    async def fetch_response(
        self, prompt: str, context: List[Dict[str, str]]
    ) -> Optional[str]:
        if not self._initialized:
            await self.initialize()

        full_message = [
            {
                "role": "system",
                "content": """
                    You are AmjkoAI, an AI assistant in a Discord server.
                """,
            }
        ]
        # full_message.extend(context)
        full_message.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=100,
            messages=cast(List[ChatCompletionMessageParam], full_message),
        )

        return response.choices[0].message.content

    async def generate_embedding(self, text: str) -> List[float]:
        if not self._initialized:
            await self.initialize()

        response = await self.client.embeddings.create(
            model=self.embedding_model, input=text
        )

        return response.data[0].embedding

    async def fetch_context(self, user_id: str, text: str, limit: int = 5):
        if not self._initialized:
            await self.initialize()

        current_embedding = await self.generate_embedding(text)
        async with self.db_manager.get_pool.acquire() as connection:
            similar_text = await connection.fetch(
                """
                SELECT data, (embedding <=> $1) as distance
                  FROM conversations
                 WHERE user_id = $2
                 ORDER BY distance 
                       ASC
                 LIMIT $3
                """,
                current_embedding,
                user_id,
                limit,
            )

        return similar_text

    async def close(self):
        if self.client:
            await self.client.close()
