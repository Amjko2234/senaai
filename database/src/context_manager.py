import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import asyncpg
import numpy as npy

from ai.interface.embedding_provider import EmbeddingProvider
from database.interface.ctx_retriever_provider import ContextRetrieverProvider
from database.interface.database_provider import DatabaseProvider


class ContextManager:
    def __init__(
        self,
        db_manager: Optional[DatabaseProvider] = None,
        embedding: Optional[EmbeddingProvider] = None,
    ):

        # Configuration
        self.max_context_messages = 15  # Total context limit
        self.recent_window_minutes = 15  # Recent conversation window
        self.similarity_threshold = 0.3  # Minimum similarity for old msgs
        self.max_old_messages = 5  # Maximum old context msgs
        self._initialized = False  # Prevent accessing methods without initialization

        self.db_manager = db_manager
        self.embedding = embedding

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(
        self,
        db_manager: Optional[DatabaseProvider] = None,
        embedding: Optional[EmbeddingProvider] = None,
    ) -> None:

        self.db_manager = db_manager
        self.embedding = embedding

        if self.db_manager is None:
            raise ValueError("DatabaseProvider must be provided")
        if self.embedding is None:
            raise ValueError("EmbeddingProvider must be provied")

        self._initialized = True

    async def get_conversation_context(
        self,
        user_id: str,
        current_message: str,
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        # Get recent conversation context
        recent_context = await self._get_recent_context(
            user_id=user_id, channel_id=channel_id
        )

        # Decide the need for old context
        need_old_context = await self._should_retrieve_old_context(
            current_message=current_message, recent_context=recent_context
        )

        old_context = []
        if need_old_context:
            # Get semantically relevant old messages
            old_context = await self._get_semantic_context(
                user_id=user_id,
                current_message=current_message,
                recent_context=recent_context,
                channel_id=channel_id,
            )

        # Combine and prioritize context
        final_context = self._merge_prioritize_context(
            current_message=current_message,
            recent_context=recent_context,
            old_context=old_context,
        )

        return final_context

    async def _get_recent_context(
        self,
        user_id: str,
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        # Only query for data created within specified time
        cutoff_time = datetime.now(timezone.utc) - timedelta(
            minutes=self.recent_window_minutes
        )

        query = """
            SELECT data, created_at, embedding
              FROM conversations
             WHERE user_id = $1
               AND created_at >= $2
        """
        params = [user_id, cutoff_time]

        # Avoid unnecessary selecting of irrelavant data origin
        if channel_id:
            query += " AND channel_id = $3"
            params.append(channel_id)

        # Chronological order
        query += " ORDER BY created_at ASC LIMIT 10"

        # Query
        async with self.db_manager.get_pool.acquire() as connection:
            rows = await connection.fetch(query, *params)

        return [
            {
                "messages": json.loads(row["data"])["messages"],
                "timestamp": row["created_at"],
                "embedding": row["embedding"],
                "type": "recent",
            }
            for row in rows
        ]

    async def _should_retrieve_old_context(
        self,
        current_message: str,
        recent_context: List[Dict[str, Any]],
    ) -> bool:

        # Trigger conditions for old context retrieval
        triggers = [
            # User asks about past events
            any(
                word in current_message.lower()
                for word in [
                    "remember",
                    "earlier",
                    "before",
                    "previously",
                    "last time",
                    "you said",
                    "we talked",
                    "mentioned",
                ]
            ),
            # Question without recent context
            current_message.strip().endswith("?") and len(recent_context) < 3,
            # Reference pronouns (it, that, this) without clear antecedent
            any(
                word in current_message.lower().split()
                for word in ["it", "that", "this", "them", "those"]
            )
            and len(recent_context) < 2,
            # Continuation words
            any(
                current_message.lower().startswith(word)
                for word in ["also", "additionally", "furthermore", "besides"]
            ),
        ]

        return any(triggers)

    async def _get_semantic_context(
        self,
        user_id: str,
        current_message: str,
        recent_context: List[Dict[str, Any]],
        channel_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        # Embedding of current message to compare to other embedded vectors
        current_embedding = await self.embedding.generate(current_message)

        # Exclude recent messages
        recent_cutoff = datetime.now(timezone.utc) - timedelta(
            minutes=self.recent_window_minutes
        )

        # Search for similar old messages
        query = """
            SELECT data, created_at, embedding,
                   (embedding <=> $1) as similarity_distance
              FROM conversations 
             WHERE user_id = $2 
               AND created_at < $3
        """
        params = [current_embedding, user_id, recent_cutoff]

        # Avoid unnecessary selecting of irrelavant data origin
        if channel_id:
            query += " AND channel_id = $4"
            params.append(channel_id)

        limit_param_num = len(params) + 1
        query += f"""
            ORDER BY similarity_distance ASC 
            LIMIT ${limit_param_num}::BIGINT
        """  # Either $4 or $5 depending if channel_id was specified
        params.append(self.max_old_messages * 2)  # Get extra for filtering

        async with self.db_manager.get_pool.acquire() as connection:
            rows = await connection.fetch(query, *params)

        # Filter by similarity threshold and relevance
        old_context = []
        for row in rows:
            similarity_distance = float(row["similarity_distance"] or 50)

            # Convert distance to similarity (lower distance = higher similarity)
            similarity_score = 1 - similarity_distance

            if similarity_score >= self.similarity_threshold:
                old_context.append(
                    {
                        "messages": json.loads(row["data"])["messages"],
                        "timestamp": row["created_at"],
                        "similarity_score": similarity_score,
                        "type": "semantic",
                    }
                )

            if len(old_context) >= self.max_old_messages:
                break

        return old_context

    def _merge_prioritize_context(
        self,
        current_message: str,
        recent_context: List[Dict[str, Any]],
        old_context: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        # Priority system:
        # 1. Most recent messages (always included)
        # 2. Highly relevant old messages
        # 3. Fill remaining slots with recent messages

        all_context = []

        # Add recent context (chronologically ordered)
        for context in recent_context:
            context["priority"] = self._calculate_priority(context, "recent")
            all_context.append(context)

        # Add old context (similarity ordered)
        for context in old_context:
            context["priority"] = self._calculate_priority(context, "semantic")
            all_context.append(context)

        # Sort by priority (higher = more important)
        all_context.sort(key=lambda x: x["priority"], reverse=True)

        # Take top messages within limit
        final_context = all_context[: self.max_context_messages]

        # Re-sort final context chronologically for coherent flow
        final_context.sort(key=lambda x: x["timestamp"])

        return final_context

    def _calculate_priority(
        self,
        context: Dict[str, Any],
        context_type: str,
    ) -> float:

        base_priority = 0.0

        if context_type == "recent":
            # Recent messages get higher base priority
            base_priority = 1.0

            # Boost very recent messages
            time_diff = datetime.now(timezone.utc) - context["timestamp"]
            if time_diff.total_seconds() < 300:  # 5 minutes
                base_priority += 0.5

        elif context_type == "semantic":
            # Old messages based on similarity
            base_priority = context.get("similarity_score", 0.0)

            # Boost if very high similarity
            if context.get("similarity_score", 0) > 0.8:
                base_priority += 0.3

        # Additional boosts based on message content
        messages = context.get("messages", [])
        for msg in messages:
            content = msg.get("content", "").lower()

            # Important keywords boost
            if any(
                word in content for word in ["important", "remember", "don't forget"]
            ):
                base_priority += 0.2

            # Question-answer pairs are valuable
            if msg.get("role") == "user" and content.endswith("?"):
                base_priority += 0.1

        return base_priority

    def format_context_for_ai(
        self,
        current_message: str,
        context: List[Dict[str, Any]],
    ) -> str:

        if not context:
            return ""

        formatted_parts = ["Previous conversation context:\n"]

        for ctx in context:
            timestamp = ctx["timestamp"].strftime("%H:%M")
            ctx_type = ctx.get("type", "unknown")

            # Add context marker
            if ctx_type == "recent":
                marker = f"[Recent - {timestamp}]"
            else:
                similarity = ctx.get("similarity_score", 0)
                marker = f"[Relevant - {timestamp}, similarity: {similarity:.2f}]"

            formatted_parts.append(f"\n{marker}")

            # Add messages from this context
            for msg in ctx["messages"]:
                role = msg["role"].capitalize()
                content = msg["content"]
                formatted_parts.append(f"{role}: {content}")

        formatted_parts.append(f"\n\nCurrent message: {current_message}")

        return "\n".join(formatted_parts)
