import asyncio
import logging

import discord

from ai.intent_manager import init as init_intent_manager
from ai.openai_client import init as init_openai
from bot.client import AIDiscordBot
from config.settings import DISCORD_TOKEN, OPENAI_API_KEY
from utils.logger import HANDLER, HANDLER_LEVEL


class AmjkoAI:
    def __init__(self):
        # TODO:
        # Initialize Discord bot
        self.bot = AIDiscordBot()
        # Initialize database manager

        # Initialize AI client
        init_openai(OPENAI_API_KEY)
        init_intent_manager()
        # Initialize message handler

        # Initialize consent manager

    async def setup(self):
        # TODO:
        # Create database tables
        # Test OpenAI connection
        # Set up Discord event handlers
        # Set up Discord commands
        await self.bot.setup_hook()

    async def close_bot(self):
        # TODO:
        pass

    async def cleanup(self):
        # TODO:
        pass

    async def close(self):
        """Cleanup handler before closing"""
        # Cleanup for other files aside from bot
        await self.cleanup()
        # Execute cleanup for the Discord bot
        await self.bot.close()


def main():
    ai = AmjkoAI()
    ai.bot.run(token=DISCORD_TOKEN, log_handler=HANDLER, log_level=HANDLER_LEVEL)


if __name__ == "__main__":
    main()
