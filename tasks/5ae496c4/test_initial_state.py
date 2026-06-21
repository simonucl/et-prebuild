# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state is exactly as
# described in the task instructions *before* the student executes any command.
# It deliberately avoids checking for any of the OUTPUT artefacts that will be
# produced later (e.g. error_summary.log or CHANGELOG.md) in accordance with the
# grading-suite rules.

from pathlib import Path
import pytest

APP_ROOT = Path("/home/user/app")
VERSION_FILE = APP_ROOT / "VERSION"
LOG_DIR = APP_ROOT / "logs"
APP_LOG_FILE = LOG_DIR / "app.log"

EXPECTED_VERSION_CONTENT = "2.5.6\n"
EXPECTED_LOG_LINES = [
    "[2024-05-15 10:12:34] INFO: Service started\n",
    "[2024-05-15 10:12:35] ERROR: Unable to connect to database\n",
    "[2024-05-15 10:12:36] WARN: Retrying connection\n",
    "[2024-05-15 10:12:37] ERROR: Connection timed out\n",
    "[2024-05-15 10:12:40] INFO: Shutdown complete\n",
]


def test_app_directory_exists():
    """The application root directory must be present."""
    assert APP_ROOT.exists(), f"Expected directory {APP_ROOT} to exist."
    assert APP_ROOT.is_dir(), f"Expected {APP_ROOT} to be a directory."


def test_version_file_contents():
    """The VERSION file must exist and contain exactly '2.5.6\\n'."""
    assert VERSION_FILE.exists(), f"Expected file {VERSION_FILE} to exist."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} is not a regular file."

    content = VERSION_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_VERSION_CONTENT
    ), (
        "VERSION file content mismatch.\n"
        f"Expected: {repr(EXPECTED_VERSION_CONTENT)}\n"
        f"Found   : {repr(content)}"
    )


def test_logs_directory_and_app_log_file_contents():
    """The logs directory and the app.log file must exist with the expected lines."""
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."

    assert APP_LOG_FILE.exists(), f"Expected log file {APP_LOG_FILE} to exist."
    assert APP_LOG_FILE.is_file(), f"{APP_LOG_FILE} is not a regular file."

    actual_lines = APP_LOG_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    assert (
        actual_lines == EXPECTED_LOG_LINES
    ), (
        "app.log content mismatch.\n"
        "Expected lines:\n"
        + "".join(EXPECTED_LOG_LINES)
        + "\nActual lines:\n"
        + "".join(actual_lines)
    )