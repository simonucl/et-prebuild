# test_initial_state.py
#
# Pytest suite that validates the operating-system state
# BEFORE the student performs any work on the assignment.
#
# Requirements checked:
#   1. The three HTML files are present exactly where expected.
#   2. Their byte-sizes match the authoritative ground-truth.
#   3. The target output directory (/home/user/perf) and its
#      expected result files do NOT yet exist.

import os
import stat
import pytest

HOME = "/home/user"

WEBPAGES_DIR = os.path.join(HOME, "webpages")
HTML_FILES = {
    "page1.html": 75,
    "page2.html": 74,
    "page3.html": 77,
}

PERF_DIR = os.path.join(HOME, "perf")
CSV_REPORT = os.path.join(PERF_DIR, "initial_load_metrics.csv")
LOG_REPORT = os.path.join(PERF_DIR, "content_length.log")


def _full_path(filename: str) -> str:
    """Return the absolute path of a file inside /home/user/webpages."""
    return os.path.join(WEBPAGES_DIR, filename)


def _read_file_size(path: str) -> int:
    """Return the size in bytes of a file at *path* (raises if not a file)."""
    st = os.stat(path)
    if not stat.S_ISREG(st.st_mode):
        raise AssertionError(f"Expected {path!r} to be a regular file, "
                             f"but it is not (mode={oct(st.st_mode)})")
    return st.st_size


def test_webpages_directory_exists():
    assert os.path.isdir(WEBPAGES_DIR), (
        f"Required directory {WEBPAGES_DIR} is missing. "
        "The three HTML pages must be located here before the exercise begins."
    )


@pytest.mark.parametrize("filename,expected_size", HTML_FILES.items())
def test_html_files_exist_with_expected_size(filename, expected_size):
    full_path = _full_path(filename)

    assert os.path.exists(full_path), (
        f"Required HTML file {full_path} is missing."
    )

    size = _read_file_size(full_path)
    assert size == expected_size, (
        f"File {full_path} exists but its size is {size} bytes; "
        f"expected {expected_size} bytes. Do not modify these files."
    )


def test_perf_directory_does_not_exist_yet():
    """
    The /home/user/perf directory (and its contents) must NOT exist before the
    student runs their solution.  Its absence proves the environment is clean.
    """
    assert not os.path.exists(PERF_DIR), (
        f"Directory {PERF_DIR} already exists, but it should not be present "
        "before the student creates it."
    )

    # Even if the directory itself is absent, also assert that the expected
    # result files have not been created in some other location.
    assert not os.path.exists(CSV_REPORT), (
        f"File {CSV_REPORT} already exists, but it must be created by the "
        "student's solution."
    )
    assert not os.path.exists(LOG_REPORT), (
        f"File {LOG_REPORT} already exists, but it must be created by the "
        "student's solution."
    )