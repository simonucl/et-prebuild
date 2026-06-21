# test_initial_state.py
#
# This test-suite verifies that the **initial** operating-system / file-system
# state is correct *before* the student runs any command.  It checks only the
# existing log file and its parent directories; it deliberately ignores the
# yet-to-be-created `error_summary.txt` as required by the instructions.

import os
import pytest

# Absolute paths used throughout the verification.
LOG_DIR = "/home/user/projects/myapp/logs"
APP_LOG = os.path.join(LOG_DIR, "app.log")

# The exact lines expected inside app.log, in order.
EXPECTED_LOG_LINES = [
    "2024-05-30 12:00:01,001 INFO  Starting application\n",
    "2024-05-30 12:00:02,002 ERROR Failed to connect to database\n",
    "2024-05-30 12:00:03,003 WARN  Cache miss for key user_123\n",
    "2024-05-30 12:00:04,004 ERROR Null pointer exception in module XYZ\n",
    "2024-05-30 12:00:05,005 INFO  Processing request id=987\n",
    "2024-05-30 12:00:06,006 ERROR Timeout while contacting external API\n",
    "2024-05-30 12:00:07,007 DEBUG Retrying connection\n",
    "2024-05-30 12:00:08,008 ERROR Invalid credentials for user 'admin'\n",
    "2024-05-30 12:00:09,009 INFO  Shutdown sequence initiated\n",
    "2024-05-30 12:00:10,010 ERROR Unhandled exception in main loop\n",
]

@pytest.mark.dependency(name="dirs_exist")
def test_required_directories_exist():
    """
    Ensure that each directory in the absolute path to the log file exists.
    """
    current_path = "/"
    # Split the log directory into components and walk down verifying each.
    for part in LOG_DIR.strip("/").split("/"):
        current_path = os.path.join(current_path, part)
        assert os.path.isdir(current_path), (
            f"Required directory missing: {current_path!r}. "
            "The exercise expects this directory to be present before any action."
        )

@pytest.mark.dependency(name="app_log_exists", depends=["dirs_exist"])
def test_app_log_file_exists_and_is_regular():
    """
    The application log file must already be present and be a regular file.
    """
    assert os.path.isfile(APP_LOG), (
        f"Expected log file {APP_LOG!r} does not exist. "
        "The initial state must include this file."
    )
    # Extra guard: ensure it's not an empty file.
    assert os.path.getsize(APP_LOG) > 0, (
        f"Log file {APP_LOG!r} is unexpectedly empty."
    )

@pytest.mark.dependency(depends=["app_log_exists"])
def test_app_log_contents_are_exact():
    """
    Verify the exact number of lines, their order, their content, and that the
    file ends with exactly one trailing newline.
    """
    with open(APP_LOG, "r", encoding="utf-8") as fp:
        contents = fp.readlines()

    # 1) Exact number of lines.
    assert len(contents) == 10, (
        f"app.log should contain 10 lines, but {len(contents)} were found."
    )

    # 2) Exact text of each line (order & characters, including spaces).
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LOG_LINES, contents), start=1):
        assert actual == expected, (
            f"Mismatch on line {idx} of app.log.\n"
            f"Expected: {expected!r}\n"
            f"Found   : {actual!r}"
        )

    # 3) Ensure the file ends with exactly one newline, no extra blank lines.
    with open(APP_LOG, "rb") as fp:
        raw = fp.read()
    assert raw.endswith(b"\n"), "app.log must end with a single trailing newline."
    assert not raw.endswith(b"\n\n"), (
        "app.log ends with more than one trailing newline; only one is allowed."
    )

@pytest.mark.dependency(depends=["app_log_exists"])
def test_error_line_count_is_five():
    """
    Confirm that exactly five lines in the log contain the literal word 'ERROR'.
    """
    with open(APP_LOG, "r", encoding="utf-8") as fp:
        error_lines = [ln for ln in fp if "ERROR" in ln]

    assert len(error_lines) == 5, (
        f"app.log is expected to contain exactly 5 'ERROR' lines, "
        f"but {len(error_lines)} were found."
    )