# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student performs any actions.  It deliberately avoids checking
# for the presence of the output directory or files that the student is
# expected to create later.

import os
import stat
import pytest

LOG_DIR = "/home/user/api_test/logs"
LOG_FILE = "/home/user/api_test/logs/api_responses_20240314.log"

EXPECTED_LOG_DIR_PERMS = 0o755  # rwxr-xr-x
EXPECTED_LOG_FILE_PERMS = 0o644  # rw-r--r--

EXPECTED_LINES = [
    "2024-03-14T07:21:01Z,GET,/users,200,115ms",
    "2024-03-14T07:22:45Z,POST,/login,201,89ms",
    "2024-03-14T07:23:50Z,DELETE,/users/42,204,102ms",
    "2024-03-14T07:24:30Z,GET,/reports,500,321ms",
    "2024-03-14T07:25:10Z,PUT,/users/42,404,78ms",
]


def _human_mode(mode: int) -> str:
    """Convert a numeric permission (e.g., 0o755) to a human-readable string."""
    return oct(mode)


def test_logs_directory_exists_with_correct_permissions():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR} does not exist or is not a directory."
    )
    mode = stat.S_IMODE(os.stat(LOG_DIR).st_mode)
    assert (
        mode == EXPECTED_LOG_DIR_PERMS
    ), (
        f"Directory {LOG_DIR} should have permissions "
        f"{_human_mode(EXPECTED_LOG_DIR_PERMS)} but has {_human_mode(mode)}."
    )


def test_log_file_exists_with_correct_permissions():
    assert os.path.isfile(LOG_FILE), f"Required log file {LOG_FILE} does not exist."
    mode = stat.S_IMODE(os.stat(LOG_FILE).st_mode)
    assert (
        mode == EXPECTED_LOG_FILE_PERMS
    ), (
        f"Log file {LOG_FILE} should have permissions "
        f"{_human_mode(EXPECTED_LOG_FILE_PERMS)} but has {_human_mode(mode)}."
    )


def test_log_file_has_expected_content_and_format():
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        data = fp.read()

    # Ensure the file ends with a single trailing newline (LF)
    assert data.endswith(
        "\n"
    ), f"{LOG_FILE} must terminate with a single newline (LF)."

    # Remove the trailing newline for comparison
    lines = data.rstrip("\n").split("\n")

    assert len(lines) == 5, (
        f"{LOG_FILE} should contain exactly 5 data lines; found {len(lines)}."
    )

    assert lines == EXPECTED_LINES, (
        f"Contents of {LOG_FILE} do not match the expected data.\n"
        f"Expected:\n{EXPECTED_LINES!r}\nFound:\n{lines!r}"
    )

    # Extra sanity check: every line has exactly 5 comma-separated columns.
    for idx, line in enumerate(lines, start=1):
        cols = line.split(",")
        assert len(cols) == 5, (
            f"Line {idx} of {LOG_FILE!r} should have 5 comma-separated columns "
            f"but has {len(cols)}: {line!r}"
        )