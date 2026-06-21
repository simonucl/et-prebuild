# test_initial_state.py
"""
Pytest suite to validate the initial state of the operating system / filesystem
BEFORE the student performs any actions for the log-processing task.

What we assert:
1. The logs directory /home/user/logs exists and is a directory.
2. The file /home/user/logs/app.log exists and is readable.
3. The log file contains exactly 7 non-empty lines.
4. Each line conforms to the “TIMESTAMP LEVEL MESSAGE” structure where
   LEVEL ∈ {INFO, WARN, ERROR}.
5. Exactly two lines have LEVEL == "ERROR".

We intentionally do NOT test for the presence or absence of any files the
student is expected to create later (e.g. debug.db, error_summary.log).
"""
import os
import re
import stat
import pytest

LOG_DIR = "/home/user/logs"
APP_LOG = os.path.join(LOG_DIR, "app.log")


def test_logs_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR} is missing. "
        "Make sure the log directory is in place before starting the task."
    )
    # Optional: ensure we can at least list it
    try:
        os.listdir(LOG_DIR)
    except PermissionError as exc:
        pytest.fail(f"Cannot access {LOG_DIR}: {exc}")


def test_app_log_exists_and_readable():
    assert os.path.isfile(APP_LOG), (
        f"Required log file {APP_LOG} is missing."
    )
    st = os.stat(APP_LOG)
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"Log file {APP_LOG} is not readable."
    )


def _read_log_lines():
    with open(APP_LOG, "r", encoding="utf-8") as fh:
        # Use splitlines() so we ignore the trailing newline, if any.
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]
    return lines


def test_app_log_line_count():
    lines = _read_log_lines()
    assert len(lines) == 7, (
        f"{APP_LOG} should contain exactly 7 non-empty lines; found {len(lines)}."
    )


# A simple, compiled regex for a timestamp followed by a level word and a message.
_LINE_REGEX = re.compile(
    r"""
    ^                       # start of line
    \d{4}-\d{2}-\d{2}       # YYYY-MM-DD
    \s+
    \d{2}:\d{2}:\d{2}       # HH:MM:SS
    \s+
    (INFO|WARN|ERROR)       # capture the level
    \s+
    .+                      # the remainder of the message
    $                       # end of line
    """,
    re.VERBOSE,
)


def test_app_log_content_and_error_count():
    lines = _read_log_lines()

    levels = []
    for idx, line in enumerate(lines, start=1):
        match = _LINE_REGEX.match(line)
        assert match, (
            f"Line {idx} in {APP_LOG!r} does not match the expected format:\n{line!r}"
        )
        levels.append(match.group(1))

    # Ensure only allowed levels are present (regex already restricts them, but be explicit).
    allowed = {"INFO", "WARN", "ERROR"}
    unexpected = set(levels) - allowed
    assert not unexpected, (
        f"Unexpected log levels found in {APP_LOG}: {unexpected}"
    )

    error_count = sum(1 for lvl in levels if lvl == "ERROR")
    assert error_count == 2, (
        f"{APP_LOG} should contain exactly 2 lines with level 'ERROR'; "
        f"found {error_count}."
    )