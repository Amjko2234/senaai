from typing import Any, Dict, List, Optional, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ai.interface.ai_provider import AIProvider


class OpenAIClient:
    """Concrete implementation of AIProvider using OpenAI"""

    def __init__(self, api_key: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = "gpt-4.1-mini"
        self._embedding_model = "text-embedding-3-small"

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

    async def initialize(self) -> None:
        self._initialized = True

    async def fetch_response(self, prompt: str, context: str = "") -> Optional[str]:
        if not self.is_initialized:
            await self.initialize()

        system_prompt = """
            You are Sena, an AI assistant in a Discord server.
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
