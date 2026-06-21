# test_initial_state.py
#
# This pytest suite validates that the operating-system state *before*
# the student’s action is exactly what the assignment describes.
#
# It checks only the “input” area (/home/user/policy-code) and purposefully
# avoids looking at—or even mentioning—the “output” area
# (/home/user/reports), as per the grading rules.

import os
from pathlib import Path

POLICY_DIR = Path("/home/user/policy-code").resolve()

# Ground-truth expectations derived from the task description
EXPECTED_FILES = {
    POLICY_DIR / "policy.yaml": 113,
    POLICY_DIR / "README.md": 88,
    POLICY_DIR / "script.sh": 67,
    POLICY_DIR / "tests" / "test1.txt": 16,
}
EXPECTED_TOTAL_FILES = 4
EXPECTED_TOTAL_BYTES = 284


def test_policy_directory_exists_and_is_dir():
    assert POLICY_DIR.exists(), f"Required directory {POLICY_DIR} is missing."
    assert POLICY_DIR.is_dir(), f"{POLICY_DIR} exists but is not a directory."


def test_expected_files_present_with_exact_size():
    """
    Each expected file must exist, be a regular file, and have the exact
    byte size stated in the specification.
    """
    for path, expected_size in EXPECTED_FILES.items():
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."
        actual_size = path.stat().st_size
        assert (
            actual_size == expected_size
        ), f"File {path} has size {actual_size} bytes; expected {expected_size}."


def test_no_extra_regular_files_and_correct_aggregate_metrics():
    """
    The directory must contain exactly the expected number of regular files
    and the exact cumulative byte size.
    """
    all_regular_files = [
        p for p in POLICY_DIR.rglob("*") if p.is_file() and not p.is_symlink()
    ]

    total_files = len(all_regular_files)
    total_bytes = sum(p.stat().st_size for p in all_regular_files)

    assert (
        total_files == EXPECTED_TOTAL_FILES
    ), f"Found {total_files} regular files; expected {EXPECTED_TOTAL_FILES}."
    assert (
        total_bytes == EXPECTED_TOTAL_BYTES
    ), f"Cumulative size is {total_bytes} bytes; expected {EXPECTED_TOTAL_BYTES}."