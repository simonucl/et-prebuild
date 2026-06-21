# test_initial_state.py
#
# Pytest suite to validate the *pre-exercise* operating-system state for the
# “open-ports CSV” pipeline kata.
#
# These tests purposely avoid checking for any *output* artefacts such as
# /home/user/reports/vuln_summary.csv or its backup, because they must not
# exist (or are irrelevant) prior to the student’s solution being run.
#
# What **is** verified:
#   1. The mock-scan directory exists and is a directory.
#   2. At least one “*.nmap” file is present inside that directory.
#   3. Every discovered “*.nmap” file is a regular, readable file.
#   4. Each file looks like a plausible Nmap output: it contains both a
#      “Nmap scan report for …” header and at least one line whose STATE is
#      “open”.  This ensures the exercise data are suitable for parsing.
#
# The intent is to give the learner clear, actionable feedback if the base
# environment is incomplete or corrupted *before* they attempt the exercise.

import os
from pathlib import Path

MOCK_DIR = Path("/home/user/mock_scans")

def _discover_nmap_files():
    """Return a list of *.nmap Path objects under MOCK_DIR."""
    return sorted(p for p in MOCK_DIR.glob("*.nmap") if p.is_file())

def test_mock_scan_directory_exists():
    assert MOCK_DIR.exists(), (
        f"Required directory {MOCK_DIR} is missing. "
        "Create it and populate it with .nmap files before proceeding."
    )
    assert MOCK_DIR.is_dir(), f"{MOCK_DIR} exists but is not a directory."

def test_at_least_one_nmap_file_present():
    nmap_files = _discover_nmap_files()
    assert nmap_files, (
        f"No .nmap files found in {MOCK_DIR}. "
        "At least one scan file is required for the exercise."
    )

def test_each_nmap_file_is_readable_and_well_formed():
    nmap_files = _discover_nmap_files()
    assert nmap_files, "Internal error: no .nmap files to validate."

    for path in nmap_files:
        # 1. Readability and type checks
        assert path.is_file(), f"{path} exists but is not a regular file."
        assert os.access(path, os.R_OK), f"{path} is not readable."

        # 2. Content sanity checks — minimal but prevents empty/garbled files
        text = path.read_text(errors="ignore")
        assert "Nmap scan report for" in text, (
            f"{path} does not contain an 'Nmap scan report for' line; "
            "file appears to be malformed."
        )
        assert " open " in text or "\topen\t" in text or "/open " in text, (
            f"{path} contains no lines where STATE is 'open'; "
            "exercise requires at least one open port per file (case-sensitive)."
        )