# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state before the student starts working on the task.  It ensures that
# the supplied log file and directory layout are present and correct, and
# that none of the artefacts that the student is supposed to create exist
# yet.
#
# Only Python stdlib + pytest are used.

import os
import stat
import re
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
ACCESS_LOG = LOG_DIR / "access.log"

ANALYSIS_DIR = Path("/home/user/analysis")
ARTEFACT_404_BY_IP = ANALYSIS_DIR / "404_by_ip.txt"
ARTEFACT_TOP10 = ANALYSIS_DIR / "top10_endpoints.txt"
ARTEFACT_STATUS = ANALYSIS_DIR / "status_codes.csv"
SANITIZED_LOG = LOG_DIR / "access_sanitized.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _file_mode(path: Path) -> int:
    """Return the file permission bits similar to `ls -l` (e.g. 0o644)."""
    return path.stat().st_mode & 0o777


def _parse_status_codes(lines):
    """
    Very small Apache 'combined' parser that extracts the numeric status code
    (the field that comes immediately after the quoted request).
    """
    status_counts = {}
    rx = re.compile(r'"\w+ [^"]+ HTTP/[^"]+" (?P<status>\d{3}) ')
    for idx, line in enumerate(lines, 1):
        m = rx.search(line)
        assert m, (f"Line {idx} of {ACCESS_LOG} does not look like a valid "
                   "Apache combined log entry")
        status = int(m.group("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
    return status_counts


# --------------------------------------------------------------------------- #
# Tests for the *existing* log directory and log file
# --------------------------------------------------------------------------- #
def test_log_directory_exists_and_has_correct_permissions():
    assert LOG_DIR.exists(), f"{LOG_DIR} directory is missing"
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory"
    expected_mode = 0o755
    actual_mode = _file_mode(LOG_DIR)
    assert actual_mode == expected_mode, (
        f"{LOG_DIR} should have permissions {oct(expected_mode)}, "
        f"found {oct(actual_mode)}"
    )


def test_access_log_exists_with_correct_permissions():
    assert ACCESS_LOG.exists(), f"Required log file {ACCESS_LOG} is missing"
    assert ACCESS_LOG.is_file(), f"{ACCESS_LOG} exists but is not a regular file"
    expected_mode = 0o644
    actual_mode = _file_mode(ACCESS_LOG)
    assert actual_mode == expected_mode, (
        f"{ACCESS_LOG} should have permissions {oct(expected_mode)}, "
        f"found {oct(actual_mode)}"
    )


def test_access_log_content_is_exactly_30_lines_and_intact():
    lines = ACCESS_LOG.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 30, (
        f"{ACCESS_LOG} should have exactly 30 lines, found {len(lines)}"
    )

    # Quick sanity check on first and last line so we know the right file
    assert lines[0].startswith("192.168.1.10 "), (
        f"The first line of {ACCESS_LOG} is not as expected:\n{lines[0]}"
    )
    assert lines[-1].startswith("192.168.1.10 "), (
        f"The last line of {ACCESS_LOG} is not as expected:\n{lines[-1]}"
    )

    # Check that line endings are Unix (LF) only.
    raw_bytes = ACCESS_LOG.read_bytes()
    assert b"\r\n" not in raw_bytes, (
        f"{ACCESS_LOG} must use LF line endings only (no CR characters found)"
    )

    # Check for the expected number of “GET /old-page” occurrences
    old_page_occurrences = sum(1 for l in lines if "GET /old-page" in l)
    assert old_page_occurrences == 6, (
        f"{ACCESS_LOG} should contain 6 occurrences of 'GET /old-page', "
        f"found {old_page_occurrences}"
    )

    # A basic distribution check of status codes so the grader knows the data
    expected_distribution = {200: 15, 201: 1, 301: 2, 404: 10, 500: 2}
    actual_distribution = _parse_status_codes(lines)
    assert actual_distribution == expected_distribution, (
        f"Status-code distribution in {ACCESS_LOG} is off.\n"
        f"Expected: {expected_distribution}\nActual:   {actual_distribution}"
    )


# --------------------------------------------------------------------------- #
# Tests that ensure *student output files do NOT yet exist*
# --------------------------------------------------------------------------- #
def test_analysis_output_files_do_not_yet_exist():
    for artefact in [ARTEFACT_404_BY_IP, ARTEFACT_TOP10, ARTEFACT_STATUS]:
        assert not artefact.exists(), (
            f"{artefact} should NOT exist before the student runs their solution"
        )


def test_sanitized_log_does_not_yet_exist():
    assert not SANITIZED_LOG.exists(), (
        f"{SANITIZED_LOG} should NOT exist before the student runs their solution"
    )