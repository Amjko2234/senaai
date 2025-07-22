import os

from dotenv import load_dotenv

load_dotenv()
# TODO:
# DISCORD_TOKEN = os.getenv("AMJKOAI_TOKEN")
# GUILD_ID = os.getenv("GUILD_ID")
# OPENAI_API_KEY = os.getenv("no openai api key")

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

# assert isinstance(DISCORD_TOKEN, str), "no discord token"
# assert isinstance(GUILD_ID, str), "no guild id"
# assert isinstance(OPENAI_API_KEY, str), "no openai api key"
