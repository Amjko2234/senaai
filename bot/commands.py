from discord.ext import commands

from ai.interface.ai_provider import AIProvider


class Commands(commands.Cog):
    """Contains commands for the Discord bot"""

    def __init__(self, bot):
        """Load Discord bot commands"""

        self.bot = bot
        # self.ai_client = ai_client

    # !hello
    @commands.command()
    async def hello(self, context):
        await context.send(f"Hello {context.author.mention}!")

    # !ask
    # @commands.command()
    # async def ask(self, context, *, prompt: str):
    #     if not prompt:
    #         context.send(f"Please input something first")
    #     else:
    #         response = await self.ai_client.fetch_response(prompt)
    #         if response is None:
    #             response = "Someone tell Amjko there's a problem with my AI"
    #         await context.send(response)


# Entry point for loading commands extension
async def setup(bot):
    await bot.add_cog(Commands(bot))
