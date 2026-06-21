# test_initial_state.py
#
# Pytest suite that validates the _initial_ state of the file-system
# before the student begins working on the “web-log filtering” task.
#
# What we check:
#   1. The original Apache log exists at the expected absolute path and
#      contains the exact, unmodified eight lines supplied by the spec.
#   2. The target “filtered” directory and its two deliverable files do
#      NOT exist yet (they must be created by the student’s solution).
#
# Only stdlib + pytest are used.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
PROJECTS_DIR = HOME / "projects" / "weblog"
ORIGINAL_LOG = PROJECTS_DIR / "access.log"

FILTERED_DIR = PROJECTS_DIR / "filtered"
ANONYMIZED_LOG = FILTERED_DIR / "anonymized_access.log"
REPORT_FILE = FILTERED_DIR / "filter_report.txt"

# The canonical contents of the original access log, _including_ the
# trailing newline after the last line.
EXPECTED_ORIGINAL_LOG = (
    "93.184.216.34 - - [10/Jun/2024:13:55:36 +0000] "
    "\"GET /assets/logo.png HTTP/1.1\" 200 5321 \"https://example.com/\" \"Mozilla/5.0\"\n"
    "185.199.110.153 - - [10/Jun/2024:13:55:37 +0000] "
    "\"GET /api/user?id=42 HTTP/1.1\" 200 1234 \"-\" \"curl/8.5.0\"\n"
    "203.0.113.7 - - [10/Jun/2024:13:55:37 +0000] "
    "\"GET /assets/banner.JPG HTTP/1.1\" 200 23122 \"https://example.com/\" \"Mozilla/5.0\"\n"
    "203.0.113.7 - - [10/Jun/2024:13:55:38 +0000] "
    "\"GET /assets/banner.JPG HTTP/1.1\" 304 0 \"https://example.com/\" \"Mozilla/5.0\"\n"
    "192.0.2.44 - - [10/Jun/2024:13:55:39 +0000] "
    "\"POST /login HTTP/1.1\" 302 0 \"https://example.com/login\" \"Mozilla/5.0\"\n"
    "198.51.100.23 - - [10/Jun/2024:13:55:40 +0000] "
    "\"GET /assets/sprite.gif HTTP/1.1\" 200 998 \"https://example.com/\" \"Mozilla/5.0\"\n"
    "198.51.100.23 - - [10/Jun/2024:13:55:41 +0000] "
    "\"GET /assets/sprite.gif HTTP/1.1\" 404 209 \"https://example.com/\" \"Mozilla/5.0\"\n"
    "203.0.113.9 - - [10/Jun/2024:13:55:42 +0000] "
    "\"GET /assets/bg.jpeg HTTP/1.1\" 200 14231 \"https://example.com/\" \"Mozilla/5.0\"\n"
)


def test_original_log_exists():
    """Ensure the source log file is present before the task begins."""
    assert ORIGINAL_LOG.exists(), (
        f"Required log file missing: {ORIGINAL_LOG}"
    )
    assert ORIGINAL_LOG.is_file(), (
        f"Expected a regular file at {ORIGINAL_LOG}, but something else exists."
    )


def test_original_log_contents_exact_match():
    """
    The automated grader relies on the log being unmodified.
    Check that the file has exactly the eight expected lines.
    """
    contents = ORIGINAL_LOG.read_text(encoding="utf-8")
    assert contents == EXPECTED_ORIGINAL_LOG, (
        "The contents of access.log do not match the expected initial state.\n"
        "If you previously modified this file, restore it before continuing."
    )


def test_filtered_directory_not_yet_present():
    """
    The deliverables must not pre-exist.  Either the directory is absent
    or, if it does exist, it must not already contain the files that the
    student is supposed to create.
    """
    if not FILTERED_DIR.exists():
        # Ideal initial state: directory absent.
        return

    # If the directory is already here, ensure it does NOT contain
    # either of the deliverables.  Having other unrelated files would
    # also be suspicious, but we only guard against the two that matter.
    assert not ANONYMIZED_LOG.exists(), (
        f"File {ANONYMIZED_LOG} should NOT exist before the task starts."
    )
    assert not REPORT_FILE.exists(), (
        f"File {REPORT_FILE} should NOT exist before the task starts."
    )