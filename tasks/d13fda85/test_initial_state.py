# test_initial_state.py
#
# This test-suite verifies the **initial** filesystem state
# before the student carries out any work.  It intentionally
# makes **no reference** to the output directory or files that
# the student is expected to create later.

import os
import stat
from pathlib import Path
import re
import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
LOG_FILES = [
    LOGS_DIR / "auth.log.2023-07-17",
    LOGS_DIR / "auth.log.2023-07-18",
    LOGS_DIR / "auth.log.2023-07-19",
]

FAILED_RE = re.compile(r"^.*sshd\[.*\]:\ Failed\ password")


def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) for *path*."""
    return stat.S_IMODE(path.stat().st_mode)


def _assert_permission(path: Path, expected: int):
    """Assert that *path* has exactly *expected* permission bits."""
    actual = _mode(path)
    assert actual == expected, (
        f"{path} permissions are {oct(actual)}, expected {oct(expected)}"
    )


def test_logs_directory_exists_and_has_correct_permissions():
    assert LOGS_DIR.exists(), f"Required directory {LOGS_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
    # Mode should be at least 0o755 (rwxr-xr-x).  Allow more permissive bits
    # such as the sticky bit but disallow more restrictive ones.
    mode = _mode(LOGS_DIR)
    required_bits = 0o755
    missing_bits = required_bits & ~mode
    assert (
        missing_bits == 0
    ), f"{LOGS_DIR} permissions ({oct(mode)}) are too restrictive; must include {oct(required_bits)}."


@pytest.mark.parametrize("log_path", LOG_FILES)
def test_log_file_exists_and_is_regular_file(log_path: Path):
    assert log_path.exists(), f"Log file {log_path} is missing."
    assert log_path.is_file(), f"{log_path} exists but is not a regular file."


@pytest.mark.parametrize("log_path", LOG_FILES)
def test_log_file_permission_bits_are_0644(log_path: Path):
    _assert_permission(log_path, 0o644)


@pytest.mark.parametrize(
    ("log_path", "expected_fail_count"),
    [
        (LOG_FILES[0], 3),
        (LOG_FILES[1], 3),
        (LOG_FILES[2], 4),
    ],
)
def test_each_log_contains_expected_failed_login_count(log_path: Path, expected_fail_count: int):
    """
    Ensure each log file contains exactly the expected number of lines
    that match the Failed-password pattern.  This guarantees the fixtures
    are in place and have not been tampered with.
    """
    with log_path.open("r", encoding="utf-8") as fh:
        failures = [ln for ln in fh if FAILED_RE.match(ln)]
    assert (
        len(failures) == expected_fail_count
    ), f"{log_path} should contain {expected_fail_count} failed login lines, found {len(failures)}."