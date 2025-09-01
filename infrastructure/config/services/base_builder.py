from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

ConfigType = TypeVar("ConfigType", bound=BaseModel, covariant=True)


class BaseConfigBuilder(Generic[ConfigType], ABC):
    """Abstract base for all config builders.

    This class is generic over a covariant `ConfigType` (a subclass of
    `pydantic.BaseModel`), meaning its internal config objects must not be
    mutated after assignment.

    All adapters inheriting from this abstact base
    (e.g., `LoggerConfigBuilder`) should only contain methods for config read
    or generation. This base provides:
        - reset(): Resets internal config to its original default state
        - build(): Finalizes and returns current config

    Notes:
        - Do not mutate fields of `self._base_config`, `self._current_config`.
        - This class enforces read-only semantics/config state to satisfy
          covariance.
        - This class should not be instantiated directly.
    """

    def __init__(self, config: ConfigType):
        self._base_config = config
        self._current_config = config.model_copy(deep=True)

    def reset(self) -> "BaseConfigBuilder[ConfigType]":
        """Reset to base configuration.

        Returns:
            The config builder. Note: use `.build()` to
            apply the changes and get the config itself.
        """

        self._current_config = self._base_config.model_copy(deep=True)
        return self

    def build(self) -> ConfigType:
        """Build the final configuration.

        Note:
            `this` should be used after applying changes
            to the config.

        Returns:
            The config.
        """

        return self._current_config.model_copy(deep=True)

    # -------------------------------------------------------------------------
    #   Abstract methods
    # -------------------------------------------------------------------------

    # I don't know when I should use this
    # @abstractmethod
    # def name(self, n: str):
    #     """Assign a name to config built."""
    #
    #     return self._current_config.model_copy(update={"name": n})

    # -------------------------------------------------------------------------
    #   Private methods
    #   internally used to help child builders validate
    #   reconfig data
    # -------------------------------------------------------------------------

    def _validated_copy(self, model: BaseModel, **kwupdate) -> BaseModel:
        """Update and validate changes to config.

        Args:
            model: The model to validate `kwupdate` in.
            kwupdate: The changes to make in the config.

        Returns:
            Updated and validated config instance.
        """

        data = model.model_dump()
        data.update(kwupdate)
        return model.__class__(**data)
