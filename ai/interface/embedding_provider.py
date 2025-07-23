from typing import List, Optional, Protocol

from ai.interface.ai_provider import AIProvider


class EmbeddingProvider(Protocol):

    @property
    def is_initialized(self) -> bool:
        """Check if AI embedding is initialized"""
        ...

    async def initialize(self, ai_client: Optional[AIProvider] = None) -> None:
        """Initialize AI embedding"""
        ...

    async def generate(self, text: str, raw: bool = False) -> List[float] | str:
        """Generate an embedding vector"""
        ...

    @staticmethod
    def _embedding_to_str(embedding: List[float]) -> str:
        """Convert embedding vector to string"""
        ...
