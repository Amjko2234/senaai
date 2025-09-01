from enum import StrEnum
from typing import Dict, List

from .filters import BaseLogFilter, ServiceFilter, StripMarkupFilter, _Filter

# -----------------------------------------------------------------------------
#   Registry
# -----------------------------------------------------------------------------


class FilterType(StrEnum):
    SERVICE = "service"
    STRIP_MARKUP = "strip_markup"


class FilterRegistry:
    """Registry for managing and creating log filters."""

    _filters: Dict[FilterType, _Filter] = {
        FilterType.SERVICE: ServiceFilter,
        FilterType.STRIP_MARKUP: StripMarkupFilter,
    }

    @classmethod
    def create_filter(
        cls,
        type: FilterType | str,
        **kwargs,
    ) -> BaseLogFilter:
        """Create a filter instance of specified type.

        Args:
            type (FilterType | str): The type of filter to create

        Returns:
            A filter instance
        """

        _type = (
            type if isinstance(type, FilterType) else FilterType[type.strip().upper()]
        )
        if _type not in cls._filters:
            # TODO:
            raise ...

        filter_cls = cls._filters[_type]
        return filter_cls(**kwargs)

    @classmethod
    def registry_filter(
        cls,
        type: FilterType,
        filter: _Filter,
    ) -> None:
        """Registry a new filter type."""

        cls._filters[type] = filter

    @classmethod
    def get_filters(cls) -> List[FilterType]:
        """Get the list of available filters."""

        return list(cls._filters.keys())
