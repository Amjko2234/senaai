from .base import CoreWarning


class DeprecationNotice(CoreWarning):
    # For custom deprecation tracking
    pass


class PerformanceCoreWarning(CoreWarning):
    # Performance degradation notices
    pass


class ConfigurationCoreWarning(CoreWarning):
    # Suspicious but non fatal config
    pass


class ExperimentalFeatureCoreWarning(CoreWarning):
    # Unstable or preview feature usage
    pass
