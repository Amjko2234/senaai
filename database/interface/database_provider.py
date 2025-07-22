from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol


class DatabaseProvider(Protocol):
    """Protocol defining the contract for database operations"""

    @property
    def is_connected(self) -> bool:
        """Check if database is connected"""
        ...

    async def connect(self) -> None:
        """Establish database connection"""
        ...

    async def save_message_pair(
        self,
        user_id: str,
        channel_id: str,
        user_message: str,
        assistant_reply: Optional[str],
        topic: str = "unspecified",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Any:
        """Save a conversation message pair"""
        ...

    async def fetch_messages(
        self,
        user_id: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch user messages with optional filters"""
        ...

    async def close(self) -> None:
        """Clean up database resources"""
        ...
