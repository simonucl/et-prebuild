# test_initial_state.py
#
# This pytest suite validates the *initial* state of the file-system
# before the student runs their single-command solution.  It makes sure
# that the raw input file is present and correct, and that none of the
# output artefacts have been created yet.

import os
import stat
import pytest

# ----------------------------------------------------------------------
# Paths used in the assignment
RAW_PATH      = "/home/user/dataset/raw.csv"
SORTED_PATH   = "/home/user/dataset/sorted_raw.csv"
BENCH_DIR     = "/home/user/benchmark"
BENCH_LOG     = "/home/user/benchmark/sort_benchmark.log"

# ----------------------------------------------------------------------
# Expected contents of /home/user/dataset/raw.csv (including final '\n')
EXPECTED_RAW_CONTENT = (
    "id,value\n"
    "3,apple\n"
    "1,orange\n"
    "2,banana\n"
)
EXPECTED_RAW_SIZE = 35  # bytes


# ----------------------------------------------------------------------
def test_raw_csv_exists_and_is_regular_file():
    """The raw CSV must exist and be a regular file."""
    assert os.path.exists(RAW_PATH), (
        f"Required file {RAW_PATH!r} is missing."
    )
    assert os.path.isfile(RAW_PATH), (
        f"{RAW_PATH!r} exists but is not a regular file."
    )


def test_raw_csv_contents_are_exact():
    """The raw CSV contents must match the specification exactly."""
    with open(RAW_PATH, "r", newline="") as fh:
        data = fh.read()
    assert data == EXPECTED_RAW_CONTENT, (
        f"{RAW_PATH} contents differ from the expected template.\n"
        "Expected:\n"
        "----------\n"
        f"{EXPECTED_RAW_CONTENT!r}\n"
        "----------\n"
        "Found:\n"
        "----------\n"
        f"{data!r}\n"
        "----------"
    )


def test_raw_csv_size_is_35_bytes():
    """File size must be exactly 35 bytes."""
    size = os.stat(RAW_PATH)[stat.ST_SIZE]
    assert size == EXPECTED_RAW_SIZE, (
        f"{RAW_PATH} should be {EXPECTED_RAW_SIZE} bytes but is {size} bytes."
    )


def test_sorted_file_does_not_exist_yet():
    """The sorted output file must NOT exist before the student's command."""
    assert not os.path.exists(SORTED_PATH), (
        f"Found unexpected file {SORTED_PATH!r}; "
        "the student must create it as part of their solution."
    )


def test_benchmark_log_does_not_exist_yet():
    """The benchmark log must NOT exist before the student's command."""
    if os.path.exists(BENCH_LOG):
        pytest.fail(
            f"Found unexpected file {BENCH_LOG!r}; "
            "the student must create it as part of their solution."
        )


def test_benchmark_directory_state():
    """
    The benchmark directory may or may not exist yet, but if it does,
    it must not contain the benchmark log file.
    """
    if os.path.isdir(BENCH_DIR):
        assert BENCH_LOG not in {
            os.path.join(BENCH_DIR, name) for name in os.listdir(BENCH_DIR)
        }, (
            f"Directory {BENCH_DIR!r} already contains {BENCH_LOG!r}; "
            "it should not exist before the student's command."
        )