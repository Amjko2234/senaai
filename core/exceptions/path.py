from typing import Optional

from .base import CoreError, CoreWarning
from .error_codes import ErrorCode


class PathsystemError(CoreError):
    """Base for all path-layer exceptions."""

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str] = None,
        *,
        service: Optional[str] = "io",
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )


class PathsystemWarning(CoreWarning):
    """Base for all recoverable path-layer exceptions."""

    def __init__(
        self,
        message: str,
        err_code: ErrorCode,
        layer: Optional[str] = None,
        *,
        service: Optional[str] = "io",
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            service=service,
            **kwargs,
        )


# -----------------------------------------------------------------------------
#   Children
# -----------------------------------------------------------------------------


class PathNotFoundError(PathsystemError):
    """General error for validating a non-existing path."""

    def __init__(
        self,
        message: str = "Failed to get path",
        err_code: ErrorCode = ErrorCode.COR_UNK_IO_303,
        layer: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            **kwargs,
        )


class PathNotFoundWarning(PathsystemWarning):
    """Recoverable general error for validating a non-exisitng path."""

    def __init__(
        self,
        message: str = "Recoverable: failed to get path",
        err_code: ErrorCode = ErrorCode.COR_UNK_IO_304,
        layer: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            **kwargs,
        )
