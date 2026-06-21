# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct *initial* state before the student performs any
# actions.  Only the items that are supposed to exist **before** the
# task starts are checked here.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
REPORT_DIR = HOME / "disk_reports"
INDEX_FILE = REPORT_DIR / "index.html"


@pytest.fixture(scope="module")
def index_contents():
    """Return the contents of the index.html file as bytes."""
    try:
        return INDEX_FILE.read_bytes()
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {INDEX_FILE}")


def test_report_directory_exists():
    assert REPORT_DIR.exists(), f"Required directory missing: {REPORT_DIR}"
    assert REPORT_DIR.is_dir(), f"{REPORT_DIR} exists but is not a directory"


def test_index_file_exists_and_is_file():
    assert INDEX_FILE.exists(), f"Required file missing: {INDEX_FILE}"
    assert INDEX_FILE.is_file(), f"{INDEX_FILE} exists but is not a regular file"


def test_index_file_content_exact(index_contents):
    """
    Ensure that /home/user/disk_reports/index.html contains the exact
    HTML expected at the start of the exercise.
    """
    expected_html = (
        "<html>\n"
        "<head><title>Storage Report</title></head>\n"
        "<body>\n"
        "<h1>Storage Administrator Disk Usage Report</h1>\n"
        "<p>This is a placeholder report.</p>\n"
        "</body>\n"
        "</html>\n"
    ).encode()

    actual = index_contents

    # Remove a single trailing newline for comparison tolerance.
    if actual.endswith(b"\n") and not expected_html.endswith(b"\n"):
        actual = actual[:-1]
    if expected_html.endswith(b"\n") and not actual.endswith(b"\n"):
        expected_html = expected_html[:-1]

    assert (
        actual == expected_html
    ), "The contents of index.html do not match the expected initial HTML."


def test_no_extra_files_in_report_directory():
    """
    Verify that no unexpected files are present in /home/user/disk_reports/.
    Only 'index.html' should exist at this point.
    """
    entries = {p.name for p in REPORT_DIR.iterdir()}
    assert entries == {
        "index.html"
    }, (
        "Unexpected files or directories found in "
        f"{REPORT_DIR}: {entries - {'index.html'}}"
    )