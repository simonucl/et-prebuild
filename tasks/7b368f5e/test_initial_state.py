# test_initial_state.py
"""
Pytest suite to validate the machine *before* the student performs any action.

It checks that:
1. The logs directory exists and is writable.
2. The source log file build_2023-09-01.log exists and contains the exact
   baseline content (including a single trailing newline).
3. None of the target artefacts (critical log, counter file, command record)
   are present yet.

If any assertion fails, the error message should give a clear hint about the
missing or unexpected item.
"""

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
WORKSPACE_DIR = HOME / "workspace" / "app" / "logs"

SOURCE_LOG = WORKSPACE_DIR / "build_2023-09-01.log"
CRITICAL_LOG = WORKSPACE_DIR / "critical_2023-09-01.log"
COUNT_FILE = WORKSPACE_DIR / "critical_2023-09-01.count"
COMMANDS_FILE = WORKSPACE_DIR / "filter_commands.log"

# Expected exact content (including the final newline)
EXPECTED_SOURCE_CONTENT = (
    '2023-09-01 10:01:02 INFO [Init] Application started\n'
    '2023-09-01 10:01:03 WARNING [Config] Missing optional setting "theme"\n'
    '2023-09-01 10:01:04 ERROR [Database] Connection refused\n'
    '2023-09-01 10:02:00 INFO [Heartbeat] Alive\n'
    '2023-09-01 10:03:12 ERROR [Auth] Invalid credentials\n'
    '2023-09-01 10:04:45 INFO [Shutdown] Application stopped\n'
)


def _is_writable(path: Path) -> bool:
    """
    Return True if *path* is writable by the current user
    (regardless of directory permissions, this checks the effective uid/gid).
    """
    try:
        test_file = path / ".pytest_write_check.tmp"
        with open(test_file, "w"):
            pass
        test_file.unlink()
        return True
    except Exception:  # pragma: no cover
        return False


def test_logs_directory_exists_and_writable():
    """
    The directory /home/user/workspace/app/logs must exist and be writable.
    """
    assert WORKSPACE_DIR.exists(), (
        f"Required directory {WORKSPACE_DIR} is missing."
    )
    assert WORKSPACE_DIR.is_dir(), (
        f"{WORKSPACE_DIR} exists but is not a directory."
    )
    # Optional: verify write permission the POSIX way first,
    # then try an actual write as a stronger guarantee.
    mode = WORKSPACE_DIR.stat().st_mode
    is_world_writable = bool(mode & stat.S_IWUSR or mode & stat.S_IWGRP or mode & stat.S_IWOTH)
    assert is_world_writable or _is_writable(WORKSPACE_DIR), (
        f"Directory {WORKSPACE_DIR} is not writable by the current user."
    )


def test_source_log_exists_with_exact_content():
    """
    The baseline log file must exist, be a regular file, and contain the
    expected lines *exactly* (including the trailing newline).
    """
    assert SOURCE_LOG.exists(), f"Baseline log {SOURCE_LOG} is missing."
    assert SOURCE_LOG.is_file(), f"{SOURCE_LOG} exists but is not a regular file."

    content = SOURCE_LOG.read_text(encoding="utf-8")
    assert content == EXPECTED_SOURCE_CONTENT, (
        "Baseline log does not match the expected content.\n"
        "If you modified the file, restore it to its original state."
    )

    # Verify a single trailing newline (i.e., the file ends with '\n' but not '\n\n').
    assert content.endswith("\n"), (
        f"{SOURCE_LOG} must end with exactly one newline character."
    )
    assert not content.endswith("\n\n"), (
        f"{SOURCE_LOG} ends with more than one newline character."
    )


@pytest.mark.parametrize("path", [CRITICAL_LOG, COUNT_FILE, COMMANDS_FILE])
def test_output_files_do_not_exist_yet(path: Path):
    """
    The artefacts that students are supposed to create should *not* be present
    before they run their solution.
    """
    assert not path.exists(), (
        f"File {path} already exists, but it should be created by the student."
    )