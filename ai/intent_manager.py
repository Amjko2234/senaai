# from ai.openai_client import client as ai_client


class IntentManager:
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
        pass

    async def is_intent_ai(self, message: str) -> bool:
        for name in self.ai_names:
            if name.lower() in message.lower().strip():
                return True
        return False


_intent_manager: IntentManager | None = None


def init() -> None:
    global _intent_manager
    if _intent_manager is None:
        _intent_manager = IntentManager()

    return


def get_manager() -> IntentManager:
    if _intent_manager is None:
        raise RuntimeError("AI Intent Manager not initialized")
    return _intent_manager
