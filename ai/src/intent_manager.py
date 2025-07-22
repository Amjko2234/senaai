from typing import Optional


class IntentManager:
    _instance: Optional["IntentManager"] = None

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
        return cls._instance

    async def is_intent_ai(self, message: str) -> bool:
        for name in self.ai_names:
            if name.lower() in message.lower().strip():
                return True
        return False
