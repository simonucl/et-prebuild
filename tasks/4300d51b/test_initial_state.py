# test_initial_state.py
"""
Pytest suite to validate the operating-system state *before* the student’s
solution is run.

Checks performed:
1. /home/user/qa_logs exists and is a directory.
2. /home/user/qa_logs/application.log exists and contains exactly the 10
   expected lines (each terminated by '\n').
3. No other files are present in /home/user/qa_logs at this stage.

Only the standard library and pytest are used.
"""

from pathlib import Path
import pytest

QA_DIR = Path("/home/user/qa_logs")
APP_LOG = QA_DIR / "application.log"

EXPECTED_LINES = [
    "2024-06-01 10:00:00 [INFO] Starting application\n",
    "2024-06-01 10:00:01 [DEBUG] Initializing modules\n",
    "2024-06-01 10:00:02 [WARN] Deprecated API used\n",
    "2024-06-01 10:00:03 [INFO] Module A ready\n",
    "2024-06-01 10:00:04 [ERROR] Null pointer exception\n",
    "2024-06-01 10:00:05 [WARN] Low disk space\n",
    "2024-06-01 10:00:06 [DEBUG] Cache cleared\n",
    "2024-06-01 10:00:07 [ERROR] Out of memory\n",
    "2024-06-01 10:00:08 [INFO] Shutdown requested\n",
    "2024-06-01 10:00:09 [WARN] Configuration file missing\n",
]


def test_qa_logs_directory_exists():
    assert QA_DIR.exists(), f"Required directory {QA_DIR} does not exist."
    assert QA_DIR.is_dir(), f"{QA_DIR} exists but is not a directory."


def test_application_log_exists():
    assert APP_LOG.exists(), (
        f"Required log file {APP_LOG} does not exist. "
        "The exercise cannot be graded without it."
    )
    assert APP_LOG.is_file(), f"{APP_LOG} exists but is not a regular file."


def test_application_log_content():
    lines = APP_LOG.read_text(encoding="utf-8").splitlines(keepends=True)
    assert lines == EXPECTED_LINES, (
        f"{APP_LOG} does not contain the expected 10 lines or they are not in the "
        "correct order.\n"
        "Expected content:\n"
        + "".join(EXPECTED_LINES)
    )


def test_no_extra_files_present():
    """Ensure no other files are present before the student runs their solution."""
    files = sorted(p.name for p in QA_DIR.iterdir() if p.is_file())
    assert files == ["application.log"], (
        f"Unexpected files present in {QA_DIR}: {files}. "
        "Only 'application.log' should exist before execution."
    )