# test_initial_state.py
#
# This pytest suite validates the state of the operating-system / filesystem
# *before* the student begins any work.  It confirms that the expected
# directories and files exist (or do *not* exist) exactly as described in the
# task prompt so that subsequent grading logic can rely on a known baseline.
#
# Only Python stdlib + pytest are used.

import os
import stat
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
PROJECTS_DIR = HOME / "projects"
CONFMON_DIR = PROJECTS_DIR / "confmon"
LOGS_DIR = CONFMON_DIR / "logs"
REPORTS_DIR = CONFMON_DIR / "reports"

LOG_FILE = LOGS_DIR / "config_changes.log"

CSV_REPORT = REPORTS_DIR / "nov_2022_jdoe_changes.csv"
COUNT_REPORT = REPORTS_DIR / "nov_2022_jdoe_changes.count"

# Exact expected contents of the pre-existing log file
EXPECTED_LOG_CONTENT = (
    "2022-11-01 09:15:32 | jdoe | MODIFY | /etc/nginx/nginx.conf | SUCCESS\n"
    "2022-11-01 10:45:03 | bgates | MODIFY | /etc/ssh/sshd_config | SUCCESS\n"
    "2022-11-02 14:11:27 | jdoe | DELETE | /etc/apache2/sites-enabled/000-default.conf | SUCCESS\n"
    "2022-10-31 12:00:00 | jdoe | MODIFY | /etc/passwd | FAILED\n"
    "2022-11-15 16:42:05 | root | CREATE | /etc/sysctl.conf | SUCCESS\n"
    "2022-11-20 08:22:18 | jdoe | MODIFY | /etc/nginx/nginx.conf | SUCCESS\n"
    "2022-11-20 08:23:18 | jdoe | MODIFY | /etc/nginx/mime.types | SUCCESS\n"
    "2022-11-30 23:59:59 | jdoe | DELETE | /etc/cron.d/backup | SUCCESS\n"
    "2022-12-01 00:00:00 | jdoe | MODIFY | /etc/hosts | SUCCESS\n"
    "2022-11-22 11:11:11 | alice | DELETE | /etc/ssh/ssh_config | FAILED\n"
)
EXPECTED_LOG_NUM_LINES = 10


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def _assert_mode(path: Path, expected_mode: int) -> None:
    """
    Assert that `path`'s permission bits (lowest 3 octal digits) equal
    `expected_mode`.  Provide a clear message on mismatch.
    """
    mode = stat.S_IMODE(path.stat().st_mode)
    assert (
        mode == expected_mode
    ), f"Permissions for {path} are {oct(mode)}, expected {oct(expected_mode)}"


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


def test_required_directories_exist():
    """
    The four required directories must already exist.
    """
    for d in (PROJECTS_DIR, CONFMON_DIR, LOGS_DIR, REPORTS_DIR):
        assert d.exists(), f"Required directory {d} is missing"
        assert d.is_dir(), f"Expected {d} to be a directory"


def test_reports_directory_is_empty_initially():
    """
    /home/user/projects/confmon/reports/ must start empty—no files yet.
    """
    contents = list(REPORTS_DIR.iterdir())
    assert (
        not contents
    ), f"{REPORTS_DIR} should be empty before the student runs anything, but found: {[p.name for p in contents]}"


def test_log_file_exists_and_is_regular():
    """
    The master audit log must exist and be a regular, world-readable file.
    """
    assert LOG_FILE.exists(), f"Log file {LOG_FILE} is missing"
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file"
    # The problem statement shows all files should be 0644; enforce that here.
    _assert_mode(LOG_FILE, 0o644)


def test_log_file_contents_match_exactly():
    """
    The audit log must contain exactly the 10 specified lines including the
    trailing newline character on each line.
    """
    log_text = LOG_FILE.read_text(encoding="utf-8")
    assert (
        log_text == EXPECTED_LOG_CONTENT
    ), "Contents of config_changes.log do not match the expected baseline"

    # Redundant but explicit sanity check on line count
    assert (
        log_text.count("\n") == EXPECTED_LOG_NUM_LINES
    ), f"Expected {EXPECTED_LOG_NUM_LINES} lines in the log, found {log_text.count(chr(10))}"


def test_output_files_do_not_yet_exist():
    """
    The two result files must *not* be present at the start.
    """
    for path in (CSV_REPORT, COUNT_REPORT):
        assert not path.exists(), f"Output file {path} should not exist before the task runs"