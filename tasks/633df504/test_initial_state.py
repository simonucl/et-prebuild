# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem state
# for the compliance-project exercise **before** the student
# adds a Makefile or generates any artefacts.
#
# Requirements verified:
# 1. Pre-populated data files exist and have the exact,
#    expected content (line-for-line, byte-for-byte).
# 2. No Makefile is present yet.
# 3. No output artefacts (audit.log, report.txt) are present.
#
# Only the Python standard library and pytest are used.

import os
import pathlib
import pytest

# ---------- CONSTANTS ---------------------------------------------------------

BASE_DIR = pathlib.Path("/home/user/compliance_project")
DATA_DIR = BASE_DIR / "data"

POLICIES_PATH = DATA_DIR / "policies.json"
CONTROLS_PATH = DATA_DIR / "controls.csv"

MAKEFILE_PATH = BASE_DIR / "Makefile"
AUDIT_LOG_PATH = BASE_DIR / "audit.log"
REPORT_TXT_PATH = BASE_DIR / "report.txt"

EXPECTED_POLICIES_LINES = [
    '{"id":1,"policy":"encryption"}',
    '{"id":2,"policy":"access-control"}',
    '{"id":3,"policy":"backup"}',
]

EXPECTED_CONTROLS_LINES = [
    "id,control",
    "1,Full Disk Encryption",
    "2,Role Based Access Control",
    "3,Automated Backups",
]

# ---------- HELPERS -----------------------------------------------------------


def _read_lines(path: pathlib.Path):
    """Return a list of strings for each *non-empty* line (no trailing newlines)."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# ---------- TESTS -------------------------------------------------------------


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The initial dataset must be present before starting the task."
    )


def test_policies_file_content():
    assert POLICIES_PATH.is_file(), (
        f"Missing file: {POLICIES_PATH}. "
        "The starter repository must contain this JSON policies file."
    )
    lines = _read_lines(POLICIES_PATH)
    assert lines == EXPECTED_POLICIES_LINES, (
        f"{POLICIES_PATH} content mismatch.\n"
        f"Expected {len(EXPECTED_POLICIES_LINES)} lines exactly:\n"
        f"{EXPECTED_POLICIES_LINES}\n\n"
        f"Found {len(lines)} lines:\n{lines}"
    )


def test_controls_file_content():
    assert CONTROLS_PATH.is_file(), (
        f"Missing file: {CONTROLS_PATH}. "
        "The starter repository must contain this CSV controls file."
    )
    lines = _read_lines(CONTROLS_PATH)
    assert lines == EXPECTED_CONTROLS_LINES, (
        f"{CONTROLS_PATH} content mismatch.\n"
        f"Expected {len(EXPECTED_CONTROLS_LINES)} lines exactly:\n"
        f"{EXPECTED_CONTROLS_LINES}\n\n"
        f"Found {len(lines)} lines:\n{lines}"
    )


def test_makefile_absent_initially():
    assert not MAKEFILE_PATH.exists(), (
        f"{MAKEFILE_PATH} should NOT exist at the initial state. "
        "Students create it as part of the exercise."
    )


def test_output_files_absent_initially():
    missing = [
        p for p in (AUDIT_LOG_PATH, REPORT_TXT_PATH) if p.exists()
    ]
    assert not missing, (
        "Output files unexpectedly present at initial state: "
        + ", ".join(str(p) for p in missing)
    )