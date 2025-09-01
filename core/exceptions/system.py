from .base import CoreError


class SystemConfigError(CoreError):
    # Bad or missing core config, env variable, or setup

    pass


class SystemResourceError(CoreError):
    # Missing files, memory issues, resource exhaustion
    pass


class SystemDependencyError(CoreError):
    # Missing or incompatible third-party dependency
    pass
