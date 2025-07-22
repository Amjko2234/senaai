from typing import Any, Dict, List, Optional, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ai.interface.ai_provider import AIProvider
from database.interface.database_provider import DatabaseProvider


class OpenAIClient:
    """Concrete implementation of AIProvider using OpenAI"""

    def __init__(self, api_key: str, db_provider: Optional[DatabaseProvider]):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"
        self.db_provider = db_provider
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(self) -> None:
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

    async def close(self):
        if self.client:
            await self.client.close()
