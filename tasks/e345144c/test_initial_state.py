# test_initial_state.py
#
# Pytest suite to validate the initial, pre-task filesystem state
# for the “observability engineer” exercise.
#
# Rules verified:
#   • The synthetic application log is present and unmodified.
#   • The output directory and its two deliverables are NOT present yet.
#
# No third-party libraries are used—only stdlib + pytest.

import os
from pathlib import Path
import pytest

# Absolute paths used throughout the exercise
INPUT_LOG  = Path("/home/user/observability/input/app.log")
OUTPUT_DIR = Path("/home/user/observability/output")
ERROR_LOG  = OUTPUT_DIR / "2023-07-20_error.log"
COUNT_FILE = OUTPUT_DIR / "2023-07-20_error.count"

# Canonical contents of the input log at exercise start
EXPECTED_APP_LOG_LINES = [
    "2023-07-19 10:13:45,123 INFO  PaymentsService - Starting reconciliation",
    "2023-07-19 10:13:45,456 ERROR PaymentsService - Failed to reconcile invoice 8745",
    "2023-07-19 11:07:12,789 WARN  AuthService - Token expired for user 102",
    "2023-07-19 11:07:15,001 INFO  AuthService - Token refreshed for user 102",
    "2023-07-20 09:03:05,321 ERROR OrdersService - Order 5561 could not be processed",
    "2023-07-20 09:03:06,555 INFO  OrdersService - Retry queued for order 5561",
    "2023-07-20 12:47:17,678 ERROR InventoryService - Stock level mismatch for SKU 887",
    "2023-07-20 12:47:18,999 WARN  InventoryService - Retrying stock update",
    "2023-07-20 20:00:00,555 ERROR AuthService - Authentication DB unreachable",
    "2023-07-21 08:22:55,111 INFO  PaymentsService - Reconciliation complete",
    "2023-07-21 08:23:00,222 ERROR PaymentsService - Payment gateway timeout",
    "2023-07-21 14:15:42,333 INFO  OrdersService - Order 5561 processed successfully",
    "2023-07-21 14:16:42,444 ERROR OrdersService - Refund failed for order 5561",
]


@pytest.mark.dependency(name="input_log_present")
def test_input_log_exists():
    """The synthetic log file must exist before any student action."""
    assert INPUT_LOG.is_file(), (
        f"Expected input log file not found at {INPUT_LOG}. "
        "The exercise cannot proceed without it."
    )


@pytest.mark.dependency(depends=["input_log_present"], name="input_log_content")
def test_input_log_content_unchanged():
    """The input log must contain exactly the expected lines, in order."""
    with INPUT_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert actual_lines == EXPECTED_APP_LOG_LINES, (
        "The contents of the input log differ from the expected initial state.\n"
        f"Found {len(actual_lines)} lines, expected {len(EXPECTED_APP_LOG_LINES)}."
    )


def test_output_directory_absent():
    """
    The output directory should not exist yet (clean initial state).
    If it exists for some reason, it must not already contain the
    files the student is supposed to create.
    """
    if OUTPUT_DIR.exists():
        assert OUTPUT_DIR.is_dir(), (
            f"{OUTPUT_DIR} exists but is not a directory—unexpected state."
        )
        unexpected_files = [p for p in [ERROR_LOG, COUNT_FILE] if p.exists()]
        assert not unexpected_files, (
            "Output artefacts already present before any work was done: "
            + ", ".join(str(p) for p in unexpected_files)
        )
    else:
        # Directory absent, which is also acceptable for a clean slate.
        assert True


def test_output_files_do_not_exist():
    """Neither of the deliverable files should pre-exist."""
    for path in (ERROR_LOG, COUNT_FILE):
        assert not path.exists(), (
            f"Unexpected file present before task execution: {path}"
        )