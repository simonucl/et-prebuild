# test_initial_state.py
#
# This pytest suite validates the *starting* filesystem state that must be
# present BEFORE the student’s solution is run.  It deliberately avoids checking
# for any artefacts that the student is supposed to create later
# (/home/user/cert_analysis/*).
#
# The suite asserts:
#   • /home/user/certs_incoming/ exists.
#   • That directory contains EXACTLY six files:
#       three “*.crt” files and three matching “*.meta” files.
#   • Each .meta file contains the expected single-line, pipe-delimited metadata.
#   • /home/user/cert_analysis/ does NOT yet exist.
#
# Only the Python standard library and pytest are used.

import datetime as _dt
from pathlib import Path
import pytest


# --------------------------------------------------------------------------- #
# Helper data                                                                #
# --------------------------------------------------------------------------- #

INCOMING_DIR = Path("/home/user/certs_incoming")
ANALYSIS_DIR = Path("/home/user/cert_analysis")

EXPECTED_META_CONTENTS = {
    "server_ok.meta": (
        "CN=api.example.com|CN=Example-CA|2023-06-01|2024-12-31"
    ),
    "server_soon.meta": (
        "CN=login.example.com|CN=Example-CA|2023-07-01|2024-07-01"
    ),
    "server_expired.meta": (
        "CN=legacy.example.com|CN=Legacy-CA|2022-05-01|2023-12-31"
    ),
}

EXPECTED_CRT_FILES = {
    "server_ok.crt",
    "server_soon.crt",
    "server_expired.crt",
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_incoming_directory_exists():
    """The incoming certificate directory must be present and be a directory."""
    assert INCOMING_DIR.exists(), (
        f"Required directory {INCOMING_DIR} is missing."
    )
    assert INCOMING_DIR.is_dir(), (
        f"{INCOMING_DIR} exists but is not a directory."
    )


def test_correct_files_present_and_only_those():
    """
    /home/user/certs_incoming/ must contain exactly six files—
    three .crt files and three .meta files—with the expected names.
    """
    files = {p.name for p in INCOMING_DIR.iterdir() if p.is_file()}
    expected_files = EXPECTED_CRT_FILES.union(EXPECTED_META_CONTENTS.keys())

    # Presence
    missing = expected_files.difference(files)
    assert not missing, (
        f"The following required files are missing from {INCOMING_DIR}: {sorted(missing)}"
    )

    # No extras
    extras = files.difference(expected_files)
    assert not extras, (
        f"Unexpected extra file(s) found in {INCOMING_DIR}: {sorted(extras)}"
    )


def _is_iso8601_date(text: str) -> bool:
    """Return True if text is YYYY-MM-DD and represents a valid date."""
    try:
        _dt.date.fromisoformat(text)
        return True
    except ValueError:
        return False


@pytest.mark.parametrize("meta_filename,expected_line", EXPECTED_META_CONTENTS.items())
def test_meta_file_contents(meta_filename: str, expected_line: str):
    """
    Each .meta file must:
      • Exist.
      • Contain exactly one line (optionally terminated by a single newline).
      • Match the expected pipe-delimited metadata.
      • Contain four fields in the correct order.
      • Have ISO-8601 dates in the 3rd and 4th positions.
    """
    meta_path = INCOMING_DIR / meta_filename
    assert meta_path.is_file(), f"Metadata file {meta_path} is missing."

    raw = meta_path.read_text()
    # Allow a single trailing newline, but no additional lines.
    stripped = raw.rstrip("\n")
    assert "\n" not in stripped, (
        f"Metadata file {meta_path} must be single-line; found multiple lines."
    )

    assert stripped == expected_line, (
        f"Unexpected content in {meta_path!s}.\n"
        f"Expected: {expected_line!r}\n"
        f"Found   : {stripped!r}"
    )

    # Structural sanity: 4 fields separated by "|", correct date formats
    parts = stripped.split("|")
    assert len(parts) == 4, (
        f"Metadata in {meta_path} should have 4 pipe-delimited fields; found {len(parts)}."
    )

    not_before, not_after = parts[2], parts[3]
    for label, date_str in [("not_before", not_before), ("not_after", not_after)]:
        assert _is_iso8601_date(date_str), (
            f"{label} value '{date_str}' in {meta_path} is not a valid ISO-8601 date (YYYY-MM-DD)."
        )


def test_analysis_directory_absent():
    """
    The output directory /home/user/cert_analysis/ must NOT exist yet.
    The student’s script will create it during execution.
    """
    assert not ANALYSIS_DIR.exists(), (
        f"Directory {ANALYSIS_DIR} should not exist before the student runs their solution."
    )