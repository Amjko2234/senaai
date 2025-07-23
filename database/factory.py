from typing import Literal, Optional

from ai.interface.embedding_provider import EmbeddingProvider
from database.interface.ctx_retriever_provider import ContextRetrieverProvider
from database.interface.database_provider import DatabaseProvider
from database.src.context_manager import ContextManager
from database.src.postgresql_manager import PostgreSQLManager


class DatabaseError(Exception):
    """Custom database error"""

    pass


class DatabaseFactory:
    """Factory for creating database providers"""

    _instance: Optional["DatabaseFactory"] = None
    _db_provider: Optional[DatabaseProvider] = None
    _ctx_provider: Optional[ContextRetrieverProvider] = None

    # Singleton pattern: one global instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_postgresql(self, dsn: str) -> None:
        """Initialize with PostgreSQL provider"""

        self._db_provider = PostgreSQLManager(dsn)

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
    ) -> ContextRetrieverProvider:
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
