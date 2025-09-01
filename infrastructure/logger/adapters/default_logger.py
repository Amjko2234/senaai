import logging
from collections.abc import Callable
from typing import Any, List, Optional

from ....core.exceptions.error_codes import ErrorCode
from ....core.protocols.infrastructure.logger import ServiceLoggerProtocol
from ....shared.logger.log_levels import LogLevel
from ...exceptions import MissingValueError


class _ServiceLogger:
    """Logger instance for a specific service."""

    def __init__(
        self,
        name: str,
        console_handler: Optional[logging.Handler] = None,
        file_handler: Optional[logging.Handler] = None,
        on_close_callback: Optional[Callable] = None,
    ):

        if (not console_handler) and (not file_handler):
            raise MissingValueError(
                message="The logger does not have file and/or console handler",
                err_code=ErrorCode.INF_CFGB_LOOK_524,
            )

        self.name = name
        self.logger = logging.getLogger(f"sena.{name}")
        self.logger.setLevel(logging.DEBUG)
        self.handlers: List[Any] = [console_handler, file_handler]
        self._closed: bool = False
        self.on_close_callback = on_close_callback

        if console_handler:
            self.logger.addHandler(console_handler)
        if file_handler:
            self.logger.addHandler(file_handler)

        # Test
        # print(self.logger.getEffectiveLevel())

    # -------------------------------------------------------------------------
    #   Public properties
    # -------------------------------------------------------------------------

    @property
    def closed(self) -> bool:
        return self._closed

    # -------------------------------------------------------------------------
    #   Logger methods
    #   Use this for emitting logs
    # -------------------------------------------------------------------------

    def debug(self, message: str, **context):
        self._log_with_context(
            level=LogLevel.DEBUG,
            message=message,
            **context,
        )

    def info(self, message: str, **context):
        self._log_with_context(
            level=LogLevel.INFO,
            message=message,
            **context,
        )

    def warning(self, message: str, **context):
        self._log_with_context(
            level=LogLevel.WARNING,
            message=message,
            **context,
        )

    def error(self, message: str, **context):
        self._log_with_context(
            level=LogLevel.ERROR,
            message=message,
            **context,
        )

    def critical(self, message: str, **context):
        self._log_with_context(
            level=LogLevel.CRITICAL,
            message=message,
            **context,
        )

    def _log_with_context(
        self,
        level: LogLevel,
        message: str,
        **context,
    ):
        if self._closed:
            return

        extra = context if context else {}
        self.logger.log(
            level=level.to_value(),
            msg=message,
            extra=extra,
            # Refer to the calling functions
            # 1 is default (itself), incrementing 1 refers to a level above
            stacklevel=3,
        )

    # -------------------------------------------------------------------------
    #   Close method
    # -------------------------------------------------------------------------

    def close(self):
        if self._closed:
            return

        for handler in self.handlers:
            self.logger.removeHandler(handler)
            handler.close()

        self.handlers.clear()
        self._closed = True

        # Notify factory that this service logger is closing
        if self.on_close_callback:
            self.on_close_callback(self.name)

    # -------------------------------------------------------------------------
    #   Entry a runtime context
    # -------------------------------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
