from enum import StrEnum
from logging import Formatter
from typing import Dict, Type

from .formatters import ContextJSONFormatter, JSONFormatter


class FormatterType(StrEnum):
    FORMATTER = "formatter"
    JSON = "json"
    CONTEXT_JSON = "context_json"


class FormatterRegistry:
    """Registry for managing and creating log formatters."""

    _formatters: Dict[FormatterType, Type[Formatter]] = {
        FormatterType.FORMATTER: Formatter,
        FormatterType.JSON: JSONFormatter,
        FormatterType.CONTEXT_JSON: ContextJSONFormatter,
    }

    @classmethod
    def create_fmtter(
        cls,
        type: FormatterType | str,
        **kwargs,
    ) -> Formatter:
        """Create a formatter instance of specified type.

        Args:
            type (FormatterType | str): The type of formatter to create

        Returns:
            A formatter instance
        """

        _type = (
            type
            if isinstance(type, FormatterType)
            else FormatterType[type.strip().upper()]
        )
        if _type not in cls._formatters:
            # TODO:
            raise ...

        fmtter_cls = cls._formatters[_type]
        return fmtter_cls(**kwargs)
