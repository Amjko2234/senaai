import inspect
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ...shared.core import KNOWN_LAYERS
from ...shared.exceptions.aliases import LineNo
from ...shared.logger.log_levels import LogLevel
from ..exceptions.error_codes import ErrorCode
from ..protocols.infrastructure.logger import ServiceLoggerProtocol

# ------------------------------------------------------------------------------
#   Mixins
#   Inherited by core exceptions and warnings
# ------------------------------------------------------------------------------


class SerializableExceptionMixin:

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to a serializable dict."""

        raise NotImplementedError


# ------------------------------------------------------------------------------
#   Custom exceptions and warnings
#   Exposed for other exceptions to inherit from
# ------------------------------------------------------------------------------


class CoreError(Exception, SerializableExceptionMixin):
    """Base exception for all custom exceptions."""

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        file_path: Optional[Path] = None,
        line_no: Optional[LineNo] = None,
        *,
        layer: Optional[str] = None,
        service: Optional[str] = None,
        cause: Optional[BaseException] = None,
        user_message: Optional[str] = None,
        severity: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        logger: Optional[ServiceLoggerProtocol] = None,
        log_level: LogLevel = LogLevel.DEBUG,
    ):
        self.message = message
        self.error_code = err_code

        if (file_path is None) or (line_no is None):
            caller_frame = self._find_caller_frame()
            self.file_path = caller_frame.f_code.co_filename
            self.line_no = caller_frame.f_lineno
        else:
            self.file_path = file_path
            self.line_no = line_no

        self.file_name = str(self.file_path).split("/")[-1].split("\\")[-1]
        self.layer = layer or self._infer_layer()
        self.service = service or self._infer_service()
        self.__cause__ = cause
        self.user_message = user_message or message
        self.severity = severity or "ERROR"
        self.timestamp = timestamp or datetime.now(timezone.utc)

        if logger:
            log_function = {
                LogLevel.DEBUG: logger.debug,
                LogLevel.INFO: logger.info,
                LogLevel.WARNING: logger.warning,
                LogLevel.ERROR: logger.error,
                LogLevel.CRITICAL: logger.critical,
            }.get(log_level, logger.error)
            log_function(message)

        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"[{self.error_code}] {self.message} "
            f"(at {self.file_name}:{self.line_no})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"message='{self.message}'"
            f"error_code='{self.error_code}'"
            f"file_path='{self.file_path}'"
            f"line_number='{self.line_no}'"
        )

    # -------------------------------------------------------------------------
    #   Public methods
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "line_number": self.line_no,
            "layer": self.layer,
            "service": self.service,
            "cause": repr(self.__cause__) if self.__cause__ else None,
            "user_message": self.user_message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }

    # -------------------------------------------------------------------------
    #   Private helper methods
    # -------------------------------------------------------------------------

    def _find_caller_frame(self):
        """Walk up the stack to find caller's frame.

        Detect the frame is of the caller by looking for the first frame that
        is not part of the exception hierarchy initialization.

        Returns:
            Caller's frame.
        """

        frame = inspect.currentframe()

        while frame:
            frame = frame.f_back
            if frame is None:
                break

            # Get the class being called in this frame
            frame_locals = frame.f_locals

            # Skips frames that are __init__ of exception classes
            if (
                "self" in frame_locals
                and isinstance(frame_locals["self"], CoreError)
                and frame.f_code.co_name == "__init__"
            ):
                continue

            return frame

        # Fallback (shouldn't happen normally)
        return inspect.currentframe().f_back

    def _infer_layer(self) -> Optional[str]:
        """Extract layer type from module path."""

        mod_path = self.__class__.__module__
        for layer in KNOWN_LAYERS:
            if f".{layer}" in mod_path or mod_path.startswith(layer):
                return layer

        return None

    def _infer_service(self) -> Optional[str]:
        """Extract service name from module path."""

        mod_parts = self.__class__.__module__.split(".")

        for layer in KNOWN_LAYERS:
            if layer in mod_parts:
                idx = mod_parts.index(layer)
                if len(mod_parts) > idx + 1:
                    # Service name is after the layer
                    return mod_parts[idx + 1]
                # Layer found but no service segment
                break

        return None


class CoreWarning(Warning):
    # Root for all warnings

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        file_path: Optional[Path] = None,
        line_no: Optional[LineNo] = None,
        *,
        layer: Optional[str] = None,
        service: Optional[str] = None,
        cause: Optional[BaseException] = None,
        user_message: Optional[str] = None,
        severity: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        logger: Optional[ServiceLoggerProtocol] = None,
        log_level: LogLevel = LogLevel.DEBUG,
    ):
        self.message = message
        self.error_code = err_code

        if (file_path is None) or (line_no is None):
            caller_frame = self._find_caller_frame()
            self.file_path = caller_frame.f_code.co_filename
            self.line_no = caller_frame.f_lineno
        else:
            self.file_path = file_path
            self.line_no = line_no

        self.file_name = str(self.file_path).split("/")[-1].split("\\")[-1]
        self.layer = layer or self._infer_layer()
        self.service = service or self._infer_service()
        self.__cause__ = cause
        self.user_message = user_message or message
        self.severity = severity or "WARNING"
        self.timestamp = timestamp or datetime.now(timezone.utc)

        if logger:
            log_function = {
                LogLevel.DEBUG: logger.debug,
                LogLevel.INFO: logger.info,
                LogLevel.WARNING: logger.warning,
                LogLevel.ERROR: logger.error,
                LogLevel.CRITICAL: logger.critical,
            }.get(log_level, logger.error)
            log_function(message)

        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"[{self.error_code}] {self.message} "
            f"(at {self.file_name}:{self.line_no})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"message='{self.message}'"
            f"error_code='{self.error_code}'"
            f"file_path='{self.file_path}'"
            f"line_number='{self.line_no}'"
        )

    # -------------------------------------------------------------------------
    #   Public methods
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "line_number": self.line_no,
            "layer": self.layer,
            "service": self.service,
            "cause": repr(self.__cause__) if self.__cause__ else None,
            "user_message": self.user_message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }

    # -------------------------------------------------------------------------
    #   Private helper methods
    # -------------------------------------------------------------------------

    def _find_caller_frame(self):
        """Walk up the stack to find caller's frame.

        Detect the frame is of the caller by looking for the first frame that
        is not part of the exception hierarchy initialization.

        Returns:
            Caller's frame.
        """

        frame = inspect.currentframe()

        while frame:
            frame = frame.f_back
            if frame is None:
                break

            # Get the class being called in this frame
            frame_locals = frame.f_locals

            # Skips frames that are __init__ of exception classes
            if (
                "self" in frame_locals
                and isinstance(frame_locals["self"], CoreError)
                and frame.f_code.co_name == "__init__"
            ):
                continue

            return frame

        # Fallback (shouldn't happen normally)
        return inspect.currentframe().f_back

    def _infer_layer(self) -> Optional[str]:
        """Extract layer type from module path."""

        mod_path = self.__class__.__module__
        for layer in KNOWN_LAYERS:
            if f".{layer}" in mod_path or mod_path.startswith(layer):
                return layer

        return None

    def _infer_service(self) -> Optional[str]:
        """Extract service name from module path."""

        mod_parts = self.__class__.__module__.split(".")

        for layer in KNOWN_LAYERS:
            if layer in mod_parts:
                idx = mod_parts.index(layer)
                if len(mod_parts) > idx + 1:
                    # Service name is after the layer
                    return mod_parts[idx + 1]
                # Layer found but no service segment
                break

        return None


class CoreCriticalError(Exception):
    # Root for all unrecoverable exceptions, should terminate execution
    pass


class CoreNonCriticalError(Exception):
    # Root for all recoverable exceptions (still abnormal behavior)
    pass
