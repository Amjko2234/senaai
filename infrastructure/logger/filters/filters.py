import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from logging import LogRecord
from typing import TypeAlias


class BaseLogFilter(ABC):
    """Base class for all log filters."""

    @abstractmethod
    def __call__(self, record: LogRecord) -> bool:
        pass


Filter: TypeAlias = Callable[[LogRecord], bool]
"""A filter ready to be added."""
_Filter: TypeAlias = Callable[..., BaseLogFilter]
"""A callable filter constructor."""


# -----------------------------------------------------------------------------
#   Callable filters
# -----------------------------------------------------------------------------


class ServiceFilter(BaseLogFilter):
    """Adds a service name attribute to `logging.LogRecord` records."""

    def __init__(self, service_name: str):
        self.service_name = service_name

    def __call__(self, record: LogRecord) -> bool:
        setattr(record, "service", self.service_name)
        return True


class StripMarkupFilter(BaseLogFilter):
    """Strips markup (like '[bold], [/bold]') from log messages."""

    def __init__(self, pattern: str = r"\[/?[^\]]*\]"):
        """
        Args:
            pattern (str): Regex pattern to strip from messages
                Defaults to removing markup tags
        """
        self.pattern = re.compile(pattern)

    def __call__(self, record: LogRecord) -> bool:
        if hasattr(record, "msg") and isinstance(record.msg, str):
            record.msg = self.pattern.sub("", record.msg)
        return True
