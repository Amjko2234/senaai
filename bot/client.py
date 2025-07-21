import discord
from discord.ext import commands


class AIDiscordBot(commands.Bot):
    """Main bot that inherits from commands.Bot"""

    def __init__(self):
        """Initialize discord bot"""
        # Privileged discord intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        # Set prefix
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def on_ready(self):
        """Called when bot successfully connects to Discord"""
        print(f"{self.user.name} successfully connected to Discord")

    async def on_message(self, message):
        """Called for every message sent in channels bot can see"""
        # Ignore messages from bots
        if message.author.bot:
            return
        # Allow to continue handling other messages sent in server
        await self.process_commands(message)

    async def setup_hook(self):
        """Load extension of commands"""
        await self.load_extension("bot.commands")

    async def cleanup(self):
        """Other executions to do before closing"""
        print(f"\nBot shutting down...")

    async def close(self):
        await self.cleanup()
        await super().close()
