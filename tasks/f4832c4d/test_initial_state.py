# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem/OS state
# (before the learner performs any work) matches the specification
# laid out in the task description.  It checks:
#
# 1. Presence of the two raw Apache access-log snapshots with the exact
#    expected contents (5 lines each, LF endings only, no CR bytes).
# 2. Absence of the output directory (/home/user/project/reports) and any
#    deliverable files (combined_report.csv, command_log.txt).
#
# Any failure message pinpoints precisely what is missing or incorrect,
# guiding the learner to start from the proper base state.
import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "project" / "logs"
REPORTS_DIR = HOME / "project" / "reports"

DAY1_LOG = LOG_DIR / "day1_access.log"
DAY2_LOG = LOG_DIR / "day2_access.log"

DAY1_EXPECTED_LINES = [
    '192.168.1.10 - - [15/Sep/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1043 "-" "Mozilla/5.0"',
    '172.16.0.3 - - [15/Sep/2023:10:02:47 +0000] "POST /login HTTP/1.1" 302 560 "-" "Mozilla/5.0"',
    '93.184.216.34 - - [15/Sep/2023:10:03:12 +0000] "GET /images/logo.png HTTP/1.1" 304 0 "-" "Mozilla/5.0"',
    '192.0.2.44 - - [15/Sep/2023:10:05:55 +0000] "GET /about HTTP/1.1" 200 2048 "-" "Mozilla/5.0"',
    '203.0.113.5 - - [15/Sep/2023:10:07:23 +0000] "GET /contact HTTP/1.1" 404 512 "-" "Mozilla/5.0"',
]

DAY2_EXPECTED_LINES = [
    '192.168.1.10 - - [16/Sep/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1100 "-" "Mozilla/5.0"',
    '172.16.0.3 - - [16/Sep/2023:10:02:47 +0000] "POST /login HTTP/1.1" 200 580 "-" "Mozilla/5.0"',
    '93.184.216.34 - - [16/Sep/2023:10:03:12 +0000] "GET /images/logo.png HTTP/1.1" 304 0 "-" "Mozilla/5.0"',
    '192.0.2.44 - - [16/Sep/2023:10:05:55 +0000] "GET /about HTTP/1.1" 503 2100 "-" "Mozilla/5.0"',
    '203.0.113.5 - - [16/Sep/2023:10:07:23 +0000] "GET /contact HTTP/1.1" 200 540 "-" "Mozilla/5.0"',
]


@pytest.fixture(scope="module", autouse=True)
def _ensure_home_is_correct():
    """
    Quickly sanity-check that /home/user exists so we don't run these tests
    on the wrong host/CI runner by accident.
    """
    assert HOME.exists(), "Base directory /home/user does not exist on this system."


def _read_lines(path: Path):
    """Read the file as text (universal newlines) and return list of lines."""
    with path.open("r", encoding="utf-8") as fh:
        # Strip only the final newline produced by splitlines(keepends=False)
        return fh.read().splitlines()


def _no_cr_bytes(path: Path):
    """True if the file contains *no* carriage-return bytes (CR, \\r)."""
    with path.open("rb") as fh:
        return b"\r" not in fh.read()


def test_log_directory_exists_and_is_populated():
    assert LOG_DIR.is_dir(), f"Required directory missing: {LOG_DIR}"
    assert DAY1_LOG.is_file(), f"Missing log file: {DAY1_LOG}"
    assert DAY2_LOG.is_file(), f"Missing log file: {DAY2_LOG}"


@pytest.mark.parametrize(
    ("path", "expected_lines"),
    [
        (DAY1_LOG, DAY1_EXPECTED_LINES),
        (DAY2_LOG, DAY2_EXPECTED_LINES),
    ],
)
def test_each_access_log_has_exact_expected_contents(path, expected_lines):
    # Length and exact line-by-line comparison.
    actual_lines = _read_lines(path)
    assert (
        len(actual_lines) == 5
    ), f"{path} should contain exactly 5 lines, found {len(actual_lines)}."

    assert (
        actual_lines == expected_lines
    ), f"Contents of {path} do not match the expected snapshot."

    # Verify pure LF endings (no CR bytes).
    assert _no_cr_bytes(
        path
    ), f"{path} contains carriage-return characters (CR); expected LF line endings only."


def test_reports_directory_does_not_yet_exist():
    """
    Before the student starts, the `reports` directory (and any output files
    within it) must *not* exist.  We enforce this to signal a clean slate.
    """
    assert not REPORTS_DIR.exists(), (
        "The directory /home/user/project/reports already exists, but it "
        "should be created by the learner's solution script."
    )