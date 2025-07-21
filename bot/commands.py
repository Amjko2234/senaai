import discord
from ai.openai_client import client
from discord.ext import commands


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
            response = await client.ask(prompt)
            if response is None:
                response = "Someone tell Amjko there's a problem with my AI"
            await context.send(response)


# Entry point for loading commands extension
async def setup(bot):
    await bot.add_cog(Commands(bot))
