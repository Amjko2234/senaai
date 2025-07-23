import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = str(os.getenv("AMJKOAI_TOKEN"))
# GUILD_ID = os.getenv("GUILD_ID")
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))
DATA_SOURCE_NAME = str(os.getenv("DATA_SOURCE_NAME"))

if DISCORD_TOKEN is None:
    # TODO:
    pass
if OPENAI_API_KEY is None:
    # TODO:
    pass
