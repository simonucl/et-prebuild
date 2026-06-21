# test_initial_state.py
#
# This pytest file verifies the OPERATING SYSTEM state **before** the student
# performs any actions.  It checks that the expected “raw” log files are present
# exactly as specified and that none of the output directories / files that the
# task asks the student to create already exist.
#
# The tests will fail with clear messages if anything is missing or altered.

import textwrap
from pathlib import Path

import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "research" / "logs" / "raw"
COMBINED_DIR = HOME / "research" / "logs" / "combined"
FILTERED_DIR = HOME / "research" / "logs" / "filtered"

# --------------------------------------------------------------------------- #
# Helper:  canonical description of each raw log file *including* newlines.
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    RAW_DIR / "run1.log": textwrap.dedent(
        """\
        2023-05-01 09:00:00.123 [data_collector] INFO: Starting data collection
        2023-05-01 09:00:01.456 [data_collector] DEBUG: Reading sensor 1
        2023-05-01 09:00:02.789 [data_collector] WARNING: Sensor 1 value out of range
        2023-05-01 09:00:03.012 [data_collector] INFO: Sensor 1 value normalized
        2023-05-01 09:00:04.345 [data_collector] ERROR: Failed to write to database
        """
    ),
    RAW_DIR / "run2.log": textwrap.dedent(
        """\
        2023-05-01 10:10:00.111 [data_processor] INFO: Starting batch job
        2023-05-01 10:10:02.222 [data_processor] WARNING: Missing metadata for file X
        2023-05-01 10:10:05.555 [data_processor] INFO: Completed batch job
        2023-05-01 10:10:06.666 [data_processor] DEBUG: Post-processing
        2023-05-01 10:10:07.777 [data_processor] FATAL: Unrecoverable error, shutting down
        """
    ),
    RAW_DIR / "run3.log": textwrap.dedent(
        """\
        2023-05-01 11:20:00.000 [report_generator] DEBUG: loading templates
        2023-05-01 11:20:01.000 [report_generator] INFO: generating report
        2023-05-01 11:20:02.000 [report_generator] WARNING: deprecated API
        2023-05-01 11:20:03.000 [report_generator] INFO: report generated
        2023-05-01 11:20:04.000 [report_generator] ERROR: failed to upload report
        """
    ),
}

# Make sure every expected-content string ends with a newline so that we test
# the exact byte-for-byte representation the grader will look for.
for pth, txt in EXPECTED_FILES.items():
    if not txt.endswith("\n"):
        EXPECTED_FILES[pth] = txt + "\n"


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_raw_directory_exists_and_only_expected_files():
    """The raw directory should exist and contain exactly the three *.log files."""
    assert RAW_DIR.is_dir(), f"Missing directory: {RAW_DIR}"
    found_logs = sorted(f.name for f in RAW_DIR.glob("*.log"))
    expected_logs = sorted(p.name for p in EXPECTED_FILES)
    assert (
        found_logs == expected_logs
    ), f"Raw directory should contain only {expected_logs}, found {found_logs}"


@pytest.mark.parametrize("filepath, expected_content", EXPECTED_FILES.items())
def test_each_raw_log_file_exact_contents(filepath: Path, expected_content: str):
    """Each raw log file must exist and match the canonical contents byte-for-byte."""
    assert filepath.is_file(), f"Missing log file: {filepath}"
    actual = filepath.read_text(encoding="utf-8")
    # Compare lengths first for an easy-to-interpret diff when they mismatch.
    assert (
        len(actual) == len(expected_content)
    ), f"Size mismatch for {filepath}: expected {len(expected_content)} bytes, got {len(actual)} bytes"
    assert (
        actual == expected_content
    ), f"Contents of {filepath} differ from expected value.\n--- Expected ---\n{expected_content}\n--- Actual ---\n{actual}\n"


def test_output_directories_do_not_yet_exist():
    """combined/ and filtered/ directories should NOT exist before the student runs their code."""
    assert (
        not COMBINED_DIR.exists()
    ), f"{COMBINED_DIR} already exists but should be created by the student's script."
    assert (
        not FILTERED_DIR.exists()
    ), f"{FILTERED_DIR} already exists but should be created by the student's script."


def test_no_accidental_files_in_parent_logs_dir():
    """Ensure no premature output files have been placed in /research/logs/."""
    parent_logs_dir = RAW_DIR.parent
    forbidden = {"combined", "filtered", "full.log", "critical.log", "summary.csv"}
    hits = [p for p in parent_logs_dir.rglob("*") if p.name in forbidden]
    assert (
        not hits
    ), f"Found files/directories that should not exist yet: {', '.join(str(h) for h in hits)}"