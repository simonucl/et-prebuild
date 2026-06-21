# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student begins working on the exercise.  It checks only the
# files and directories that must already exist, **not** any that the student
# is expected to create later.

import os
import stat
import pytest

HOME = '/home/user'
LOG_DIR = os.path.join(HOME, 'logs')
OUT_DIR = os.path.join(HOME, 'output')
RAW_LOG = os.path.join(LOG_DIR, 'ping_results.log')

EXPECTED_LOG_LINES = [
    "2023-04-01T12:00:01Z|router1|8.8.8.8|24|reachable",
    "2023-04-01T12:05:01Z|router1|1.1.1.1|25|reachable",
    "2023-04-01T12:10:01Z|router1|8.8.4.4|27|reachable",
    "2023-04-01T12:15:01Z|router1|208.67.222.222|-|unreachable",
    "2023-04-01T12:20:01Z|router1|8.8.8.8|26|reachable",
    "2023-04-01T12:25:01Z|router1|1.1.1.1|-|unreachable",
    "2023-04-01T12:30:01Z|router1|8.8.4.4|29|reachable",
    "2023-04-01T12:35:01Z|router1|208.67.222.222|28|reachable",
]


def _mode(path):
    "Return the permission bits (e.g. 0o755) for the given path."
    return stat.S_IMODE(os.stat(path).st_mode)


# --------------------------------------------------------------------------- #
# Directories
# --------------------------------------------------------------------------- #
def test_logs_directory_exists_and_has_correct_permissions():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR!r} is missing.  "
        "It must exist prior to the exercise."
    )
    expected = 0o755  # rwxr-xr-x
    actual = _mode(LOG_DIR)
    assert actual == expected, (
        f"Directory {LOG_DIR!r} has permissions {oct(actual)}, "
        f"but should be {oct(expected)} (rwxr-xr-x)."
    )


def test_output_directory_exists_empty_and_has_correct_permissions():
    assert os.path.isdir(OUT_DIR), (
        f"Required directory {OUT_DIR!r} is missing.  "
        "Create it before starting the task."
    )

    expected = 0o775  # rwxrwxr-x
    actual = _mode(OUT_DIR)
    assert actual == expected, (
        f"Directory {OUT_DIR!r} has permissions {oct(actual)}, "
        f"but should be {oct(expected)} (rwxrwxr-x)."
    )

    contents = os.listdir(OUT_DIR)
    assert contents == [], (
        f"Directory {OUT_DIR!r} is expected to be empty initially, "
        f"but currently contains: {contents}"
    )


# --------------------------------------------------------------------------- #
# Raw probe log
# --------------------------------------------------------------------------- #
def test_raw_ping_log_exists_and_has_correct_permissions():
    assert os.path.isfile(RAW_LOG), (
        f"Required log file {RAW_LOG!r} is missing."
    )

    expected = 0o644  # rw-r--r--
    actual = _mode(RAW_LOG)
    assert actual == expected, (
        f"File {RAW_LOG!r} has permissions {oct(actual)}, "
        f"but should be {oct(expected)} (rw-r--r--)."
    )


def test_raw_ping_log_has_exact_expected_content_and_line_endings():
    # Read as bytes to make sure there are no CR characters.
    with open(RAW_LOG, "rb") as fh:
        data = fh.read()

    assert b"\r" not in data, (
        f"File {RAW_LOG!r} must use Unix LF line endings only; "
        "found carriage-return characters."
    )

    # Decode after CR check.
    text = data.decode("utf-8")
    lines = text.split("\n")

    # If the file ends with a trailing newline, split() will give an extra
    # empty string at the end — remove it.
    if lines and lines[-1] == "":
        lines.pop()

    assert lines == EXPECTED_LOG_LINES, (
        f"File {RAW_LOG!r} does not contain the expected eight probe records "
        "in the correct order.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual:\n"
        + "\n".join(lines)
    )