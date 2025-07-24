from typing import List, Optional

from ..interface import AIProvider, EmbeddingProvider


class OpenAIEmbedding:

    def __init__(self, ai: Optional[AIProvider] = None):
        self.ai = ai
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(self, ai_client: Optional[AIProvider] = None) -> None:
        self.ai = ai_client
        if self.ai is None:
            raise ValueError("AIProvider must be provided")

        self._initialized = True

    async def generate(self, text: str, raw: bool = False) -> List[float] | str:
        if not self.is_initialized:
            await self.initialize()

        response = await self.ai.client.embeddings.create(
            model=self.ai.embedding_model, input=text
        )

        if not raw:
            return self._embedding_to_str(response.data[0].embedding)

        return response.data[0].embedding

    @staticmethod
    def _embedding_to_str(embedding: List[float]) -> str:
        return f"[{','.join(map(str, embedding))}]"
