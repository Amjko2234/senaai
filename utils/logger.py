import logging
import sys
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None

    def __init__(self):
        self.handler = logging.FileHandler(
            filename="logs/discord.log", encoding="utf-8", mode="w"
        )
        self.handler_level = logging.DEBUG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def run(self):
        logging.basicConfig(
            level=self.handler_level,
            handlers=[self.handler],
            format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        )

        # Custom uncaught exception catcher
        def handle_exception(except_type, except_value, except_traceback):
            if issubclass(except_type, KeyboardInterrupt):
                sys.__excepthook__(except_type, except_value, except_traceback)
                return
            logging.critical(
                "Uncaught exception",
                exc_info=(except_type, except_value, except_traceback),
            )

        # Override the catcher with custom catcher
        sys.excepthook = handle_exception
