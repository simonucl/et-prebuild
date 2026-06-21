# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state is exactly as
# expected *before* the student performs any action.
#
# What we check:
#   • The directory /home/user/project/logs/ exists.
#   • Exactly three *.log files are present directly inside it:
#       - app.log
#       - db.log
#       - auth.log
#   • Each of those files contains the precise, line-by-line content specified
#     in the task description, including newline terminators.
#
# What we deliberately do NOT check:
#   • The presence of /home/user/project/docs/
#   • The presence of /home/user/project/docs/error_summary.txt
#
# If any assertion fails the error message will clearly indicate what is
# missing or incorrect.

from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/project")
LOG_DIR = BASE_DIR / "logs"

EXPECTED_LOG_FILES = {
    "app.log": [
        "INFO Application started\n",
        "WARN Cache miss\n",
        "ERROR Failed to load config\n",
        "INFO Shutdown complete\n",
    ],
    "db.log": [
        "INFO Connection established\n",
        "ERROR Query timeout\n",
        "ERROR Could not commit\n",
        "INFO Connection closed\n",
    ],
    "auth.log": [
        "INFO User login\n",
        "WARN Password attempt\n",
        "ERROR Invalid token\n",
        "ERROR Session expired\n",
        "ERROR Permission denied\n",
        "INFO Logout\n",
    ],
}

@pytest.fixture(scope="session")
def log_dir():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    return LOG_DIR


def test_exact_log_files_present(log_dir):
    """
    Ensure that exactly the expected three *.log files—and no others—are present
    directly inside /home/user/project/logs/.
    """
    present_logs = sorted(p.name for p in log_dir.iterdir() if p.is_file() and p.suffix == ".log")
    expected_logs = sorted(EXPECTED_LOG_FILES.keys())
    assert present_logs == expected_logs, (
        "Mismatch in .log files inside {dir}\n"
        "Expected: {exp}\n"
        "Found   : {found}".format(dir=log_dir, exp=expected_logs, found=present_logs)
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOG_FILES.items())
def test_log_file_contents(log_dir, filename, expected_lines):
    """
    Validate that each log file has exactly the expected content, line by line.
    """
    file_path = log_dir / filename
    assert file_path.exists(), f"Expected log file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    with file_path.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert lines == expected_lines, (
        f"Content mismatch for {file_path}.\n"
        f"Expected {len(expected_lines)} lines:\n{''.join(expected_lines)}\n"
        f"Found {len(lines)} lines:\n{''.join(lines)}"
    )


def test_total_error_line_count(log_dir):
    """
    Sanity-check: The total number of lines containing the exact string 'ERROR'
    across all *.log files must be 6.
    """
    total_errors = 0
    for path in log_dir.iterdir():
        if path.is_file() and path.suffix == ".log":
            with path.open(encoding="utf-8") as fp:
                total_errors += sum(1 for line in fp if "ERROR" in line)
    assert total_errors == 6, (
        f"Expected exactly 6 'ERROR' lines across all log files, found {total_errors}."
    )