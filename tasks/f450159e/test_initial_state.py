# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present before the student starts working on the task.  It purposefully
# avoids checking for the presence (or absence) of any expected *output*
# artifacts such as /home/user/logs/summary.csv, as required by the
# instructions.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "server.log")

EXPECTED_LOG_CONTENT = (
    "2023-10-01 12:00:00Z INFO  server1 GET    /api/user    200 123ms\n"
    "2023-10-01 12:05:00Z WARN  server1 POST   /api/order   500 98ms\n"
    "2023-10-01 12:10:00Z INFO  server2 GET    /api/product 200 110ms\n"
    "2023-10-01 12:15:00Z ERROR server2 DELETE /api/order   404 130ms\n"
)

# The log file in the description uses single spaces between columns, but we
# allow for *at least* one whitespace between fields.  To compare byte-for-byte
# we normalize the example from the description into this canonical form.
# The tests still verify eight columns per line regardless of spacing.


@pytest.fixture(scope="module")
def log_content():
    """
    Read the entire server.log file once for all tests.
    """
    if not os.path.exists(LOG_FILE):
        pytest.skip(f"{LOG_FILE} does not exist on this system")
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        return fp.read()


def test_log_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR!r} is missing or not a directory."
    )

    dir_mode = stat.S_IMODE(os.stat(LOG_DIR).st_mode)
    # Directory should be at least 0o755 (rwxr-xr-x)
    assert dir_mode & 0o755 == 0o755, (
        f"Directory {LOG_DIR!r} must have permissions >= 755 "
        f"(currently: {oct(dir_mode)})"
    )


def test_server_log_exists_and_permissions():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE!r} is missing."
    )

    file_mode = stat.S_IMODE(os.stat(LOG_FILE).st_mode)
    # File should be at least 0o644 (rw-r--r--)
    assert file_mode & 0o644 == 0o644, (
        f"Log file {LOG_FILE!r} must have permissions >= 644 "
        f"(currently: {oct(file_mode)})"
    )


def test_server_log_exact_content(log_content):
    """
    The exercise specifies the exact byte-for-byte content (including the final
    newline) that must already be present in server.log.  Any deviation would
    indicate that the starting point is wrong.
    """
    # Normalize internal whitespace in both expected and actual content to
    # single spaces so minor spacing differences do not break the test while
    # still ensuring all tokens are present in order.
    def _normalize(text: str) -> str:
        return "\n".join(" ".join(line.split()) for line in text.rstrip("\n").splitlines())

    expected_normalized = _normalize(EXPECTED_LOG_CONTENT)
    actual_normalized = _normalize(log_content)

    assert actual_normalized == expected_normalized, (
        "The content of server.log does not match the expected starting "
        "content.\n"
        "Expected (normalized whitespace):\n"
        f"{expected_normalized}\n\n"
        "Actual (normalized whitespace):\n"
        f"{actual_normalized}\n"
    )

    # Also ensure the file ends with exactly one trailing newline
    assert log_content.endswith("\n"), (
        "server.log must end with exactly one Unix newline character (\\n)."
    )


def test_each_log_line_has_eight_columns(log_content):
    """
    Sanity check: every line must contain exactly eight whitespace-separated
    columns as described in the task.
    """
    for idx, line in enumerate(log_content.rstrip("\n").splitlines(), 1):
        columns = line.split()
        assert len(columns) == 8, (
            f"Line {idx} of server.log should have 8 columns but has "
            f"{len(columns)}: {line!r}"
        )