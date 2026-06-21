# test_initial_state.py
#
# Pytest suite that validates the INITIAL operating-system / filesystem
# state for the “MyApp” configuration-management exercise.
#
# These tests must all PASS **before** the student performs any actions.
# If one of them fails, the project’s starting environment is not set up
# according to the specification and the exercise itself becomes invalid.
#
# Only Python’s stdlib and pytest are used.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
MYAPP_DIR = HOME / "myapp"
BIN_DIR = HOME / "bin"
ENV_CONFIGS_DIR = HOME / "env-configs"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_file_lines(path: Path):
    """Return the file’s contents as a list of lines *without* trailing '\n's."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def is_executable(path: Path) -> bool:
    """Return True if path’s mode indicates 0o755 permissions."""
    mode = path.stat().st_mode & 0o777
    return mode == 0o755


# ---------------------------------------------------------------------------
# Tests for initial state
# ---------------------------------------------------------------------------

def test_myapp_bin_and_start_sh_exist():
    """/home/user/myapp/bin must exist and contain start.sh with correct mode and lines."""
    bin_dir = MYAPP_DIR / "bin"
    start_sh = bin_dir / "start.sh"

    assert bin_dir.is_dir(), f"Expected directory {bin_dir} to exist."
    assert start_sh.is_file(), f"Expected file {start_sh} to exist inside {bin_dir}."

    # Permissions
    assert is_executable(start_sh), (
        f"{start_sh} must have mode 0755 but has {oct(start_sh.stat().st_mode & 0o777)}."
    )

    # Exact file content
    expected_lines = ["#!/bin/bash", 'echo "Starting MyApp"']
    actual_lines = read_file_lines(start_sh)
    assert actual_lines == expected_lines, (
        f"{start_sh} must contain exactly these two lines:\n"
        f"{expected_lines}\nFound:\n{actual_lines}"
    )


def test_myapp_conf_app_conf_content():
    """/home/user/myapp/conf/app.conf must have exactly the 3 expected lines."""
    conf_dir = MYAPP_DIR / "conf"
    app_conf = conf_dir / "app.conf"

    assert conf_dir.is_dir(), f"Expected directory {conf_dir} to exist."
    assert app_conf.is_file(), f"Expected file {app_conf} to exist."

    expected_lines = [
        "# MyApp Main configuration",
        "log_level=INFO",
        "max_threads=4",
    ]
    actual_lines = read_file_lines(app_conf)
    assert actual_lines == expected_lines, (
        f"{app_conf} must contain exactly these lines:\n"
        f"{expected_lines}\nFound:\n{actual_lines}"
    )


def test_home_user_bin_exists_and_is_empty():
    """/home/user/bin must exist and *not* yet contain any files (empty directory)."""
    assert BIN_DIR.is_dir(), f"Expected directory {BIN_DIR} to exist."

    # Filter out '.' and '..' entries implicitly; Path.iterdir() yields only real entries
    contents = list(BIN_DIR.iterdir())
    assert contents == [], (
        f"{BIN_DIR} should be empty at start of exercise, but contains: "
        f"{[p.name for p in contents]}"
    )


def test_env_configs_directory_absent_initially():
    """/home/user/env-configs must NOT exist before student actions."""
    assert not ENV_CONFIGS_DIR.exists(), (
        f"Directory {ENV_CONFIGS_DIR} should NOT exist in the initial state."
    )


@pytest.mark.parametrize(
    "forbidden_path",
    [
        HOME / "env-configs" / "change_log.txt",
        HOME / "env-configs" / "done.flag",
    ],
)
def test_no_change_log_or_done_flag_anywhere(forbidden_path):
    """Neither change_log.txt nor done.flag should exist anywhere under /home/user."""
    for root, _dirs, files in os.walk(HOME):
        if forbidden_path.name in files:
            pytest.fail(f"Found unexpected file {forbidden_path.name} at {root}.")


def test_bashrc_has_no_myapp_entries_and_ends_with_newline():
    """/home/user/.bashrc must not yet reference MYAPP_HOME or enable_cache; must end with newline."""
    bashrc = HOME / ".bashrc"
    assert bashrc.is_file(), f"Expected {bashrc} to exist."

    with bashrc.open("rb") as f:
        content_bytes = f.read()

    # Ensure file ends with a single newline character.
    assert content_bytes.endswith(b"\n"), f"{bashrc} must end with a newline character."

    # Decode once for text search
    content = content_bytes.decode("utf-8", errors="replace")

    assert "MYAPP_HOME" not in content, (
        f"{bashrc} should NOT contain 'MYAPP_HOME' in the initial state."
    )
    assert "enable_cache" not in content, (
        f"{bashrc} should NOT contain 'enable_cache' in the initial state."
    )