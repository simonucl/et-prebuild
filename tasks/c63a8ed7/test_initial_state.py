# test_initial_state.py
#
# This pytest suite validates that the operating-system state is exactly
# what the exercise description promises *before* the student performs
# any action.  It deliberately avoids examining /home/user/reports or any
# other output locations the student is supposed to create.

import os
from pathlib import Path
import stat
import pytest

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "user_actions.log"

EXPECTED_LOG_LINES = [
    "2024-05-18 08:14:22 alice LOGIN",
    "2024-05-18 08:16:30 bob LOGIN",
    "2024-05-18 08:20:44 alice LOGOUT",
    "2024-05-18 09:01:07 charlie FAILED",
    "2024-05-18 09:02:12 diana LOGIN",
    "2024-05-18 09:05:55 charlie LOGIN",
    "2024-05-18 09:07:01 charlie LOGOUT",
    "2024-05-18 09:10:33 bob LOGOUT",
    "2024-05-18 09:11:11 edward LOGIN",
    "2024-05-18 09:15:00 frank FAILED",
]


def test_logs_directory_exists():
    """The directory /home/user/logs must exist and be a directory."""
    assert LOG_DIR.exists(), "/home/user/logs is missing."
    assert LOG_DIR.is_dir(), "/home/user/logs exists but is not a directory."


def test_logs_directory_permissions():
    """The /home/user/logs directory must have mode 0755."""
    mode = stat.S_IMODE(os.stat(LOG_DIR).st_mode)
    assert mode == 0o755, (
        f"/home/user/logs should have permissions 0755, "
        f"but has {oct(mode)} instead."
    )


def test_log_file_exists_and_is_regular():
    """The system log file must exist and be a regular file."""
    assert LOG_FILE.exists(), "/home/user/logs/user_actions.log is missing."
    assert LOG_FILE.is_file(), (
        "/home/user/logs/user_actions.log exists but is not a regular file."
    )


def test_log_file_contents_exact():
    """
    The log file must contain exactly the expected 10 lines, each terminated
    by a single LF, and nothing else.
    """
    # Read file as *binary* so we can verify trailing newline behaviour.
    data = LOG_FILE.read_bytes()
    # The file must end with exactly one LF and no extra blank lines
    assert data.endswith(b"\n"), (
        "/home/user/logs/user_actions.log must end with a single LF."
    )
    text = data.decode()
    # Removing the final '\n' because splitlines() below discards it.
    if text.endswith("\n"):
        text = text[:-1]
    actual_lines = text.split("\n")

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The content of /home/user/logs/user_actions.log does not match the "
        "expected initial state.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )


@pytest.mark.parametrize("line", EXPECTED_LOG_LINES)
def test_each_log_line_has_four_fields(line):
    """
    Each expected log line must consist of exactly four space-separated
    fields: date, time, username, and action.
    """
    parts = line.split()
    assert len(parts) == 4, f"Log line {line!r} does not have exactly 4 fields."