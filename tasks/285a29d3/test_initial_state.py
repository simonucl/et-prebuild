# test_initial_state.py
#
# Pytest suite to validate the initial operating-system / filesystem state
# BEFORE the student starts working on the “backup summary” exercise.
#
# This file checks ONLY the prerequisites (input directory / file and their
# exact contents).  It deliberately does NOT check for any output files or
# directories that the student will create later.
#
# Requirements verified:
#   1. /home/user/backup/logs            (directory, mode 755)
#   2. /home/user/backup/logs/restore_2024-05-17.log  (file, mode 644,
#      exact 6-line content as specified)
#
# If any assertion fails, the accompanying message pin-points what is wrong
# so the learner knows exactly which prerequisite is missing or malformed.

import os
import stat
import pytest

# Constants --------------------------------------------------------------

LOGS_DIR = "/home/user/backup/logs"
RESTORE_LOG = os.path.join(LOGS_DIR, "restore_2024-05-17.log")

EXPECTED_LOG_CONTENT = (
    "[2024-05-17 10:15:21] INFO  Restored: /var/data/customer1.db\n"
    "[2024-05-17 10:15:22] ERROR Restore failed: /var/data/customer2.db - checksum mismatch\n"
    "[2024-05-17 10:15:23] INFO  Restored: /var/data/customer3.db\n"
    "[2024-05-17 10:15:25] INFO  Restored: /var/data/reports/2024_Q2.pdf\n"
    "[2024-05-17 10:15:27] ERROR Restore failed: /var/data/archive/2023.tar.gz - file missing\n"
    "[2024-05-17 10:15:30] INFO  Restored: /var/data/media/image1.png\n"
)

# Helper -----------------------------------------------------------------

def _mode(path: str) -> int:
    """
    Return only the permission bits of a filesystem object, equivalent to
    the symbolic permissions you would see with `ls -l` (e.g. 0o755).
    """
    return stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)

# Tests ------------------------------------------------------------------

def test_logs_directory_exists_and_permissions():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory missing: {LOGS_DIR}"
    )
    actual_mode = _mode(LOGS_DIR)
    expected_mode = 0o755
    assert actual_mode == expected_mode, (
        f"Directory {LOGS_DIR} must have mode 755 "
        f"(found {oct(actual_mode)})"
    )

def test_restore_log_file_exists_and_permissions():
    assert os.path.isfile(RESTORE_LOG), (
        f"Required log file missing: {RESTORE_LOG}"
    )
    actual_mode = _mode(RESTORE_LOG)
    expected_mode = 0o644
    assert actual_mode == expected_mode, (
        f"Log file {RESTORE_LOG} must have mode 644 "
        f"(found {oct(actual_mode)})"
    )

def test_restore_log_file_exact_content():
    with open(RESTORE_LOG, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert content == EXPECTED_LOG_CONTENT, (
        "The content of the restore log does not match the expected "
        "pre-exercise state.\n\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )

@pytest.mark.parametrize(
    "line_no, expected_line",
    [(idx + 1, line) for idx, line in enumerate(EXPECTED_LOG_CONTENT.splitlines())],
)
def test_each_line_matches_expected(line_no, expected_line):
    """
    A more granular check that pinpoints exactly which line differs if the
    whole-file comparison above fails.  Each line (without its newline)
    must match the specification.
    """
    with open(RESTORE_LOG, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert line_no <= len(lines), (
        f"Log file {RESTORE_LOG} should have at least {line_no} lines "
        f"(found only {len(lines)})"
    )
    assert lines[line_no - 1] == expected_line, (
        f"Line {line_no} of {RESTORE_LOG} is incorrect.\n\n"
        f"Expected: {expected_line!r}\n"
        f"Found   : {lines[line_no - 1]!r}"
    )