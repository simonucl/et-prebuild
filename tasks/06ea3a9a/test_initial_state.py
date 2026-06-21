# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student starts working on the task.  It checks that the
# three expected log files already exist in /home/user/logs/ and that
# their contents match the specification exactly (byte-for-byte,
# including trailing newlines).  No assertions are made about any
# future output directories or files.

import pathlib
import pytest

LOG_DIR = pathlib.Path("/home/user/logs")

# ---------------------------------------------------------------------------
# Helper: expected contents of each log file (including the trailing newline)
# ---------------------------------------------------------------------------
EXPECTED_LOGS = {
    "node1.log": (
        "[2024-04-24 12:00:00] INFO  Starting training epoch 1\n"
        "[2024-04-24 12:00:01] ERROR Loss became NaN\n"
        "[2024-04-24 12:00:02] ERROR Gradient explosion detected\n"
        "[2024-04-24 12:00:03] INFO  Retrying with smaller learning rate\n"
    ),
    "node2.log": (
        "[2024-04-24 12:00:00] INFO  Starting training epoch 1\n"
        "[2024-04-24 12:00:05] ERROR Out of memory\n"
        "[2024-04-24 12:00:06] INFO  Swapped to CPU memory\n"
    ),
    "node3.log": (
        "[2024-04-24 12:00:00] INFO  Starting training epoch 1\n"
        "[2024-04-24 12:00:04] ERROR Gradient explosion detected\n"
        "[2024-04-24 12:00:05] ERROR Gradient explosion detected\n"
        "[2024-04-24 12:00:06] INFO  Adjusting gradient clipping\n"
    ),
}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_directory_exists():
    """The /home/user/logs directory must exist and be a directory."""
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.parametrize("log_name", sorted(EXPECTED_LOGS.keys()))
def test_log_file_exists(log_name):
    """Each expected log file must be present."""
    log_path = LOG_DIR / log_name
    assert log_path.exists(), f"Expected file {log_path} is missing."
    assert log_path.is_file(), f"{log_path} exists but is not a file."


@pytest.mark.parametrize("log_name,expected_content", EXPECTED_LOGS.items())
def test_log_file_contents_exact(log_name, expected_content):
    """
    Contents of each log file must match the specification exactly,
    including line endings and final trailing newline.
    """
    log_path = LOG_DIR / log_name
    actual_content = log_path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"Contents of {log_path} do not match the expected specification.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}\n"
    )