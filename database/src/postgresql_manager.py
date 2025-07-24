import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import asyncpg

from ..interface import DatabaseProvider


class PostgreSQLManager:
    """PostgreSQL implementation of DatabaseProvider"""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    @property
    def is_connected(self) -> bool:
        try:
            if self.pool:
                self.pool._queue.qsize()
                return True
            return False
        except AttributeError:
            return False

    @property
    def get_pool(self) -> Optional[asyncpg.Pool]:
        return self.pool

    async def connect(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def save_message_pair(
        self,
        user_id: str,
        channel_id: str,
        user_message: str,  # Part of data
        assistant_reply: Optional[str],  # Part of data
        topic: str = "unspecified",  # Part of data
        tags: Optional[List[str]] = None,  # Part of data
        metadata: Optional[Dict] = None,  # Part of data
        embedding: str = "",
    ) -> Any:
        # TODO:
        if not self.is_connected:
            await self.connect()

        try:
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                        "timestamp": datetime.now().isoformat(),
                    },
                ],
                "message_count": 1,
                "topic": topic,
                "tags": tags or [],
                "source": f"discord_channel:{channel_id}",
                "context_id": str(uuid4()),
                "metadata": metadata or {},
            }

            if assistant_reply:
                payload["messages"].append(
                    {
                        "role": "assistant",
                        "content": assistant_reply,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                payload["message_count"] = 2

            async with self.pool.acquire() as connection:
                result = await connection.fetchval(
                    """
                    INSERT INTO conversations (user_id, channel_id, data, created_at, embedding)
                    VALUES ($1, $2, $3, NOW(), $4)
                    RETURNING id
                """,
                    user_id,
                    channel_id,
                    json.dumps(payload),
                    embedding,
                )

            return result

        except Exception as err:
            # TODO:
            # raise DatabaseError(f"Failed to saved message pair: {str(err)}") from err
            raise RuntimeError(f"Failed to save message pair: {str(err)}")

    async def fetch_messages(
        self,
        user_id: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        if not self.is_connected:
            await self.connect()

        query_parts: List[str] = [
            "SELECT data->'messages' AS messages",
            "FROM conversations",
            "WHERE user_id = $1",
        ]

        args = []
        args.append(user_id)

        if since:
            query_parts.append(f"AND created_at >= ${len(args) + 1}")
            args.append(since)

        if until:
            query_parts.append(f" AND created_at <= ${len(args) + 1}")
            args.append(until)

        query_parts.append("ORDER BY created_at DESC")

        if limit:
            query_parts.append(f"LIMIT ${len(args) + 1}")
            args.append(limit)

        query = " ".join(query_parts)

        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, *args)

        messages = []
        for row in rows:
            messages.extend(row["messages"])

        return messages

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
