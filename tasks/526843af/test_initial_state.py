# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student starts working.  It checks that the prerequisite log
# files are present with the exact expected contents and that none of the
# artefacts the student is supposed to create (diagnostics directory,
# report, flag file, tarball) are present yet.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

# Paths that must already exist
ACCESS_LOG = HOME / "app" / "logs" / "access.log"
ERROR_LOG = HOME / "app" / "logs" / "error.log"

# Paths that must *not* exist yet (created by student later)
DIAG_DIR   = HOME / "diagnostics"
DIAG_LOG   = DIAG_DIR / "acmeweb_diagnostic.log"
DONE_FILE  = DIAG_DIR / "DONE"
TARBALL    = DIAG_DIR / "acmeweb_logs.tar.gz"

EXPECTED_ACCESS_LINES = [
    '127.0.0.1 - - [15/Sep/2023:14:21:43 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '203.0.113.10 - - [15/Sep/2023:14:22:01 +0000] "POST /login HTTP/1.1" 500 7212',
    '198.51.100.77 - - [15/Sep/2023:14:22:05 +0000] "GET /api/data HTTP/1.1" 500 532',
    '203.0.113.10 - - [15/Sep/2023:14:22:08 +0000] "GET /dashboard HTTP/1.1" 200 854',
    '192.0.2.55 - - [15/Sep/2023:14:22:15 +0000] "GET /reports HTTP/1.1" 500 1300',
]

EXPECTED_ERROR_LINES = [
    "2023-09-15T14:22:01Z ERROR com.acmeweb.auth.LoginController - NullPointerException",
    "java.lang.NullPointerException",
    "    at com.acmeweb.auth.LoginController.authenticate(LoginController.java:42)",
    "2023-09-15T14:22:05Z ERROR com.acmeweb.api.DataController - IllegalStateException",
    "java.lang.IllegalStateException",
    "    at com.acmeweb.api.DataController.fetch(DataController.java:37)",
    "2023-09-15T14:22:15Z ERROR com.acmeweb.reports.ReportsController - SQLException",
    "java.sql.SQLException",
    "    at com.acmeweb.reports.ReportsController.buildReport(ReportsController.java:55)",
    "2023-09-15T14:23:00Z INFO  HealthCheck - OK",
]


def _read_file_lines(path: Path):
    """
    Helper that returns a list of file lines stripped of trailing newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


def test_access_log_exists_with_expected_contents():
    """access.log must exist with exactly the expected five lines."""
    assert ACCESS_LOG.is_file(), f"Missing file: {ACCESS_LOG}"
    lines = _read_file_lines(ACCESS_LOG)
    assert lines == EXPECTED_ACCESS_LINES, (
        "access.log contents do not match the expected baseline.\n"
        f"Expected:\n{EXPECTED_ACCESS_LINES!r}\n\nFound:\n{lines!r}"
    )


def test_error_log_exists_with_expected_contents():
    """error.log must exist with exactly the expected 10 lines."""
    assert ERROR_LOG.is_file(), f"Missing file: {ERROR_LOG}"
    lines = _read_file_lines(ERROR_LOG)
    assert lines == EXPECTED_ERROR_LINES, (
        "error.log contents do not match the expected baseline.\n"
        f"Expected:\n{EXPECTED_ERROR_LINES!r}\n\nFound:\n{lines!r}"
    )


@pytest.mark.parametrize(
    "path",
    [DIAG_LOG, DONE_FILE, TARBALL],
)
def test_output_files_do_not_exist_yet(path: Path):
    """
    The artefacts that the student must create should not exist at the
    start of the exercise.
    """
    assert not path.exists(), (
        f"Found {path} on disk before the exercise started.  "
        "This file should be created by the student."
    )


def test_diagnostics_directory_not_prepopulated():
    """
    The /home/user/diagnostics directory should *not* exist, or if it does
    exist already, it must be empty because the student is responsible for
    populating it.
    """
    if not DIAG_DIR.exists():
        # Perfectly fine—the student will create it.
        return

    # If it does exist, ensure it contains no files yet.
    unexpected_files = [p for p in DIAG_DIR.iterdir()]
    assert (
        not unexpected_files
    ), f"/home/user/diagnostics is expected to be empty, but found: {unexpected_files}"