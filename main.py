import asyncio

from .ai import AIClientFactory
from .bot import AIDiscordBot
from .config import AI_API, DC_TOKEN, DSN
from .database import DatabaseFactory
from .utils import Logger


class Sena:
    def __init__(self):
        """Initialize Sena's components"""

        self.logger = Logger()
        self.logger.run()

        # Create factories
        self.db_factory = DatabaseFactory()
        self.ai_factory = AIClientFactory()

    def start(self):
        """Start entire AI bot"""

        async def run_bot():
            try:
                await self.setup()
                await self.bot.start(DC_TOKEN)
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

        try:
            # Initialize and connect to database manager
            self.db_factory.init_postgresql(DSN)
            self.db_manager = await self.db_factory.get_db_manager()

            # Initialize AI client
            self.ai_factory.init_openai(AI_API)
            self.ai_client = await self.ai_factory.get_client()

            # Initalize AI embedding generator
            self.ai_factory.init_embedding()
            self.ai_embedding = await self.ai_factory.get_embedding(self.ai_client)

            # Initialize context retriever for AI
            self.db_factory.init_ctx_retriever()
            self.context_retriever = await self.db_factory.get_ctx_retriever(
                self.db_manager, self.ai_embedding
            )

            # Initialize bot with dependencies
            self.bot = AIDiscordBot(
                ai_client=self.ai_client,
                db_manager=self.db_manager,
                embedding=self.ai_embedding,
                context_retriever=self.context_retriever,
            )
        except RuntimeError as err:
            print(f"Error: {err}")

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
    sena_ai = Sena()
    sena_ai.start()


if __name__ == "__main__":
    main()
