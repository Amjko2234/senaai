from typing import Optional

from .base import CoreError, CoreWarning
from .error_codes import ErrorCode


class FilesystemError(CoreError):
    """Base for all IO-layer exceptions."""

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


class FilesystemWarning(CoreWarning):
    """Base for all recoverable IO-layer exceptions."""

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


class FileNotFoundError(FilesystemError):
    """General error for validating a non-existing file."""

    def __init__(
        self,
        message: str = "Failed to get file",
        err_code: ErrorCode = ErrorCode.COR_UNK_IO_301,
        layer: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            **kwargs,
        )


class FileNotFoundWarning(FilesystemWarning):
    """Recoverable general error for validating a non-existing file."""

    def __init__(
        self,
        message: str = "Recoverable: failed to get file",
        err_code: ErrorCode = ErrorCode.COR_UNK_IO_302,
        layer: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            err_code=err_code,
            layer=layer,
            **kwargs,
        )
