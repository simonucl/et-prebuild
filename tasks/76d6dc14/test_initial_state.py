# test_initial_state.py
"""
Pytest suite that verifies the initial filesystem state for the
“log-monitoring” exercise *before* the student performs any action.

What is checked:
1. /home/user/logs/app.log
   • The file exists.
   • Its exact byte content matches the exercise’s truth data.
   • It contains precisely the three alert lines the student is later
     expected to extract, in the correct order.
2. /home/user/alerts/critical_errors.log
   • Must NOT exist yet (the student has not created it).
3. /home/user/alerts directory
   • May or may not exist; we only assert that, if it exists, the target
     file is still absent.

Only stdlib + pytest are used.
"""

from pathlib import Path
import re
import pytest

# ---- constants -------------------------------------------------------------

APP_LOG_PATH = Path("/home/user/logs/app.log")
ALERTS_DIR = Path("/home/user/alerts")
ALERTS_FILE = ALERTS_DIR / "critical_errors.log"

EXPECTED_APP_LOG_CONTENT = (
    "2024-06-01 10:12:33 INFO User login succeeded\n"
    "2024-06-01 10:15:41 ERROR 404 Page not found\n"
    "2024-06-01 10:17:02 WARNING Disk space low\n"
    "2024-06-01 10:20:11 CRITICAL Database connection lost\n"
    "2024-06-01 10:25:59 ERROR 500 Internal server error\n"
    "2024-06-01 10:30:12 INFO Scheduled backup completed\n"
    "2024-06-01 10:35:44 ERROR 502 Bad gateway\n"
    "2024-06-01 10:40:23 DEBUG Cache cleared\n"
)

# Lines that should be matched later by the student, in order.
EXPECTED_ALERT_LINES = [
    "2024-06-01 10:20:11 CRITICAL Database connection lost",
    "2024-06-01 10:25:59 ERROR 500 Internal server error",
    "2024-06-01 10:35:44 ERROR 502 Bad gateway",
]

# Compiled regex patterns as specified in the task description.
PATTERNS = [
    re.compile(r"CRITICAL"),
    re.compile(r"ERROR 5[0-9]{2}"),
]


# ---- helpers ---------------------------------------------------------------

def _read_app_log():
    """Read /home/user/logs/app.log as text (UTF-8)."""
    return APP_LOG_PATH.read_text(encoding="utf-8")


def _extract_alert_lines(text):
    """Return a list of lines that match either alert pattern."""
    lines = text.rstrip("\n").split("\n")
    matched = [
        line for line in lines
        if any(p.search(line) for p in PATTERNS)
    ]
    return matched


# ---- tests -----------------------------------------------------------------

def test_app_log_exists_and_content_is_exact():
    assert APP_LOG_PATH.exists(), (
        f"Required log file missing: {APP_LOG_PATH}"
    )
    assert APP_LOG_PATH.is_file(), (
        f"Expected a regular file at {APP_LOG_PATH}, "
        f"but found something else."
    )

    actual = _read_app_log()
    assert actual == EXPECTED_APP_LOG_CONTENT, (
        "The content of /home/user/logs/app.log does not match the "
        "expected truth data. Make sure the initial fixture is intact."
    )


def test_app_log_contains_expected_alert_lines_in_order():
    text = _read_app_log()
    matched = _extract_alert_lines(text)

    assert matched == EXPECTED_ALERT_LINES, (
        "The extracted alert lines from app.log are not exactly the ones "
        "expected by the exercise (either count/order/content mismatch). "
        f"Expected:\n{EXPECTED_ALERT_LINES!r}\nFound:\n{matched!r}"
    )
    assert len(matched) == 3, (
        "The number of alert lines expected in the source log is 3, "
        f"but {len(matched)} were found."
    )


def test_alerts_file_does_not_exist_yet():
    assert not ALERTS_FILE.exists(), (
        "The output file /home/user/alerts/critical_errors.log already exists, "
        "but it should **not** be present before the student runs their "
        "solution."
    )


def test_alerts_directory_state_is_allowed():
    # Merely ensure the directory, if it exists, is indeed a directory
    # (not some other kind of filesystem node). The student may have to
    # create it; its absence is therefore acceptable.
    if ALERTS_DIR.exists():
        assert ALERTS_DIR.is_dir(), (
            f"{ALERTS_DIR} exists but is not a directory."
        )