# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the student performs any actions for the encoding–conversion
# exercise.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
REPORTS_DIR = HOME / "cloud" / "reports"
LOGS_DIR = HOME / "cloud" / "logs"

ISO_FILE = REPORTS_DIR / "monthly_cost_iso.csv"
UTF8_FILE = REPORTS_DIR / "monthly_cost_utf8.csv"
AUDIT_LOG = LOGS_DIR / "encoding_audit.log"


def test_reports_directory_exists():
    assert REPORTS_DIR.is_dir(), (
        f"Expected directory {REPORTS_DIR} to exist but it does not."
    )


def test_iso_file_exists():
    assert ISO_FILE.is_file(), (
        f"Expected source file {ISO_FILE} to exist but it is missing."
    )


def test_logs_directory_exists_and_is_empty():
    assert LOGS_DIR.is_dir(), (
        f"Expected directory {LOGS_DIR} to exist but it does not."
    )
    # Collect non-hidden items in the logs directory.
    residual_items = [p for p in LOGS_DIR.iterdir() if p.name not in {".", ".."}]
    assert residual_items == [], (
        f"{LOGS_DIR} should be empty before the task starts, "
        f"but found: {', '.join(str(p) for p in residual_items)}"
    )


def test_utf8_file_does_not_exist_yet():
    assert not UTF8_FILE.exists(), (
        f"{UTF8_FILE} should NOT exist before the student performs the conversion."
    )


def test_audit_log_does_not_exist_yet():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should NOT exist before the student writes the audit log."
    )


def test_iso_file_is_iso_8859_1_not_utf8():
    """
    Confirm that the initial CSV is encoded in ISO-8859-1 (Latin-1)
    and *not* in UTF-8.
    """
    data = ISO_FILE.read_bytes()

    # 1) The file must fail UTF-8 decoding (at least in strict mode).
    with pytest.raises(UnicodeDecodeError):
        data.decode("utf-8", errors="strict")

    # 2) It must successfully decode as Latin-1 and contain expected accented names.
    text_latin1 = data.decode("latin-1")
    expected_markers = ["José", "Zoë", "René"]
    missing = [name for name in expected_markers if name not in text_latin1]
    assert not missing, (
        "The ISO file decoded as Latin-1 does not contain the expected names: "
        + ", ".join(missing)
    )