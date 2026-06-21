# test_initial_state.py
"""
Pytest suite to verify the initial, pre-exercise state of the operating system.

We assert:
1. The two source snapshot files exist at their absolute paths and contain the
   exact expected content.
2. The destination CSV file does *not* yet exist (it will be created by the
   learner).
3. The /home/user/diag directory itself exists.
4. Standard GNU coreutils programs required by the task (`cut`, `paste`,
   `echo`) are discoverable in the current $PATH.

Any failure pin-points the missing or mismatching element so the learner can
investigate before starting the exercise.
"""

import pathlib
import shutil

import pytest

# ---------- Constants --------------------------------------------------------

HOME = pathlib.Path("/home/user")
DIAG_DIR = HOME / "diag"

CPU_LOG = DIAG_DIR / "cpu_usage.log"
MEM_LOG = DIAG_DIR / "mem_usage.log"
COMBINED_CSV = DIAG_DIR / "combined_usage.csv"

CPU_EXPECTED = (
    "2023-07-15T10:00:00 12\n"
    "2023-07-15T10:05:00 18\n"
    "2023-07-15T10:10:00 20\n"
    "2023-07-15T10:15:00 25\n"
)

MEM_EXPECTED = (
    "2023-07-15T10:00:00 2048\n"
    "2023-07-15T10:05:00 2100\n"
    "2023-07-15T10:10:00 2150\n"
    "2023-07-15T10:15:00 2200\n"
)

REQUIRED_COREUTILS = ("cut", "paste", "echo")

# ---------- Helper -----------------------------------------------------------


def assert_file_content(path: pathlib.Path, expected: str) -> None:
    """
    Helper that asserts a file's byte-for-byte content.
    Emits a detailed message on mismatch.
    """
    assert path.exists(), f"Required file missing: {path}"
    assert path.is_file(), f"Expected a regular file, got something else: {path}"

    data = path.read_text(encoding="utf-8")
    assert (
        data == expected
    ), f"File {path} content mismatch.\n--- expected ---\n{expected!r}\n--- found ---\n{data!r}"


# ---------- Tests ------------------------------------------------------------


def test_diag_directory_present():
    """The /home/user/diag directory must already exist."""
    assert DIAG_DIR.exists(), f"Directory {DIAG_DIR} is missing."
    assert DIAG_DIR.is_dir(), f"{DIAG_DIR} exists but is not a directory."


def test_cpu_usage_log_present_and_correct():
    """cpu_usage.log must exist and contain the exact expected text."""
    assert_file_content(CPU_LOG, CPU_EXPECTED)


def test_mem_usage_log_present_and_correct():
    """mem_usage.log must exist and contain the exact expected text."""
    assert_file_content(MEM_LOG, MEM_EXPECTED)


def test_combined_usage_csv_absent():
    """
    combined_usage.csv should NOT exist yet.
    Its presence would imply the exercise has already been done.
    """
    assert not COMBINED_CSV.exists(), (
        f"{COMBINED_CSV} already exists. "
        "The exercise expects the learner to create this file during their solution."
    )


@pytest.mark.parametrize("binary", REQUIRED_COREUTILS)
def test_required_coreutils_available(binary):
    """
    Ensure that basic GNU coreutils tools required by the task
    are present in the PATH.
    """
    path = shutil.which(binary)
    assert (
        path is not None
    ), f"Required coreutils program '{binary}' not found in PATH."