from pathlib import Path

# -----------------------------------------------------------------------------
#   Internal functions
# -----------------------------------------------------------------------------


def _get_root_path(
    start: Path,
    root_name: str,
) -> Path:

    for parent in start.resolve().parents:
        if parent.name == root_name:
            return parent
    raise NameError(f"{PROJECT_NAME} root name not found")


# -----------------------------------------------------------------------------
#   Public functions
# -----------------------------------------------------------------------------


def get_relative(abs_path: Path) -> Path:
    """Convert the absolute path to be relative to the root."""

    return abs_path.relative_to(PROJECT_ROOT)


# -----------------------------------------------------------------------------
#   Constants
# -----------------------------------------------------------------------------

PROJECT_NAME = "Sena"
PROJECT_ROOT = _get_root_path(Path(__file__), PROJECT_NAME)
