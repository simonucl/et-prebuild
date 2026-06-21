# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student starts working on the task.  It checks that the
# raw input data are present and correct and that none of the required
# output artefacts have been created yet.
#
# Only Python’s standard library and pytest are used.

from pathlib import Path
import json
import gzip
import pytest

HOME = Path("/home/user").expanduser().resolve()
RAW_DIR = HOME / "data" / "raw"
PROCESSED_DIR = HOME / "data" / "processed"
LOG_DIR = HOME / "data" / "logs"

FILE1 = RAW_DIR / "file1.csv"
FILE2 = RAW_DIR / "file2.csv"

EXPECTED_FILE1 = (
    "id,name,status,value\n"
    "1,Alice,train,0.5\n"
    "2,Bob,test,0.8\n"
    "3,Carol,train,0.3\n"
    "4,Dan,train,0.9\n"
)
EXPECTED_FILE2 = (
    "id,name,status,value\n"
    "3,Carol,train,0.3\n"
    "4,Dan,train,0.9\n"
    "5,Eve,train,0.4\n"
    "6,Frank,val,0.7\n"
)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _read_text(path: Path) -> str:
    """Return file contents as UTF-8 text, raising comprehensible errors."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {path} as UTF-8: {exc}")


# ----------------------------------------------------------------------
# Tests for the *presence* and *content* of the raw input data
# ----------------------------------------------------------------------


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), f"Raw data directory is missing: {RAW_DIR}"


@pytest.mark.parametrize(
    "csv_path,expected_content",
    [
        (FILE1, EXPECTED_FILE1),
        (FILE2, EXPECTED_FILE2),
    ],
)
def test_raw_files_exist_and_match_expected(csv_path: Path, expected_content: str):
    assert csv_path.is_file(), f"Required CSV file is missing: {csv_path}"

    actual = _read_text(csv_path)
    assert (
        actual == expected_content
    ), f"Contents of {csv_path} differ from the expected initial data."


def test_raw_row_counts_are_five_each():
    for path in (FILE1, FILE2):
        lines = _read_text(path).splitlines()
        assert (
            len(lines) == 5
        ), f"Expected 5 lines (header + 4 rows) in {path}, found {len(lines)}."


# ----------------------------------------------------------------------
# Tests that **output artefacts do NOT exist yet**
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        PROCESSED_DIR / "combined_train.csv",
        PROCESSED_DIR / "combined_train.csv.gz",
        LOG_DIR / "prep_timings.log",
        LOG_DIR / "row_counts.log",
    ],
)
def test_no_output_files_yet(path: Path):
    assert (
        not path.exists()
    ), f"Output artefact {path} already exists before processing has begun."


def test_no_processed_directory_yet():
    # The processed directory may legitimately not exist at the very start.
    # If it does exist, it must be empty to avoid interfering with grading.
    if PROCESSED_DIR.exists():
        assert (
            not any(PROCESSED_DIR.iterdir())
        ), f"Processed directory {PROCESSED_DIR} should be empty before the task starts."


def test_no_logs_directory_yet():
    if LOG_DIR.exists():
        assert (
            not any(LOG_DIR.iterdir())
        ), f"Logs directory {LOG_DIR} should be empty before the task starts."