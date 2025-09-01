import json
from pathlib import Path
from typing import Any, Dict, Optional, Type

import yaml
from dotenv import dotenv_values
from jsonschema import ValidationError, validate

# -----------------------------------------------------------------------------
#   Functions exposed with an API
# -----------------------------------------------------------------------------


def _load_env(
    path: Path,
    *,
    expect: Optional[Type[dict]],
) -> Dict[str, str | None]:

    data = dotenv_values(path)

    if expect:
        if not isinstance(data, expect):
            # TODO:
            raise ...

    return data


def _load_json(
    path: Path,
    *,
    encoding: str,
    schema: Optional[Path],
    expect: Optional[Type[Any]],
) -> Any:

    with open(path, mode="r", encoding=encoding) as file:
        data = json.load(file)
        if schema:
            with open(schema, mode="r") as schema_file:
                schema_data = json.load(schema_file)
                try:
                    validate(instance=data, schema=schema_data)
                except ValidationError:
                    return None
        if expect:
            if not isinstance(data, expect):
                # TODO:
                raise ...

        return data


def _load_yaml(
    path: Path,
    *,
    encoding: str,
    expect: Optional[Type[Any]],
) -> Any:

    with open(path, mode="r", encoding=encoding) as file:
        data = yaml.safe_load(file)

        if expect:
            if not isinstance(data, expect):
                # TODO:
                raise ...

        return data


def _write(
    content: str,
    path: Path,
    *,
    encoding: str,
) -> None:

    with open(path, "w", encoding=encoding) as file:
        file.write(content)


def _clear_content(
    path: Path,
    *,
    encoding: str,
) -> None:

    _write("", path, encoding=encoding)


# -----------------------------------------------------------------------------
#   Internal helper functions
# -----------------------------------------------------------------------------
