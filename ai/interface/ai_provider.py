from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol

from openai import AsyncOpenAI

from database.interface.database_provider import DatabaseProvider


class AIProvider(Protocol):
    """Protocol defining the contract for AI providers"""

    @property
    def client(self) -> AsyncOpenAI:
        """Get the existing AI client instance"""
        ...

    @property
    def model(self) -> str:
        """Get the model of the current AI client"""
        ...

    @property
    def embedding_model(self) -> str:
        """Get the model of the current AI embedding"""
        ...

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        ...

    async def initialize(self, db_manager: Optional[DatabaseProvider] = None) -> None:
        """Initialize the AI provider"""
        ...

    async def fetch_response(self, prompt: str, context: str = "") -> Optional[str]:
        """Fetch AI response with given prompt and context"""
        ...

    async def close(self) -> None:
        """Clean up resources"""
        ...
