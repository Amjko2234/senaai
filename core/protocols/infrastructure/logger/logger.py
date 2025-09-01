from typing import Protocol

from .....shared.logger.log_levels import LogLevel


class ServiceLoggerProtocol(Protocol):

    # -------------------------------------------------------------------------
    #   Public properties
    # -------------------------------------------------------------------------

    @property
    def closed(self) -> bool:
        """Check if logger is closed."""
        ...

    # -------------------------------------------------------------------------
    #   Public methods
    # -------------------------------------------------------------------------

    def debug(self, message: str, **context):
        """Log with debug level."""
        ...

    def info(self, message: str, **context):
        """Log with info level."""
        ...

    def warning(self, message: str, **context):
        """Log with warning level."""
        ...

    def error(self, message: str, **context):
        """Log with error level."""
        ...

    def critical(self, message: str, **context):
        """Log with critical level."""
        ...

    # -------------------------------------------------------------------------
    #   Helper methods
    # -------------------------------------------------------------------------

    def _log_with_context(
        self,
        level: LogLevel,
        message: str,
        **context,
    ):
        """Log with additional context data."""
        ...

    # -------------------------------------------------------------------------
    #   Close method
    # -------------------------------------------------------------------------

    def close(self):
        """Clean shutdown of this logger."""
        ...
