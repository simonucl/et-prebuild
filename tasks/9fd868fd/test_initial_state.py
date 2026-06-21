# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “restore log alert view” task *before* the student performs
# any actions.
#
# What is checked:
#   1. /home/user/logs exists and has 0o755 permissions.
#   2. /home/user/logs/restore.log exists, is readable, has 0o644 permissions,
#      is pure UTF-8 text with Unix line-endings, and its contents are *exactly*
#      the nine lines specified in the task description (no more, no less).
#
# Nothing related to the output artefacts (e.g. restore_alerts.log) is tested
# here, by design.

import os
import stat
import pytest


LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "restore.log")

EXPECTED_LINES = [
    "2023-09-10 12:45:27 | INFO  | Restore started for backup set ID=BK20230910A",
    "2023-09-10 12:46:00 | WARN  | Missing incremental file inc-20230909-02.delta",
    "2023-09-10 12:46:05 | INFO  | Attempting partial restore",
    "2023-09-10 12:47:10 | ERROR | Restore failed with code ERR42",
    "2023-09-10 12:47:45 | INFO  | Clean-up finished",
    "2023-09-11 08:10:32 | INFO  | Restore started for backup set ID=BK20230911A",
    "2023-09-11 08:10:55 | WARN  | File changed during restore: /var/lib/data/app.db",
    "2023-09-11 08:12:23 | ERROR | Restore aborted due to checksum mismatch",
    "2023-09-11 08:13:00 | INFO  | Sending failure report email",
]


def _mode(path):
    """Return the permission bits (e.g. 0o755) of a file or directory."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_logs_directory_exists_and_perms():
    assert os.path.isdir(LOG_DIR), f"Required directory {LOG_DIR} is missing."
    expected_perm = 0o755
    actual_perm = _mode(LOG_DIR)
    assert (
        actual_perm == expected_perm
    ), f"Directory {LOG_DIR} must have permissions {oct(expected_perm)}, got {oct(actual_perm)}."


def test_restore_log_exists_and_perms():
    assert os.path.isfile(LOG_FILE), f"Required file {LOG_FILE} is missing."
    expected_perm = 0o644
    actual_perm = _mode(LOG_FILE)
    assert (
        actual_perm == expected_perm
    ), f"File {LOG_FILE} must have permissions {oct(expected_perm)}, got {oct(actual_perm)}."


def test_restore_log_content_exact():
    # --- Validate UTF-8 decoding and content ---------
    try:
        with open(LOG_FILE, encoding="utf-8") as fh:
            contents = fh.read()
    except UnicodeDecodeError as e:
        pytest.fail(f"{LOG_FILE} is not valid UTF-8: {e}")

    # Ensure Unix line-endings only (no '\r\n')
    assert "\r" not in contents, f"{LOG_FILE} must use Unix (LF) line-endings only."

    lines = contents.splitlines()
    assert (
        lines == EXPECTED_LINES
    ), (
        f"{LOG_FILE} content mismatch.\n"
        f"Expected exactly these {len(EXPECTED_LINES)} lines:\n"
        + "\n".join(EXPECTED_LINES)
        + "\n---\n"
        f"Found {len(lines)} lines:\n"
        + "\n".join(lines)
    )