# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem / OS state
# is exactly as expected *before* the student performs any action.

import os
from pathlib import Path
import stat
import pytest

RAW_LOG = Path("/home/user/release/logs/deploy-2023-10-01.log")
FILTERED_DIR = Path("/home/user/release/filtered")
FILTERED_FILE = FILTERED_DIR / "payment-errors.log"

EXPECTED_RAW_LOG_LINES = [
    "2023-10-01T02:15:43Z [INFO] [user-service] Deployed successfully\n",
    "2023-10-01T02:17:01Z [ERROR] [payment-service] NullPointer exception at PaymentProcessor.java:87\n",
    "2023-10-01T02:18:22Z [WARN] [inventory-service] Slow response detected\n",
    "2023-10-01T02:19:55Z [ERROR] [payment-service] Timeout while contacting bank API\n",
    "2023-10-01T02:20:01Z [INFO] [payment-service] Health check passed\n",
]


def _octal_permissions(mode: int) -> int:
    """
    Return the permission bits (e.g., 0o644) from st_mode.
    """
    return stat.S_IMODE(mode)


def test_raw_log_file_exists():
    """
    The raw log file must exist at the exact path specified.
    """
    assert RAW_LOG.is_file(), (
        f"Expected raw log file at {RAW_LOG} was not found. "
        "Ensure the file exists before students begin work."
    )


def test_raw_log_file_permissions():
    """
    The raw log file must be world-readable (at least 0o644).
    """
    mode = _octal_permissions(RAW_LOG.stat().st_mode)
    assert mode & 0o400, f"{RAW_LOG} is not readable by the owner (mode: {oct(mode)})"
    assert mode & 0o040, f"{RAW_LOG} is not readable by the group (mode: {oct(mode)})"
    assert mode & 0o004, f"{RAW_LOG} is not world-readable (mode: {oct(mode)})"


def test_raw_log_file_contents():
    """
    The raw log file must contain exactly the five expected lines
    (each ending with a single newline).
    """
    with RAW_LOG.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert (
        lines == EXPECTED_RAW_LOG_LINES
    ), "Raw log file contents do not match the expected initial state."

    # Guard against missing final newline or extra blank lines
    for line in lines:
        assert line.endswith(
            "\n"
        ), "Every line in the raw log must end with a single newline character."


def test_filtered_directory_absent_initially():
    """
    The /home/user/release/filtered/ directory should *not* exist yet.
    Creating it is part of the student's task.
    If it does exist, ensure it does NOT already contain the target file.
    """
    if FILTERED_DIR.exists():
        # If the directory is pre-created for any reason, the target file
        # still must not exist.
        assert not FILTERED_FILE.exists(), (
            f"{FILTERED_FILE} already exists before the task begins. "
            "The student should create this file themselves."
        )
    else:
        # Directory itself should ideally be absent.
        assert not FILTERED_DIR.exists(), (
            f"{FILTERED_DIR} unexpectedly exists before the task begins."
        )