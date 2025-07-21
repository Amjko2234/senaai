import logging

# Logger
HANDLER = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")

# For detailed logs
HANDLER_LEVEL = logging.DEBUG
