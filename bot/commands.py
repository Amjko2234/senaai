import discord
from discord.ext import commands

from ai.openai_client import client as ai_client


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, context):
        await context.send(f"Hello {context.author.mention}!")

    @commands.command()
    async def ask(self, context, *, prompt: str):
        if not prompt:
            context.send(f"Please input something first")
        else:
            response = await ai_client.ask(prompt)
            if response is None:
                response = "Someone tell Amjko there's a problem with my AI"
            await context.send(response)


# Entry point for loading commands extension
async def setup(bot):
    await bot.add_cog(Commands(bot))
