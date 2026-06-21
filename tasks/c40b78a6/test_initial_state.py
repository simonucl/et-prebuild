# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “Generate a Compliance-Ready Cross-Service ERROR Audit Trail”
# exercise.  These tests are executed **before** the student performs any
# work, therefore they MUST fail if the environment has already been
# modified (e.g. if /home/user/audit or the audit file already exist).
#
# Requirements verified:
#   • All three source log files exist and are readable.
#   • Each source log file still contains its expected contents.
#   • Exactly six ERROR entries (two per service) are present in total.
#   • The audit directory (/home/user/audit) and the target audit file
#     do *not* yet exist.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "distributed" / "logs"
AUDIT_DIR = HOME / "audit"
AUDIT_FILE = AUDIT_DIR / "audit_trail_20230815.log"

# --------------------------------------------------------------------------- #
# Expected, canonical contents of each source log file.                       #
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENT = {
    LOG_DIR / "auth-service.log": """\
2023-08-15T09:05:23Z INFO AuthService Started
2023-08-15T09:06:10Z ERROR AuthService FailedLogin user=john
2023-08-15T09:08:45Z WARN AuthService TokenNearExpiry user=anna
2023-08-15T10:15:00Z ERROR AuthService TokenValidationError tokenId=abc123
""",
    LOG_DIR / "payment-service.log": """\
2023-08-15T09:07:00Z INFO PaymentService Started
2023-08-15T09:10:12Z ERROR PaymentService PaymentDeclined order=4938
2023-08-15T09:11:59Z INFO PaymentService PaymentAccepted order=4939
2023-08-15T10:02:34Z ERROR PaymentService CurrencyMismatch expected=USD got=EUR
""",
    LOG_DIR / "inventory-service.log": """\
2023-08-15T08:55:12Z INFO InventoryService Started
2023-08-15T09:12:10Z ERROR InventoryService OutOfStock sku=8821
2023-08-15T09:20:33Z WARN InventoryService SlowResponse time=1200ms
2023-08-15T10:25:44Z ERROR InventoryService DBConnectionLost host=db1
""",
}

# Helper ---------------------------------------------------------------------


def read_file(path: Path) -> str:
    """Return the full text of *path* with universal newline handling."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n")


# Tests ----------------------------------------------------------------------


@pytest.mark.parametrize("log_path", EXPECTED_LOG_CONTENT.keys())
def test_log_file_exists_and_readable(log_path: Path):
    """Verify that each log file exists, is a regular file, and is readable."""
    assert log_path.exists(), f"Expected log file not found: {log_path}"
    assert log_path.is_file(), f"Path exists but is not a file: {log_path}"
    # Posix read permission for the owner is sufficient here.
    mode = log_path.stat().st_mode
    assert bool(mode & stat.S_IRUSR), f"Log file is not readable: {log_path}"


@pytest.mark.parametrize("log_path, expected_text", EXPECTED_LOG_CONTENT.items())
def test_log_file_contents_are_untouched(log_path: Path, expected_text: str):
    """
    Ensure that every log file still contains the exact, canonical
    text provided at the start of the exercise.  This guards against
    accidental in-place edits by the student.
    """
    actual = read_file(log_path)
    assert (
        actual == expected_text
    ), f"Contents of {log_path} have changed. Do not modify the source logs."


def test_total_error_lines_is_exactly_six():
    """
    Confirm that across the three source logs there are exactly six lines
    that include ' ERROR ' (note the surrounding spaces to avoid over-matching).
    """
    error_lines = []
    for log_path in EXPECTED_LOG_CONTENT.keys():
        for line in read_file(log_path).splitlines():
            if " ERROR " in line:
                error_lines.append((log_path.name, line))
    assert (
        len(error_lines) == 6
    ), f"Expected 6 ERROR records, found {len(error_lines)}:\n" + "\n".join(
        f"{fname}: {ln}" for fname, ln in error_lines
    )


def test_audit_directory_does_not_yet_exist():
    """
    The audit directory must *not* exist before the student has
    generated the report.  Its presence would mean the starting
    environment is already altered.
    """
    assert not AUDIT_DIR.exists(), (
        f"The directory {AUDIT_DIR} already exists; initial state should "
        "contain only the source log files.  Remove it before starting."
    )


def test_audit_file_does_not_yet_exist():
    """
    Similarly, the final audit file must not pre-exist—we are validating
    the *initial* state.
    """
    assert not AUDIT_FILE.exists(), (
        f"The file {AUDIT_FILE} is present, but it should be created "
        "by the student later in the exercise."
    )