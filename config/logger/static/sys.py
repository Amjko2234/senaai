from pathlib import Path

from ....config import PROJECT_ROOT

SYSTEM_LOGGER_CONFIG = {
    "name": "system",
    "path": Path(f"{PROJECT_ROOT}/core/utils/logger"),
    "console": {
        "enabled": True,
        "level": "INFO",
    },
    "file": {
        "enabled": True,
        "output_to": Path(f"{PROJECT_ROOT}/logs/"),
        "output_name": "system",
        "level": "DEBUG",
        "max_size_mb": 50,
        "backup_count": 10,
    },
    "async": {
        "enabled": False,
        "queue_size": 1000,
        "timeout": 1,
    },
    "security": {
        "enabled": True,
        "sanitize_sensitive_data": True,
    },
    "filters": {
        "enabled": False,
        "rate_limit": 1,
        "include_patterns": [],
        "exclude_patterns": [],
    },
}
