from typing import Optional

from ..core.exceptions.error_codes import ErrorCode
from ..core.exceptions.infrastructure import InfrastructureError


class ConfigError(InfrastructureError):
    """Raised for configuration-related errors."""

    def __init__(
        self,
        message: str = "Failed to read or get the configuration",
        err_code: ErrorCode = ErrorCode.INF_UNK_CFG_504,
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )


class LookupError(InfrastructureError):
    """Raised when failure to lookup something."""

    def __init__(
        self,
        message: str = "Failed to lookup a value",
        err_code: ErrorCode = ErrorCode.INF_UNK_LOOK_501,
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )


class MissingValueError(LookupError):
    """Raised when required values are missing."""

    def __init__(
        self,
        message: str = "Required values are missing.",
        err_code: ErrorCode = ErrorCode.INF_UNK_LOOK_501,
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )


class RegistryLookupError(LookupError):
    """Base for failed lookups in infrastructure registries."""

    def __init__(
        self,
        message: str = "Failed to lookup a registry",
        err_code: ErrorCode = ErrorCode.INF_UNK_LOOK_503,
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            service=service,
            **kwargs,
        )
