# test_initial_state.py
#
# This test-suite validates that the *initial* operating-system state
# is exactly what the assignment specification promises—before the
# student performs any actions.  The tests intentionally *fail* if
# anything is missing, renamed, pre-created, or content-mismatched,
# giving the learner clear feedback.

import os
from pathlib import Path

import pytest


METRICS_DIR = Path("/home/user/metrics")
REPORTS_DIR = Path("/home/user/reports")

CPU_LOG = METRICS_DIR / "cpu.log"
MEM_LOG = METRICS_DIR / "memory.log"

EXPECTED_CPU_CONTENT = (
    "2024-06-01T00:00 15\n"
    "2024-06-01T01:00 17\n"
    "2024-06-01T02:00 20\n"
)

EXPECTED_MEM_CONTENT = (
    "2024-06-01T00:00 45\n"
    "2024-06-01T01:00 50\n"
    "2024-06-01T02:00 55\n"
)


def _assert_file_content(path: Path, expected: str) -> None:
    """
    Helper that asserts *byte-for-byte* equality between a file
    and an expected string, giving a useful assertion message.
    """
    try:
        actual = path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")

    assert (
        actual == expected
    ), (
        f"Content mismatch in {path}.\n\n"
        "----- Expected (repr) -----\n"
        f"{repr(expected)}\n"
        "-----   Actual (repr) -----\n"
        f"{repr(actual)}\n"
    )


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (CPU_LOG, EXPECTED_CPU_CONTENT),
        (MEM_LOG, EXPECTED_MEM_CONTENT),
    ],
)
def test_metrics_files_exist_with_correct_content(file_path: Path, expected_content: str):
    """
    1. /home/user/metrics/cpu.log and /home/user/metrics/memory.log must exist.
    2. Each file must contain *exactly* the expected three lines and a
       single trailing newline (no extra blank lines or spaces).
    """
    assert file_path.is_file(), f"Required file {file_path} is missing or not a regular file."
    _assert_file_content(file_path, expected_content)


def test_reports_directory_not_precreated():
    """
    The instructions say the student must create /home/user/reports *if it does not already exist*.
    For a clean starting state we expect it NOT to exist yet.
    """
    assert not REPORTS_DIR.exists(), (
        f"The directory {REPORTS_DIR} should not exist before the student starts. "
        "Please remove it so the learner can create it themselves."
    )


def test_summary_csv_does_not_exist_yet():
    """
    The output file must not pre-exist; it is the artifact the student will create.
    """
    summary_csv = REPORTS_DIR / "usage_summary.csv"
    assert not summary_csv.exists(), (
        f"The file {summary_csv} already exists. "
        "It should NOT be present before the task is attempted."
    )