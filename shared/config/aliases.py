"""Type aliases for config JSON files.

Type Aliases:
    FilePath: Tuple of dir that leads to file name
    ConfigValues: Values extracted from a JSON file

"""

from __future__ import annotations

from typing import Dict, List, TypeAlias

# -----------------------------------------------------------------------------
#   Public Aliases
# -----------------------------------------------------------------------------

# More specific and practical type aliases
ConfigScalar: TypeAlias = str | int | float | bool | None

# JSON always returns dict at top level (per JSON spec)
JsonConfig: TypeAlias = Dict[str, "JsonValue"]
JsonValue: TypeAlias = ConfigScalar | Dict[str, "JsonValue"] | List["JsonValue"]

# YAML can be any of these at top level
YamlConfig: TypeAlias = ConfigScalar | Dict[str, "YamlValue"] | List["YamlValue"]
YamlValue: TypeAlias = ConfigScalar | Dict[str, "YamlValue"] | List["YamlValue"]

# ENV files are always string key=value pairs
EnvConfig: TypeAlias = Dict[str, str]

# Union for broad type hinting (use like `Any`)
ConfigValues: TypeAlias = JsonConfig | YamlConfig | EnvConfig
"""Configuration values from config files."""

ConfigType: TypeAlias = str
"""Configuration type detected before reading config values."""
