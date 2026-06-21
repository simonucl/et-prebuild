# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student’s solution runs.  We assert the presence of the raw
# input data and the *absence* of any artefacts that the student is expected
# to create.

import os
from pathlib import Path
import pytest

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
RAW_DIR = HOME / "capacity" / "raw"
ANALYSIS_DIR = HOME / "capacity" / "analysis"
LOG_DIR = HOME / "capacity" / "logs"

SERVER_FILES = {
    "serverA": RAW_DIR / "serverA.csv",
    "serverB": RAW_DIR / "serverB.csv",
}

EXPECTED_HEADER = "timestamp,cpu_pct,mem_mb"


# --- Helper functions ---------------------------------------------------------

def _read_first_line(path: Path) -> str:
    """Read the very first line of a text file, stripped of its newline."""
    with path.open("r", encoding="utf-8") as fp:
        return fp.readline().rstrip("\n")


def _count_lines(path: Path) -> int:
    """Return the number of lines in *path*."""
    with path.open("r", encoding="utf-8") as fp:
        return sum(1 for _ in fp)


# --- Tests --------------------------------------------------------------------

def test_raw_directory_exists():
    """The directory /home/user/capacity/raw **must** exist."""
    assert RAW_DIR.is_dir(), (
        f"Required directory missing: {RAW_DIR}.\n"
        "The raw source data must be placed here."
    )


@pytest.mark.parametrize("server, path", SERVER_FILES.items())
def test_raw_files_present(server, path):
    """Each required raw CSV file must exist and be a regular readable file."""
    assert path.exists(), f"Missing raw CSV file: {path}"
    assert path.is_file(), f"Expected a regular file for {path}, but found something else."
    assert os.access(path, os.R_OK), f"File not readable: {path}"


@pytest.mark.parametrize("server, path", SERVER_FILES.items())
def test_csv_header_is_correct(server, path):
    """The first line of every CSV must exactly match the expected header."""
    header = _read_first_line(path)
    assert (
        header == EXPECTED_HEADER
    ), f"{path} has an unexpected header.\nExpected: {EXPECTED_HEADER!r}\nFound:    {header!r}"


@pytest.mark.parametrize("server, path", SERVER_FILES.items())
def test_csv_has_four_samples_plus_header(server, path):
    """
    Each CSV file is expected to contain exactly 5 lines: one header + 4 data
    rows.  This guarantees that the test harness later knows the sample count.
    """
    line_count = _count_lines(path)
    assert (
        line_count == 5
    ), f"{path} should contain 5 lines (header + 4 samples) but contains {line_count}."


def test_no_analysis_files_yet():
    """
    None of the artefacts that the student must create should exist **before**
    their code runs.  We explicitly check for summary.csv and the per-server
    JSON files.
    """
    summary_csv = ANALYSIS_DIR / "summary.csv"
    missing_ok = [summary_csv] + [
        ANALYSIS_DIR / f"{server}.json" for server in SERVER_FILES.keys()
    ]

    for artefact in missing_ok:
        assert not artefact.exists(), (
            f"Found unexpected file before processing: {artefact}\n"
            "The student script should generate this file; it must be absent initially."
        )


def test_no_process_log_yet():
    """
    The process log must not exist yet.  It should be produced by the student
    script during execution.
    """
    log_file = LOG_DIR / "process.log"
    assert not log_file.exists(), (
        f"Unexpected log file already present: {log_file}\n"
        "This file should be created by the student's processing script."
    )