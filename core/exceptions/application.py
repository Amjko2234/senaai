from .base import CoreError


class ApplicationError(CoreError):
    # Base for all application-layer errors
    pass


class ConfigurationError(CoreError):
    # Invalid app-level settings or runtime options
    pass


class ServiceNotAvailableError(CoreError):
    # Downstream service temporarily unavailable
    pass


class OperationTimeoutError(CoreError):
    # Application-level timeout in service orchestration
    pass
