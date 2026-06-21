# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the student performs any actions for the “backup report”
# exercise.
#
# Rules enforced by this test file:
#   • The seven expected daily log files must exist under
#       /home/user/backups/logs
#     and their contents must match the ground-truth exactly.
#   • No report artefacts (failure_summary.csv, failure_events.log) should
#     exist yet in /home/user/backups/reports.
#   • Helpful assertion messages pinpoint what is missing or incorrect.
#
# Only standard library modules + pytest are used.

import os
import re
import pytest

LOG_DIR = "/home/user/backups/logs"
REPORT_DIR = "/home/user/backups/reports"

# --------------------------------------------------------------------------- #
# Ground-truth contents for the seven log files.  Each string intentionally
# ends with a single Unix LF to match the required exact byte content.
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENTS = {
    "backup_status_2023-08-01.log": (
        "host db1: SUCCESS (duration: 122s)\n"
        "host db2: FAILED (error: timeout)\n"
        "host db3: SUCCESS (duration: 130s)\n"
    ),
    "backup_status_2023-08-02.log": (
        "host db1: FAILED (error: disk full)\n"
        "host db2: FAILED (error: timeout)\n"
        "host db3: SUCCESS (duration: 128s)\n"
    ),
    "backup_status_2023-08-03.log": (
        "host db1: SUCCESS (duration: 120s)\n"
        "host db2: SUCCESS (duration: 121s)\n"
        "host db3: SUCCESS (duration: 125s)\n"
    ),
    "backup_status_2023-08-04.log": (
        "host db1: FAILED (error: network)\n"
        "host db2: SUCCESS (duration: 118s)\n"
        "host db3: FAILED (error: disk full)\n"
    ),
    "backup_status_2023-08-05.log": (
        "host db1: SUCCESS (duration: 119s)\n"
        "host db2: SUCCESS (duration: 117s)\n"
        "host db3: SUCCESS (duration: 124s)\n"
    ),
    "backup_status_2023-08-06.log": (
        "host db1: FAILED (error: timeout)\n"
        "host db2: FAILED (error: disk full)\n"
        "host db3: SUCCESS (duration: 123s)\n"
    ),
    "backup_status_2023-08-07.log": (
        "host db1: SUCCESS (duration: 118s)\n"
        "host db2: SUCCESS (duration: 116s)\n"
        "host db3: FAILED (error: network)\n"
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_file(path):
    """Return file contents as text (UTF-8)."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert os.path.isdir(
        LOG_DIR
    ), f"Required directory {LOG_DIR!r} is missing."


def test_exactly_seven_log_files_present():
    log_files = sorted(
        f for f in os.listdir(LOG_DIR) if re.match(r"^backup_status_\d{4}-\d{2}-\d{2}\.log$", f)
    )
    assert len(log_files) == 7, (
        f"Expected 7 log files in {LOG_DIR!r}, found {len(log_files)}: {log_files}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_LOG_CONTENTS.items())
def test_each_log_file_content_is_correct(filename, expected_content):
    full_path = os.path.join(LOG_DIR, filename)
    assert os.path.isfile(
        full_path
    ), f"Missing log file: {full_path}"
    actual = _read_file(full_path)
    assert (
        actual == expected_content
    ), f"Content mismatch in {full_path}. Check for exact text and trailing newline."


def test_report_directory_clean():
    """
    The student has not yet generated any reports.  Either the report directory
    does not exist or, if it does, it must not contain the target artefacts.
    """
    if not os.path.exists(REPORT_DIR):
        # All good — directory absent.
        return

    # Directory exists: make sure the two files are not there yet.
    forbidden_files = ["failure_summary.csv", "failure_events.log"]
    for fname in forbidden_files:
        full_path = os.path.join(REPORT_DIR, fname)
        assert not os.path.exists(
            full_path
        ), f"Report file {full_path!r} already exists but should not be present before the task is done."