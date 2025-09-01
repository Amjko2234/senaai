from typing import Any, Dict


class LoadedEnv:
    """Container for loaded and validated environment variables."""

    def __init__(self, variables: Dict[str, Any]):
        self._variables = variables

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            # TODO:
            raise ...

        if name in self._variables:
            return self._variables[name]

    def __repr__(self) -> str:
        vars_list = ", ".join(
            f"{k}={type(v).__name__}" for k, v in self._variables.items()
        )
        return f"LoadedEnv({vars_list})"

    def get(self, name: str, default: Any = None) -> Any:
        """Get the environment variable with optional default."""

        return self._variables.get(name, default)

    def to_dict(self) -> Dict[str, Any]:
        """Return all variables as dictionary."""

        return self._variables.copy()
