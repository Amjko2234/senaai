from typing import Optional

from .base import CoreError, CoreWarning
from .error_codes import ErrorCode


class InfrastructureError(CoreError):
    """Base for all infrastructure-layer exceptions."""

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str] = "infrastructure",
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )


class DatabaseError(CoreError):
    """"""

    # Database connection or query issues
    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str],
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )


class CacheError(CoreError):
    """"""

    # Caching system failures
    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str],
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )


class NetworkError(CoreError):
    """"""

    # HTTP or Socket failures
    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str],
        *,
        service: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )
