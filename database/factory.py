from typing import Literal, Optional

from ..ai.interface import EmbeddingProvider
from .interface import CtxRetrieverProvider, DatabaseProvider
from .src import ContextManager, DatabaseManager


class DatabaseError(Exception):
    """Custom database error"""

    pass


class DatabaseFactory:
    """Factory for creating database providers"""

    _instance: Optional["DatabaseFactory"] = None
    _db_provider: Optional[DatabaseProvider] = None
    _ctx_provider: Optional[CtxRetrieverProvider] = None

    # Singleton pattern: one global instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_postgresql(self, dsn: str) -> None:
        """Initialize with PostgreSQL provider"""

        self._db_provider = DatabaseManager(dsn)

    def init_ctx_retriever(self) -> None:
        """Initialize context retriever for AI prompts"""

        self._ctx_provider = ContextManager()

    async def get_db_manager(self) -> DatabaseProvider:
        """Get the current database provider"""

        if self._db_provider is None:
            raise RuntimeError("Database provider not initialized")

        if not self._db_provider.is_connected:
            await self._db_provider.connect()

        return self._db_provider

    async def get_ctx_retriever(
        self,
        db_manager: Optional[DatabaseProvider] = None,
        embedding: Optional[EmbeddingProvider] = None,
    ) -> CtxRetrieverProvider:
        """Get the current context retriever for ai"""

        if self._ctx_provider is None:
            raise RuntimeError("Context retriever not initialized")

        if not self._ctx_provider.is_initialized:
            await self._ctx_provider.initialize(db_manager, embedding)

        return self._ctx_provider

    async def close(self):
        """Clean up database resources"""

        if self._db_provider:
            await self._db_provider.close()
