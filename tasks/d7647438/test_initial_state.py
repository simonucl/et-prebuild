# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# for the “CSV → minified-JSON” transformation exercise.
#
# These tests are executed **before** the student performs any action.
# They must therefore assert the presence of the input artefacts and
# the absence of the expected output artefacts.
#
# The requirements verified here come directly from the task description:
#   1. /home/user/project/data/users.csv must exist and contain the exact
#      4 lines spelled out in the spec (header + 3 data rows).
#   2. No output files or directories (public/, users.min.json,
#      transformation.log) may yet exist.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import os
import stat
import pytest

PROJECT_ROOT = Path("/home/user/project")
DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = DATA_DIR / "users.csv"
PUBLIC_DIR = PROJECT_ROOT / "public"
MINIFIED_JSON_PATH = PUBLIC_DIR / "users.min.json"
LOG_PATH = PROJECT_ROOT / "transformation.log"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def readable_perms(path: Path) -> str:
    """Return a string like '0644' from path.stat().st_mode."""
    return oct(path.stat().st_mode & 0o777)


# ---------------------------------------------------------------------------
# Tests for required initial artefacts
# ---------------------------------------------------------------------------

def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected directory {PROJECT_ROOT} to exist. "
        "Make sure the project was set up in the correct location."
    )


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required data directory {DATA_DIR} is missing."
    )


def test_csv_file_exists():
    assert CSV_PATH.is_file(), (
        f"CSV source file {CSV_PATH} is missing."
    )


def test_csv_file_permissions():
    # The exact permissions are not critical for functionality,
    # but they *must* be owner-readable.
    mode = CSV_PATH.stat().st_mode
    assert mode & stat.S_IRUSR, (
        f"CSV file {CSV_PATH} is not readable by the current user "
        f"(permissions: {readable_perms(CSV_PATH)})."
    )


def test_csv_file_content_exact_match():
    expected_lines = [
        "id,first_name,last_name,email",
        "1,Jane,Doe,jane.doe@example.com",
        "2,John,Smith,john.smith@example.com",
        "3,Alice,Brown,alice.brown@example.com",
    ]

    actual_lines = CSV_PATH.read_text(encoding="utf-8").splitlines()
    assert actual_lines == expected_lines, (
        f"Content of {CSV_PATH} does not match the specification.\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Got ({len(actual_lines)} lines):\n{actual_lines}"
    )


# ---------------------------------------------------------------------------
# Tests ensuring NO output artefacts are present yet
# ---------------------------------------------------------------------------

def test_public_directory_absent_or_empty():
    """
    The transformation has not happened yet, therefore the public/
    directory should either not exist or, if it does exist for some
    unrelated reason, it must not contain users.min.json.
    """
    if not PUBLIC_DIR.exists():
        # Ideal case: directory absent.
        return

    # Directory exists – ensure the target JSON is not already there.
    assert PUBLIC_DIR.is_dir(), f"{PUBLIC_DIR} exists but is not a directory."
    assert not MINIFIED_JSON_PATH.exists(), (
        f"Output file {MINIFIED_JSON_PATH} should NOT exist before "
        "the transformation is performed."
    )


def test_transformation_log_absent():
    assert not LOG_PATH.exists(), (
        f"Log file {LOG_PATH} should NOT exist in the initial state."
    )


# ---------------------------------------------------------------------------
# Sanity check: nothing accidentally created in project root
# ---------------------------------------------------------------------------

def test_no_unexpected_output_files():
    unwanted = [MINIFIED_JSON_PATH, LOG_PATH]
    missing_unwanted = [p for p in unwanted if p.exists()]
    assert not missing_unwanted, (
        "Found artefacts that should not yet exist:\n" +
        "\n".join(str(p) for p in missing_unwanted)
    )