# test_initial_state.py
"""
Pytest suite to verify that the operating-system / filesystem is in the
expected initial state *before* the student starts working.

Rules enforced by these tests:
1. The directory /home/user/vuln_scans/ must exist.
2. The file /home/user/vuln_scans/initial_scan.txt must exist and contain
   the exact, unmodified Nmap scan text that the exercise description specifies.
3. No checks are made for the yet-to-be-created output artefact
   (/home/user/vuln_scans/open_ports_summary.log) because the instructions
   explicitly forbid testing for any output files.
"""

import pathlib
import pytest

BASE_DIR = pathlib.Path("/home/user/vuln_scans")
SCAN_FILE = BASE_DIR / "initial_scan.txt"

# The expected, canonical content of the scan file.
EXPECTED_SCAN_LINES = [
    "Host: 10.0.0.5 (target-machine)  Status: Up",
    "PORT     STATE SERVICE",
    "21/tcp   open  ftp",
    "22/tcp   open  ssh",
    "80/tcp   open  http",
    "111/tcp  closed rpcbind",
    "5432/tcp open  postgresql",
]


def test_vuln_scans_directory_exists():
    """/home/user/vuln_scans/ must exist and be a directory."""
    assert BASE_DIR.exists(), (
        f"Required directory missing: {BASE_DIR}. "
        "The exercise expects this directory to be present."
    )
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_initial_scan_file_exists():
    """initial_scan.txt must exist exactly at the prescribed location."""
    assert SCAN_FILE.exists(), (
        f"Required scan file missing: {SCAN_FILE}\n"
        "Make sure the raw scan output has been placed at this exact path."
    )
    assert SCAN_FILE.is_file(), f"{SCAN_FILE} exists but is not a regular file."


def test_initial_scan_file_contents_are_exact():
    """
    The scan file must be byte-for-byte identical to the canonical content.

    We compare on a per-line basis (without newline characters) to give
    clearer diff output if there is a mismatch.
    """
    file_lines = SCAN_FILE.read_text().splitlines()

    # Helpful failure message shows a unified diff of the mismatch.
    if file_lines != EXPECTED_SCAN_LINES:
        diff_lines = list(
            pytest.helpers.diff(expected=EXPECTED_SCAN_LINES, actual=file_lines)
            if hasattr(pytest, "helpers") and hasattr(pytest.helpers, "diff")
            else []
        )
        diff_msg = "\n".join(diff_lines) if diff_lines else ""
        pytest.fail(
            "The content of initial_scan.txt does not match the expected "
            "canonical scan output.\n"
            f"{diff_msg}"
        )