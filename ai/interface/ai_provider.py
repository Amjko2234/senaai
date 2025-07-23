from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol


class AIProvider(Protocol):
    """Protocol defining the contract for AI providers"""

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        ...

    async def initialize(self) -> None:
        """Initialize the AI provider"""
        ...

    async def fetch_response(
        self, prompt: str, context: List[Dict[str, str]]
    ) -> Optional[str]:
        """Fetch AI response with given prompt and context"""
        ...

    async def fetch_context(self, user_id: str, text: str, limit: int = 5):
        """Fetch relevant data or 'context' with given prompt"""
        ...

    async def generate_embedding(self, text: str) -> List[float]:
        """Generates a vector embedding from text"""
        ...

    async def close(self) -> None:
        """Clean up resources"""
        ...
