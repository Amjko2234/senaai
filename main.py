import asyncio

from ai.client_factory import AIClientFactory
from bot.dc_client import AIDiscordBot
from config.settings import DATA_SOURCE_NAME, DISCORD_TOKEN, OPENAI_API_KEY
from database.database_factory import DatabaseFactory
from utils.logger import Logger


class AmjkoAI:
    def __init__(self):
        """Initialize AmjkoAI components"""

        self.logger = Logger()
        self.logger.run()

        # Create factories
        self.db_factory = DatabaseFactory()
        self.ai_factory = AIClientFactory()

        #
        self.ai_client = None
        self.db_manager = None
        self.bot = None

    def start(self):
        """Start entire AI bot"""

        async def run_bot():
            try:
                await self.setup()
                await self.bot.start(DISCORD_TOKEN)
            finally:
                await self.close()

        try:
            asyncio.run(run_bot())
        except KeyboardInterrupt:
            pass
        except Exception as err:
            print(f"\nBot crashes: {err}")

    async def setup(self):
        """Async setup method for all components"""

        # Initialize and connect to database manager
        self.db_factory.init_postgresql(DATA_SOURCE_NAME)
        self.db_manager = await self.db_factory.get_db_manager()

        # Initialize AI client
        self.ai_factory.init_openai(OPENAI_API_KEY)
        self.ai_client = await self.ai_factory.get_client()

        # Initialize bot with dependencies
        self.bot = AIDiscordBot(ai_client=self.ai_client, db_manager=self.db_manager)

    async def cleanup(self):
        """Cleanup handler before closing"""

        print(f"\nBot shutting down...")

        # Safely close running components
        if hasattr(self, "ai_client") and self.ai_client:
            await self.ai_client.close()
        if hasattr(self, "db_manager") and self.db_manager:
            await self.db_manager.close()

    async def close(self):
        """Close program altogether"""

        await self.cleanup()
        if hasattr(self, "bot") and self.bot:
            await self.bot.close()


def main():
    amjko_ai = AmjkoAI()
    amjko_ai.start()


if __name__ == "__main__":
    main()
