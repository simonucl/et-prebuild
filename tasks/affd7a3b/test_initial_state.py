# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state for the
# “access-control policy” exercise is correct.  It checks ONLY the
# presence and exact content of the supplied log file.  It intentionally
# avoids touching or asserting on any of the output paths the student is
# expected to create later, in accordance with the grading rules.

import difflib
from pathlib import Path

import pytest


LOG_PATH = Path("/home/user/simulated_logs/auth-service.log")

# Exact log content that must be present *including* the trailing newline.
EXPECTED_LOG_CONTENT = (
    "[2023-09-01 12:00:00] INFO  User login succeeded: user=jdoe   ip=192.168.0.10\n"
    "[2023-09-01 12:01:00] WARN  User login failed:    user=jdoe   ip=192.168.0.10\n"
    "[2023-09-01 12:02:00] WARN  User login failed:    user=jdoe   ip=192.168.0.10\n"
    "[2023-09-01 12:03:00] WARN  User login failed:    user=alice  ip=10.0.0.5\n"
    "[2023-09-01 12:04:00] INFO  User login succeeded: user=alice  ip=10.0.0.5\n"
    "[2023-09-01 12:05:00] WARN  User login failed:    user=bob    ip=172.16.1.3\n"
    "[2023-09-01 12:06:00] WARN  User login failed:    user=bob    ip=172.16.1.3\n"
    "[2023-09-01 12:07:00] WARN  User login failed:    user=bob    ip=172.16.1.3\n"
    "[2023-09-01 12:08:00] DEBUG Heartbeat check ok\n"
    "[2023-09-01 12:09:00] WARN  User login failed:    user=charlie ip=192.168.0.20\n"
)


@pytest.fixture(scope="module")
def log_contents():
    """
    Read and return the contents of the log file.

    The fixture will fail fast if the path is missing or not a regular file,
    so individual tests do not have to duplicate those checks.
    """
    if not LOG_PATH.exists():
        pytest.fail(
            f"Required log file {LOG_PATH} is missing. "
            "The exercise cannot be started without it."
        )
    if not LOG_PATH.is_file():
        pytest.fail(
            f"{LOG_PATH} exists but is not a regular file. "
            "Please restore the correct log file."
        )
    try:
        return LOG_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {LOG_PATH}: {exc}")


def test_log_file_exact_match(log_contents):
    """
    Ensure the supplied log file matches the expected golden content exactly.
    """
    if log_contents != EXPECTED_LOG_CONTENT:
        diff = "\n".join(
            difflib.unified_diff(
                EXPECTED_LOG_CONTENT.splitlines(),
                log_contents.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(
            "The content of the log file does not match the expected fixture. "
            "See diff below:\n" + diff
        )


def test_log_file_has_trailing_newline(log_contents):
    """
    Verify the file ends with a single trailing newline, as required.
    """
    assert log_contents.endswith(
        "\n"
    ), f"{LOG_PATH} must end with exactly one newline character."


def test_log_directory_exists():
    """
    Confirm the parent directory of the log exists and is a directory.
    """
    parent = LOG_PATH.parent
    assert parent.is_dir(), f"Expected directory {parent} is missing."