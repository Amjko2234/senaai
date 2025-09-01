from typing import Optional

from ...core.exceptions.error_codes import ErrorCode
from ..exceptions import ConfigError, MissingValueError


class UnknownConfigTypeDetector(ConfigError):
    """Raised when no config types are detected."""

    def __init__(
        self,
        message: str = "No configuration type detected.",
        err_code: ErrorCode = ErrorCode.INF_TDET_CFG_527,
        *,
        service: Optional[str] = "config_type_detector",
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )


class MissingConfigValueError(MissingValueError):
    """Raised when a config is missing required values."""

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        *,
        service: Optional[str] = "config_builder_model",
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )
