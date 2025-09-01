from .base import CoreError


class DomainError(CoreError):
    # Base for all domain-layer violations
    pass


class DomainValidationError(CoreError):
    # Invalid domain model state
    pass


class DomainOperationError(CoreError):
    # Failure during valid-but-unsuccessful operation
    pass
