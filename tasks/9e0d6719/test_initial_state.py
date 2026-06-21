# test_initial_state.py
#
# This pytest suite validates that the workstation starts from the **expected
# pristine state** before the student begins editing any files.  It checks the
# presence and exact contents of the _initial_ configuration files only.
#
# IMPORTANT
# ---------
# • These tests purposefully do **not** look for the eventual output file
#   `change_log.txt` (or any other post-task artefacts).  They only assert the
#   existence and byte-for-byte contents of the two files that are supposed to
#   be present at the outset.
# • All paths are absolute, as required.

import difflib
import os
import stat
from pathlib import Path

import pytest

CONFIG_DIR = Path("/home/user/project/config")
APP_YAML   = CONFIG_DIR / "app.yaml"
DB_TOML    = CONFIG_DIR / "database.toml"

EXPECTED_APP_YAML = (
    "name: SampleApp\n"
    "version: 1.2.3\n"
    "settings:\n"
    "  debug: false\n"
    "  max_connections: 50\n"
)

EXPECTED_DB_TOML = (
    "[database]\n"
    "host = \"localhost\"\n"
    "port = 5432\n"
    "user = \"appuser\"\n"
    "password = \"secret\"\n"
    "timeout = 30\n"
)


def _read_text(path: Path) -> str:
    """Utility that returns the full text content of *path*.

    If reading fails, the pytest assertion message will clearly state why.
    """
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover — shouldn’t happen
        pytest.fail(f"Could not read {path}: {exc}")


def _assert_exact_content(actual: str, expected: str, path: Path) -> None:
    """Assert that *actual* equals *expected*.  Show a contextual diff on error."""
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile="expected",
                tofile=str(path),
            )
        )
        pytest.fail(
            f"File {path} does not match the expected initial contents. "
            f"Diff (expected → actual):\n{diff}"
        )


def test_config_directory_exists():
    assert CONFIG_DIR.exists(), f"Required directory {CONFIG_DIR} is missing."
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    ("path_obj", "expected_contents"),
    [
        (APP_YAML, EXPECTED_APP_YAML),
        (DB_TOML, EXPECTED_DB_TOML),
    ],
    ids=lambda x: x.name if isinstance(x, Path) else "contents",
)
def test_initial_file_contents(path_obj: Path, expected_contents: str):
    """
    The two configuration files must exist **and** contain exactly the unaltered
    initial boiler-plate shipped by the junior configuration manager.
    """
    actual_contents = _read_text(path_obj)
    _assert_exact_content(actual_contents, expected_contents, path_obj)


def test_files_are_user_writable():
    """
    Both files should be writable by their owner so the student can edit them
    without using sudo.
    """
    for path_obj in (APP_YAML, DB_TOML):
        mode = path_obj.stat().st_mode
        assert mode & stat.S_IWUSR, f"{path_obj} is not writable by its owner."