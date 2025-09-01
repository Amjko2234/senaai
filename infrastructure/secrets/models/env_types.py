from enum import StrEnum


class EnvType(StrEnum):
    """Supported environment types for different deployment contexts."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
