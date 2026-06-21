# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student runs any command.
#
# What we check:
#   • /home/user/rotation/            — must exist and be a directory (mode 755).
#   • /home/user/rotation/cred_rotation.log
#       – must exist, be a regular file (mode 644, UTF-8),
#       – must contain exactly nine specific lines (see EXPECTED_LINES),
#       – every line in the file must end with '\n' **and never '\r\n'**.
#
# We explicitly DO NOT look for /home/user/rotation/successful_rotations.log
# (that is an output artefact created *after* the student’s command).
#
# Only the Python stdlib and pytest are used.

import os
import stat
import difflib
from pathlib import Path

import pytest

ROTATION_DIR = Path("/home/user/rotation")
CRED_LOG = ROTATION_DIR / "cred_rotation.log"

EXPECTED_LINES = [
    "[2023-11-01 09:13:02] Rotated credential for user alice status=SUCCESS",
    "[2023-11-01 09:15:48] Rotated credential for user bob status=FAIL",
    "[2023-11-01 09:17:31] Rotated credential for user charlie status=SUCCESS",
    "[2023-11-01 09:18:20] Manual update for user dave",
    "[2023-11-02 10:22:11] Rotated credential for user dave status=SUCCESS",
    "[2023-11-02 10:25:46] Rotated credential for user eve status=FAIL",
    "[2023-11-02 10:29:50] Rotated credential for user frank status=SUCCESS",
    "[2023-11-02 10:35:59] Backup completed",
    "[2023-11-02 11:00:01] Rotated credential for user grace status=SUCCESS",
]


def _assert_mode(path: Path, expected_mode: int):
    """
    Helper that asserts the lowest 3 octal permission bits (e.g. 0o755) match.
    """
    actual_mode = path.stat().st_mode & 0o777
    assert (
        actual_mode == expected_mode
    ), f"{path} permissions expected {oct(expected_mode)} but are {oct(actual_mode)}"


def _read_file_lines(path: Path):
    """
    Reads a text file in UTF-8, returns:
      • list of lines *without* the trailing newline,
      • original raw bytes to allow CRLF checks.
    """
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    return text.splitlines(), raw


def _diff(expected, actual):
    """
    Returns a unified diff string between two lists of strings.
    """
    diff = difflib.unified_diff(
        expected,
        actual,
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    return "\n".join(diff)


@pytest.mark.order(1)
def test_rotation_directory_exists_and_has_correct_mode():
    assert ROTATION_DIR.exists(), f"Directory {ROTATION_DIR} is missing."
    assert ROTATION_DIR.is_dir(), f"{ROTATION_DIR} exists but is not a directory."
    _assert_mode(ROTATION_DIR, 0o755)


@pytest.mark.order(2)
def test_cred_rotation_log_exists_and_has_correct_mode():
    assert CRED_LOG.exists(), f"File {CRED_LOG} is missing."
    assert CRED_LOG.is_file(), f"{CRED_LOG} exists but is not a regular file."
    _assert_mode(CRED_LOG, 0o644)


@pytest.mark.order(3)
def test_cred_rotation_log_contents():
    lines, raw = _read_file_lines(CRED_LOG)

    # Basic length check
    assert len(lines) == len(
        EXPECTED_LINES
    ), f"{CRED_LOG} should contain {len(EXPECTED_LINES)} lines but has {len(lines)}."

    # Content check
    if lines != EXPECTED_LINES:
        diff_msg = _diff(EXPECTED_LINES, lines)
        pytest.fail(f"Content of {CRED_LOG} does not match expected lines.\nDiff:\n{diff_msg}")

    # Newline style check – ensure '\n' but not '\r\n'
    assert b"\r\n" not in raw, f"{CRED_LOG} must use Unix line endings ('\\n'), not Windows CRLF ('\\r\\n')."
    # Ensure the file ends with a newline (last byte is '\n')
    assert raw.endswith(
        b"\n"
    ), f"The last line in {CRED_LOG} must end with a newline character ('\\n')."