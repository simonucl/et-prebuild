# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action for the “batch summary” exercise.
#
# The tests assert that:
#   • the expected input directory tree exists with the right permissions;
#   • the three required report_YYYYMM.csv files are present
#     and contain the exact, known contents;
#   • the /home/user/output/ directory (and the files that will later be
#     created there) do *not* yet exist, or, if the directory already exists
#     for some reason, it is completely empty.
#
# Only Python stdlib + pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
OUTPUT_DIR = os.path.join(HOME, "output")

# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------
def _mode(path: str) -> int:
    """Return the permission bits (e.g. 0o755, 0o644) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)

def _read_lines(path: str):
    """Return file lines *without* their trailing newline characters."""
    with open(path, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]

# -----------------------------------------------------------------------------
# Ground-truth content for each initial CSV file
# -----------------------------------------------------------------------------
EXPECTED_REPORT_CONTENT = {
    "report_202301.csv": [
        "id,value,comment",
        "1,10,good",
        "2,20,",
        "3,,missing",
    ],
    "report_202302.csv": [
        "id,value,comment",
        "a1,5,low",
        "a2,15,mid",
        "a3,25,high",
    ],
    "report_202303.csv": [
        "id,value,comment",
        "x1,,",
        "x2,50,okay",
        "x3,60,",
    ],
}

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_directories_exist_and_are_world_readable():
    """/home/user/data and /home/user/data/reports must exist and be 755."""
    assert os.path.isdir(DATA_DIR), f"Expected directory {DATA_DIR} to exist"
    assert os.path.isdir(REPORTS_DIR), f"Expected directory {REPORTS_DIR} to exist"

    for dpath in (DATA_DIR, REPORTS_DIR):
        mode = _mode(dpath)
        assert mode == 0o755, (
            f"Directory {dpath} should have permissions 755 "
            f"(actual {oct(mode)})"
        )

@pytest.mark.parametrize("filename", sorted(EXPECTED_REPORT_CONTENT))
def test_report_files_exist_with_correct_content_and_perms(filename):
    """Each report_*.csv must exist with exact expected contents and 644 perms."""
    fpath = os.path.join(REPORTS_DIR, filename)
    assert os.path.isfile(fpath), f"Missing required input file {fpath}"

    # Permissions
    mode = _mode(fpath)
    assert mode == 0o644, (
        f"File {fpath} should have permissions 644 (actual {oct(mode)})"
    )

    # Contents
    expected_lines = EXPECTED_REPORT_CONTENT[filename]
    actual_lines = _read_lines(fpath)
    assert actual_lines == expected_lines, (
        f"Contents of {fpath} do not match the expected ground-truth.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{actual_lines}"
    )

def test_no_output_directory_or_it_is_empty():
    """
    Before the student runs their solution nothing in /home/user/output/ should
    be present.  If the directory does *not* exist, that's fine.  If it *does*
    exist (e.g. left over from a previous run), it must be completely empty so
    that the forthcoming tests can safely check the new artifacts.
    """
    if not os.path.exists(OUTPUT_DIR):
        # Ideal case: directory truly absent.
        assert True
    else:
        # Directory exists; ensure it is a directory and empty.
        assert os.path.isdir(OUTPUT_DIR), f"{OUTPUT_DIR} exists but is not a directory"
        leftover = os.listdir(OUTPUT_DIR)
        assert (
            len(leftover) == 0
        ), f"{OUTPUT_DIR} should be empty before the task starts (found: {leftover})"