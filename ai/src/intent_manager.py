import time
from typing import Dict, Optional


class IntentManager:

    _instance: Optional["IntentManager"] = None
    _active_sessions: Optional[Dict[str, float]] = None

    def __init__(self):
        self.ai_names = [
            "openai",
            "open_ai",
            "open ai",
            "amjkoai",
            "amjko_ai",
            "amjko ai",
            "ai",
        ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        if cls._active_sessions is None:
            cls._active_sessions = {}

        return cls._instance

    async def is_intent_ai(self, message: str) -> bool:
        for name in self.ai_names:
            if name.lower() in message.lower().strip():
                return True
        return False

    @classmethod
    def is_in_converstaion(cls, user_id: str) -> bool:
        last_activity = cls._active_sessions.get(user_id, 0)

        # User is not in conversation
        if last_activity == 0 or (time.time() - last_activity) > 900:
            return False

        return True

    @classmethod
    def update_activity(cls, user_id: str) -> None:
        cls._active_sessions[user_id] = time.time()
