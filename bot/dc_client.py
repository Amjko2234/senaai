import discord
from discord.ext import commands

from ..ai.interface import AIProvider, EmbeddingProvider
from ..ai.src import IntentManager
from ..database.interface import CtxRetrieverProvider, DatabaseProvider


class AIDiscordBot(commands.Bot):
    """Main bot that inherits from commands.Bot"""

    def __init__(
        self,
        ai_client: AIProvider,
        db_manager: DatabaseProvider,
        embedding: EmbeddingProvider,
        context_retriever: CtxRetrieverProvider,
    ):
        """Initialize Discord bot"""

        # Privileged Discord intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self.ai_client = ai_client
        self.db_manager = db_manager
        self.embedding = embedding
        self.context_retriever = context_retriever

        # Set command prefix
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        self.intent_manager = IntentManager()
        await self.load_extension("bot.commands")

    async def on_ready(self):
        """When bot successfully connects to Discord"""

        print(f"{self.user.name} successfully connected to Discord")

    async def on_message(self, message):
        """For every message sent in channels the bot can see"""

        # Ignore messages from bots
        if message.author.bot:
            return

        # Check if message intents toward SenaAI
        if any(
            (
                # If mentioned the AI bot
                await self.intent_manager.is_intent_ai(message.content),
                # If in active conversation - lasts for 15 minutes of no activity
                self.intent_manager.is_in_converstaion(message.author.id),
            )
        ):
            # TODO:
            context = await self.context_retriever.get_conversation_context(
                user_id=str(message.author.id),
                current_message=message.content,
                channel_id=str(message.channel.id),
            )

            formatted_context = self.context_retriever.format_context_for_ai(
                current_message=message.content, context=context
            )

            # Not yet implemented below
            topic = ""
            tags = [""]

            # Get response and handle error if something went wrong with API
            response = await self.ai_client.fetch_response(
                message.content, formatted_context
            )
            if response is None:
                response = "Someone tell Amjko there's a problem with my AI"

            # Send response to discord
            await message.channel.send(f"{response}")
        else:
            response = None

        # Update that active conversation
        self.intent_manager.update_activity(message.author.id)

        # Generate embedding vector
        embedding = await self.embedding.generate(message.content, False)
        assert isinstance(embedding, str), "Embedding is raw"

        # Save the conversation pair
        await self.db_manager.save_message_pair(
            user_id=str(message.author.id),
            channel_id=str(message.channel.id),
            user_message=message.content,
            assistant_reply=response,
            topic=topic,
            tags=tags,
            embedding=embedding,
        )

        # Allow to continue handling other messages sent in server
        await self.process_commands(message)

    async def close(self):
        """Cleans then closes the connection to Discord"""

        await super().close()
