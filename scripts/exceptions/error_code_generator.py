"""Error Code Generator

Generates the `ErrorCode` Enum from a JSON registry of error codes.

Input:
    JSON file: /Sena/data/config/core/exceptions/error_codes.json
    Schema: /Sena/data/config/core/exceptions/error_code_registry.json
    Must match pattern: ^[A-Z]{3}-[A-Z]{2,4}-[A-Z]{2,4}-\\d{3}$

Output:
    Python Enum file: /Sena/core/exceptions/error_codes.py

Usage:
    python3 -m Sena.scripts.exceptions.error_code_generator
"""

from pathlib import Path
from typing import Any, Dict, List, overload

from jsonschema import validate

from ...config.paths import PROJECT_ROOT
from ...shared.scripts.generator_output_docstrings import ERROR_CODE_SOURCE_DOCSTRING
from ...shared.utils import IOUtils, PathUtils

# -----------------------------------------------------------------------------
#   Constants
# -----------------------------------------------------------------------------

REGISTRY_PATH = f"{PROJECT_ROOT}/config/core/exceptions/error_codes.yaml"
SCHEMA_PATH = f"{PROJECT_ROOT}/config/core/exceptions/error_code_registry.json"
OUTPUT_PATH = f"{PROJECT_ROOT}/core/exceptions/error_codes.py"

DEFAULT_ENCODING = "utf-8"

# -----------------------------------------------------------------------------
#   Helper functions
# -----------------------------------------------------------------------------


@overload
def load_json(
    path: Path,
    *,
    expect: type[Dict],
) -> Dict[str, Any]: ...


@overload
def load_json(
    path: Path,
    *,
    expect: Any,
) -> Any: ...


def load_json(path: Path, *, expect: type[Any]) -> Any:
    """Load a JSON file from disk.

    Args:
        path (Path): Path to the JSON file
        expect (type): Expected Python type (e.g. dict, list)

    Returns:
        Parsed JSON content (cast to `expect`).

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        TypeError: If the loaded JSON is not of the expected type.
    """

    data = IOUtils.load_json(path)
    _validate_data_instance(data, expect)
    return data


@overload
def load_yaml(
    path: Path,
    *,
    expect: type[List],
) -> List[Dict[str, Any]]: ...


@overload
def load_yaml(
    path: Path,
    *,
    expect: Any,
) -> Any: ...


def load_yaml(path: Path, *, expect: type[Any]) -> Any:
    """Load a YAML file from disk.

    Args:
        path (Path): Path to the YAML file
        expect (type): Expected Python type (e.g. dict, list)

    Returns:
        Parsed YAML content (cast to `expect`).

    Raises:
    """

    data = IOUtils.load_yaml(path)
    _validate_data_instance(data, expect)
    return data


def _validate_data_instance(obj: object, expect: type[Any]) -> None:
    """Ensure the instance of the object matches the expected instance."""

    if not isinstance(obj, expect):
        raise


def validate_registry(registry: List, schema: Dict[str, Any]) -> None:
    """Validate the error code registry against the JSON Schema.

    Args:
        registry (List): List of error code entries
        schema (Dict): JSON Schema to validate against

    Raises:
        jsonschema.exceptions.ValidationError: If registry is invalid.
        ValueError: If a duplicated error code is found.
    """

    validate(instance=registry, schema=schema)

    # Ensure no duplicated error code
    seen_codes = set()
    for entry in registry:
        code = entry["code"]
        if code in seen_codes:
            raise ValueError(f"Error code '{code}' is duplicated")
        seen_codes.add(code)


def generate_enum_source(registry: List) -> str:
    """Generate the Python Enum source code from the validated registry.

    Args:
        registry (List): List of error code entries

    Returns:
        Python source code for the `ErrorCode` StrEnum (string Enum).
    """

    lines = [
        f'"""{ERROR_CODE_SOURCE_DOCSTRING}"""',
        "",
        "from enum import StrEnum",
        "",
        "class ErrorCode(StrEnum):",
    ]

    indent = "    "  # Default indentation in python

    for entry in registry:

        # Each entry gets an inline comment of its description
        code_name = entry["code"].replace("-", "_")
        lines.append(
            f"{indent}{code_name} = '{entry['code']}'  # {entry['description']}"
        )

    return "\n".join(lines)


# -----------------------------------------------------------------------------
#   Main
#   Should be ran separte from app
# -----------------------------------------------------------------------------


def main():
    """Orchestrate the error code Enum generation process.

    - Load registry and schema
    - Validate registry
    - Generate Enum Python code
    - Write output file
    """

    registry = load_yaml(Path(REGISTRY_PATH), expect=List)
    schema = load_json(Path(SCHEMA_PATH), expect=Dict)
    validate_registry(registry, schema)

    enum_source = generate_enum_source(registry)
    output_path = PathUtils.validate_path(Path(OUTPUT_PATH))
    IOUtils.write(enum_source, output_path)

    print(f"Generated {Path(OUTPUT_PATH).name} successfully")


if __name__ == "__main__":
    main()
