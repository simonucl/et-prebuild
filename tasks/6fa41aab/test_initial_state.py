# test_initial_state.py
#
# Pytest suite that validates the _initial_ filesystem/OS state **before**
# the student performs any changes.  It checks that all required
# directories and placeholder configuration files exist with the expected
# default content and permissions.  It also confirms that the update log
# file is **absent**, because it should be created only after the task
# is completed.

import os
import stat
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path("/home/user/project")
DIRS_EXPECTED = {
    PROJECT_ROOT,
    PROJECT_ROOT / "config",
    PROJECT_ROOT / "logs",
}

# Expected POSIX permission bits (only the rwx part is relevant here).
MODE_DIR   = 0o755
MODE_FILE  = 0o644

# Expected placeholder configuration contents (including the trailing '\n').
EXPECTED_YAML = (
    "remove_duplicates: false\n"
    "missing_value_strategy: mean\n"
    "columns: []\n"
)

EXPECTED_TOML = (
    'remove_duplicates = false\n'
    'missing_value_strategy = "mean"\n'
    'columns = []\n'
)

YAML_PATH = PROJECT_ROOT / "config" / "cleaning.yml"
TOML_PATH = PROJECT_ROOT / "config" / "cleaning.toml"
LOG_PATH  = PROJECT_ROOT / "logs"   / "config_update.log"


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _mode(path: Path) -> int:
    """
    Return the permission bits (e.g., 0o755) of a file or directory.
    """
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_directories_exist_with_correct_mode():
    """
    Ensure all required directories are present and have 0755 permissions.
    """
    for d in DIRS_EXPECTED:
        assert d.exists(), f"Required directory {d} is missing."
        assert d.is_dir(), f"{d} exists but is not a directory."
        actual_mode = _mode(d)
        assert actual_mode == MODE_DIR, (
            f"Directory {d} has mode {oct(actual_mode)}, expected {oct(MODE_DIR)}."
        )

@pytest.mark.parametrize(
    "path, expected_content",
    [
        (YAML_PATH, EXPECTED_YAML),
        (TOML_PATH, EXPECTED_TOML),
    ],
)
def test_placeholder_config_files_exist_with_correct_content_and_mode(path, expected_content):
    """
    Check that the placeholder YAML and TOML files exist, have the correct
    default template content, correct permissions (0644), and a trailing newline.
    """
    assert path.exists(), f"Configuration file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_mode = _mode(path)
    assert actual_mode == MODE_FILE, (
        f"File {path} has mode {oct(actual_mode)}, expected {oct(MODE_FILE)}."
    )

    content = path.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"File {path} does not contain the expected placeholder content.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Found ----\n"
        f"{content!r}"
    )

def test_update_log_file_does_not_yet_exist():
    """
    The log file should *not* exist before the student performs any action.
    """
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} already exists, but it should be created only after the "
        "configuration files are updated."
    )