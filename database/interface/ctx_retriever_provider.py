from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Tuple

from ai.interface.embedding_provider import EmbeddingProvider
from database.interface.database_provider import DatabaseProvider


class ContextRetrieverProvider(Protocol):
    """Protocol defining context retriever for AI"""

    @property
    def is_initialized(self) -> bool:
        """Check if context retriever is initialized"""
        ...

    async def initialize(
        self,
        db_manager: Optional[DatabaseProvider] = None,
        embedding: Optional[EmbeddingProvider] = None,
    ) -> None:
        """Initialize the context retriever program"""
        ...

    async def get_conversation_context(
        self,
        user_id: str,
        current_message: str,
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve optimal context based on:
        - Recent messages (STM)
        - Semantically similar old messages (LTM)
        """
        ...

    async def _get_recent_context(
        self,
        user_id: str,
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get recent messages within the conversation window"""
        ...

    async def _should_retrieve_old_context(
        self,
        current_message: str,
        recent_context: List[Dict[str, Any]],
    ) -> bool:
        """Decide when to look for old context"""
        ...

    async def _get_semantic_context(
        self,
        user_id: str,
        current_message: str,
        recent_context: List[Dict[str, Any]],
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve semantically similar old messages"""
        ...

    def _merge_prioritize_context(
        self,
        current_message: str,
        recent_context: List[Dict[str, Any]],
        old_context: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Intelligently merge and prioritize context messages"""
        ...

    def _calculate_priority(
        self,
        context: Dict[str, Any],
        context_type: str,
    ) -> float:
        """Calculate priority score for context message"""
        ...

    def format_context_for_ai(
        self,
        current_message: str,
        context: List[Dict[str, Any]],
    ) -> str:
        """Format retrieved context into AI-redable format"""
        ...
