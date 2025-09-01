"""Config loading and registry exceptions default messages.

This module defines the default exception and warning messages,
that should not be modified, and should not have a dedicated config
'.json' file, for these messages can be raised before extracting
values from config JSON files.

Enums:
    ConfigErrorMessage: Unable to load JSON files, stop the program
    ConfigWarningMessage: Inform in logs, but allow program to continue

Note:
    Do not modify any of the default messages.
"""

from enum import StrEnum


class ConfigErrorMessage(StrEnum):
    """
    Default error messages for loading config '.json' files.

    Do not modify any values.
    """

    # Note: Full path is prefixed at the beginning
    INVALID_CONFIG_PATH = "path does not exist or is not a file"
    # Note: Invalid file is prefixed at the beginning
    INVALID_JSON_FILE = "file does not exist"


class ConfigWarningMessage(StrEnum):
    """
    Default warning messages before trying to load config '.json' files.

    Do not modify any values.
    """

    # Note: Invalid input is appended at the end
    INVALID_INPUT_CONFIG_PATH = "input config path should not include '.json'"
