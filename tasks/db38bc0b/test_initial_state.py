# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem snapshot
# required for the “time-zone / locale audit” exercise is present and
# contains the exact data the downstream tasks rely on.
#
# IMPORTANT:
# • These tests only check the pre-existing snapshot and do **not**
#   look for any result files the student will generate later.
# • All assertions raise clear, actionable error messages so that any
#   missing or malformed prerequisite can be fixed before students
#   begin their work.
#
# Allowed libraries: stdlib + pytest only.

from pathlib import Path
import pytest

# --- Constants describing the expected snapshot state ------------------------

SNAPSHOT_ROOT = Path("/home/user/compliance_snapshot")
ETC_DIR       = SNAPSHOT_ROOT / "etc"
TIMEZONE_FILE = ETC_DIR / "timezone"
LOCALE_FILE   = ETC_DIR / "locale.conf"
REFERENCE_FILE = SNAPSHOT_ROOT / "AUDIT_REFERENCE"

EXPECTED_TIMEZONE_LINE  = "America/New_York"
EXPECTED_LOCALE_LINES   = [
    'LANG="en_US.UTF-8"',
    'LC_TIME="en_DK.UTF-8"',
]
EXPECTED_REFERENCE_LINE = "2024-04-01T12:00:00Z"


# --- Helper ------------------------------------------------------------------

def _assert_single_line_file(path: Path, expected_line: str) -> None:
    """Utility that asserts a file exists and contains one exact line."""
    assert path.is_file(), f"Expected file {path} to exist."
    content = path.read_text(encoding="utf-8").splitlines()
    assert len(content) == 1, (
        f"Expected {path} to contain exactly one line; found {len(content)} lines."
    )
    assert content[0] == expected_line, (
        f"Unexpected contents in {path}.\n"
        f"Expected: {expected_line!r}\n"
        f"Found:    {content[0]!r}"
    )


# --- Tests -------------------------------------------------------------------

def test_snapshot_directory_structure():
    """The top-level snapshot directories must exist."""
    assert SNAPSHOT_ROOT.is_dir(), f"Snapshot root {SNAPSHOT_ROOT} is missing."
    assert ETC_DIR.is_dir(), f"Directory {ETC_DIR} is missing."


def test_timezone_file():
    """/etc/timezone must exist and contain the expected single line."""
    _assert_single_line_file(TIMEZONE_FILE, EXPECTED_TIMEZONE_LINE)


def test_locale_conf_file():
    """/etc/locale.conf must exist and contain exactly the expected two lines."""
    assert LOCALE_FILE.is_file(), f"Expected file {LOCALE_FILE} to exist."

    # Read non-empty lines without trimming internal whitespace.
    raw_lines = LOCALE_FILE.read_text(encoding="utf-8").splitlines()
    non_empty = [line for line in raw_lines if line.strip()]

    assert len(non_empty) == len(EXPECTED_LOCALE_LINES), (
        f"{LOCALE_FILE} must contain exactly {len(EXPECTED_LOCALE_LINES)} non-empty "
        f"lines; found {len(non_empty)}."
    )

    # We tolerate the student’s snapshot having the two lines in either order,
    # but each expected line must be present verbatim.
    for expected in EXPECTED_LOCALE_LINES:
        assert expected in non_empty, (
            f"Missing line {expected!r} in {LOCALE_FILE}. "
            f"Found lines: {non_empty}"
        )


def test_audit_reference_file():
    """AUDIT_REFERENCE must exist and contain the exact timestamp line."""
    _assert_single_line_file(REFERENCE_FILE, EXPECTED_REFERENCE_LINE)