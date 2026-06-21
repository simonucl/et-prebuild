# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the filesystem
# before the student implements the four-stage CSV pipeline.
#
# Run with:  pytest -q
#
# These tests must pass *prior* to any work being done.  They guarantee
# that the starting environment is exactly what the subsequent grading
# rubric expects.

import os
from pathlib import Path
import stat

PROJECT_ROOT = Path("/home/user")
INCOMING_DIR = PROJECT_ROOT / "incoming"
LOGS_DIR = PROJECT_ROOT / "logs"
ARCHIVE_DIR = PROJECT_ROOT / "archive"
FAILED_DIR = PROJECT_ROOT / "failed"
PIPELINE_SCRIPT = PROJECT_ROOT / "process_pipeline.sh"

GOOD_CSV = INCOMING_DIR / "good_data.csv"
BAD_CSV = INCOMING_DIR / "bad_data.csv"

GOOD_CONTENT = [
    "1,Alpha,2024-06-01T10:15:00Z,ACTIVE",
    "2,Beta,2024-06-01T10:20:00Z,INACTIVE",
    "3,Gamma,2024-06-01T10:25:00Z,ACTIVE",
]

BAD_CONTENT = [
    "a,Delta,2024-06-01T11:00:00Z,ACTIVE",
    "4,Epsilon,not-a-timestamp,INACTIVE",
    "5,Zeta,2024-06-01T11:10:00Z,BROKEN",
    "6,Eta,2024-06-01T11:15:00Z,ACTIVE",
]


def _read_csv_lines(path: Path):
    """Return non-empty lines stripped of their trailing newline."""
    return [line.rstrip("\n") for line in path.read_text().splitlines()]


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), f"Project root {PROJECT_ROOT} is missing."


def test_incoming_directory_and_csv_files_exist():
    assert INCOMING_DIR.is_dir(), f"Incoming directory {INCOMING_DIR} is missing."

    expected_files = {GOOD_CSV.name, BAD_CSV.name}
    actual_files = {p.name for p in INCOMING_DIR.iterdir() if p.is_file()}

    assert expected_files.issubset(
        actual_files
    ), f"Incoming directory should contain at least {expected_files}, found {actual_files}."


def test_good_csv_contents():
    assert GOOD_CSV.is_file(), f"Expected file {GOOD_CSV} is missing."
    lines = _read_csv_lines(GOOD_CSV)

    assert (
        lines == GOOD_CONTENT
    ), f"Contents of {GOOD_CSV} do not match the expected initial data."


def test_bad_csv_contents():
    assert BAD_CSV.is_file(), f"Expected file {BAD_CSV} is missing."
    lines = _read_csv_lines(BAD_CSV)

    assert (
        lines == BAD_CONTENT
    ), f"Contents of {BAD_CSV} do not match the expected initial data."


def test_logs_directory_exists_and_is_empty():
    assert LOGS_DIR.is_dir(), f"Logs directory {LOGS_DIR} is missing."
    files = [p for p in LOGS_DIR.iterdir() if p.is_file()]
    assert (
        not files
    ), f"Logs directory should be empty initially, found the following files: {files}"


def test_archive_and_failed_directories_do_not_exist_yet():
    assert (
        not ARCHIVE_DIR.exists()
    ), f"Archive directory {ARCHIVE_DIR} should NOT exist before running the pipeline."
    assert (
        not FAILED_DIR.exists()
    ), f"Failed directory {FAILED_DIR} should NOT exist before running the pipeline."


def test_pipeline_script_not_present_yet():
    assert (
        not PIPELINE_SCRIPT.exists()
    ), f"{PIPELINE_SCRIPT} should not exist before the student creates it."


def test_no_extraneous_top_level_items():
    """
    Ensure that no unexpected directories/files that belong to the final
    solution already exist.  This helps catch accidental leakage of
    solution artefacts into the starting snapshot.
    """
    forbidden = {
        "archive",
        "failed",
        "process_pipeline.sh",
        "pipeline_audit.log",
    }
    top_level_items = {p.name for p in PROJECT_ROOT.iterdir()}
    offenders = forbidden.intersection(top_level_items)
    assert (
        not offenders
    ), f"The following items should NOT exist yet: {', '.join(sorted(offenders))}"