# test_initial_state.py
#
# Pytest suite that validates the on-disk state *before* the student performs
# the artifact-compression task.  It ensures that the starting conditions
# match the specification given by the exercise.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Fixtures & constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user").expanduser().resolve()
ARTIFACT_ROOT = HOME / "artifacts"
LOG_DIR = HOME / "optimization_logs"
LOG_FILE = LOG_DIR / "latest_optimization.log"

# Expected .bin files and their exact sizes (bytes)
EXPECTED_BINS = {
    ARTIFACT_ROOT / "repo_alpha" / "file1.bin": 1_200_000,
    ARTIFACT_ROOT / "repo_beta" / "module2" / "file2.bin": 1_200_000,
    ARTIFACT_ROOT / "repo_beta" / "module3" / "file3.bin": 1_200_000,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _read_exact(path: Path, n: int) -> bytes:
    """Read exactly n bytes from a file."""
    with path.open("rb") as fh:
        data = fh.read(n)
    return data


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bin_path,expected_size", EXPECTED_BINS.items())
def test_bin_files_exist_with_correct_size(bin_path: Path, expected_size: int):
    """
    The three .bin files must exist and have the exact size specified
    by the exercise (1 200 000 bytes each).
    """
    assert bin_path.is_file(), (
        f"Required file is missing: {bin_path}. "
        "Make sure the repository is in its original state."
    )

    actual_size = bin_path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"File {bin_path} should be {expected_size} bytes, found {actual_size} bytes."


@pytest.mark.parametrize("bin_path", EXPECTED_BINS.keys())
def test_bin_files_start_with_expected_content(bin_path: Path):
    """
    Sanity-check that the files contain the expected Lorem Ipsum pattern.
    Only the first 12 bytes are validated to avoid heavy I/O.
    """
    first_twelve = _read_exact(bin_path, 12)
    expected_prefix = b"Lorem Ipsum\n"
    assert (
        first_twelve == expected_prefix
    ), f"File {bin_path} does not start with the expected 'Lorem Ipsum\\n' content."


@pytest.mark.parametrize("bin_path", EXPECTED_BINS.keys())
def test_corresponding_gz_files_do_not_exist_yet(bin_path: Path):
    """
    Before the student runs their solution, the compressed .gz files must
    NOT exist; otherwise the grader can't tell if the student did any work.
    """
    gz_path = Path(f"{bin_path}.gz")
    assert not gz_path.exists(), (
        f"Compressed file {gz_path} already exists. "
        "The initial state should contain only the uncompressed .bin files."
    )


def test_no_optimization_log_dir_yet():
    """
    The directory /home/user/optimization_logs should not exist in the
    initial state.
    """
    assert not LOG_DIR.exists(), (
        f"Directory {LOG_DIR} already exists. "
        "It must be absent before the optimization task is run."
    )


def test_no_optimization_log_file_yet():
    """
    The log file should also not exist yet.
    """
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} already exists. "
        "It must be created by the student's solution, not pre-existing."
    )


def test_no_extra_large_bin_files_present():
    """
    There should be *exactly* the three expected .bin files ≥1 MiB
    inside /home/user/artifacts.  This guards against stale files that
    could interfere with the grader.
    """
    found = {
        p for p in ARTIFACT_ROOT.rglob("*.bin") if p.stat().st_size >= 1_048_576
    }
    assert found == set(EXPECTED_BINS.keys()), (
        "The set of .bin files ≥1 MiB under /home/user/artifacts does not match "
        "the expected starting state.\n"
        f"Expected:\n  {sorted(EXPECTED_BINS.keys())}\n"
        f"Found:\n  {sorted(found)}"
    )