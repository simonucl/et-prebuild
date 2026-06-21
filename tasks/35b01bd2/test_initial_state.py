# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state that must be present **before** the student’s solution runs.
#
# It deliberately checks ONLY the pre-existing artefacts that the student’s
# script will consume.  It does *not* look for any output the student is
# supposed to generate.

import os
from pathlib import Path
import textwrap
import pytest

# ---------------------------------------------------------------------------
# Constants – hard-coded absolute paths per the task description
# ---------------------------------------------------------------------------

BUILDS_DIR = Path("/home/user/builds")
INPUT_CSV  = BUILDS_DIR / "2024-05-01_daily_build_status.csv"

# Expected *complete* content of the input CSV, including the trailing \n
EXPECTED_CSV_CONTENT = textwrap.dedent("""\
    BuildID,Platform,Duration,Result,Artifact
    B001,Android,15m,PASS,app-android-B001.apk
    B002,iOS,17m,FAIL,app-ios-B002.ipa
    B003,Android,18m,FAIL,app-android-B003.apk
    B004,iOS,15m,PASS,app-ios-B004.ipa
""").lstrip()  # Remove the leading newline inserted by dedent


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    """Return file content as UTF-8 text, fail verbosely if anything goes wrong."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc!r}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_builds_directory_exists():
    """The /home/user/builds directory that holds the CSV must exist."""
    assert BUILDS_DIR.is_dir(), (
        f"Directory not found: {BUILDS_DIR}\n"
        "Make sure the 'builds' directory is present at the expected location."
    )


def test_input_csv_exists_and_is_file():
    """The daily build status CSV must exist and be a regular file."""
    assert INPUT_CSV.exists(), f"Input CSV is missing: {INPUT_CSV}"
    assert INPUT_CSV.is_file(), f"Expected a regular file at {INPUT_CSV}, found something else."


def test_input_csv_content_exact_match():
    """
    The CSV file must contain exactly the five rows provided in the
    specification (including the single header line) and end with a newline.
    """
    actual = _read_text(INPUT_CSV)
    assert actual == EXPECTED_CSV_CONTENT, (
        f"Content mismatch in {INPUT_CSV}.\n"
        "Expected:\n"
        "----------------------------------------\n"
        f"{EXPECTED_CSV_CONTENT}"
        "----------------------------------------\n"
        "Actual:\n"
        "----------------------------------------\n"
        f"{actual}"
        "----------------------------------------\n"
        "Ensure the file is unmodified."
    )