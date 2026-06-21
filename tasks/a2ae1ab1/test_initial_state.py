# test_initial_state.py
#
# This test-suite verifies that the operating-system / file-system
# is in the correct *initial* state before the student begins to
# process the log file.  It deliberately avoids checking for any
# artefacts that the student is expected to create (`api_errors_…`,
# `api_error_summary.txt`, etc.).
#
# Requirements verified:
#   • /home/user/logs directory exists and is a directory.
#   • /home/user/logs/api_integration.log exists, is a file, is readable,
#     and contains exactly the expected lines in exactly the expected order.
#
# Only stdlib + pytest are used.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "api_integration.log")

EXPECTED_LINES = [
    "2023-09-15T08:01:22Z GET /customers 200",
    "2023-09-15T08:01:23Z POST /orders 201",
    "2023-09-15T08:01:25Z GET /customers/42 404",
    "2023-09-15T08:01:27Z PATCH /customers/42 409",
    "2023-09-15T08:01:30Z GET /inventory 200",
    "2023-09-15T08:01:35Z GET /orders/310 500",
    "2023-09-15T08:01:36Z POST /payments 502",
    "2023-09-15T08:01:40Z GET /health 200",
    "2023-09-15T08:01:45Z DELETE /customers/42 204",
    "2023-09-15T08:01:50Z GET /customers/99 404",
    "2023-09-15T08:01:55Z POST /orders 503",
    "2023-09-15T08:01:59Z GET /analytics 401",
]


def test_log_directory_exists():
    assert os.path.exists(LOG_DIR), (
        f"Required directory {LOG_DIR} does not exist."
    )
    assert os.path.isdir(LOG_DIR), (
        f"{LOG_DIR} exists but is not a directory."
    )
    # Directory must be accessible (read & execute for traversal).
    st_mode = os.stat(LOG_DIR).st_mode
    assert bool(st_mode & stat.S_IRUSR), f"{LOG_DIR} is not readable by user."
    assert bool(st_mode & stat.S_IXUSR), f"{LOG_DIR} is not accessible by user (no execute bit)."


def test_api_integration_log_exists_and_readable():
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE} is missing or not a regular file."
    )
    # Check readability by actually opening it.
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as fp:
            first_line = fp.readline()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Log file {LOG_FILE} exists but could not be read: {exc!r}")

    assert first_line, (
        f"Log file {LOG_FILE} appears to be empty; expected at least one line."
    )


def test_api_integration_log_content_exact_match():
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        contents = fp.read()

    # Splitlines without keeping EOL characters;
    # this avoids newline-style differences while still requiring exact ordering.
    actual_lines = contents.rstrip("\n").splitlines()

    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "Contents of api_integration.log do not match the expected initial state.\n"
        "Differences:\n\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )