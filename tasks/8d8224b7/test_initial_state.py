# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student runs their solution command.
#
# Requirements verified:
#   1. Directory /home/user/db_logs/ exists and has 0o755 permissions.
#   2. File     /home/user/db_logs/queries.log exists with 0o644 permissions.
#   3. The file contains exactly the eight expected lines (including order).
#
# NOTE:  We deliberately do NOT check for the presence or absence of the
#        expected result file `/home/user/db_logs/slow_queries_20240601.log`
#        in order to comply with the grading-framework rules.

import os
import stat
import pytest

DIR_PATH = "/home/user/db_logs"
LOG_PATH = os.path.join(DIR_PATH, "queries.log")

EXPECTED_LINES = [
    "2024-06-01 09:12:11 | SELECT * FROM users; | 234ms\n",
    "2024-06-01 09:12:12 | SELECT * FROM orders WHERE price > 100; | 1245ms\n",
    "2024-06-01 09:12:13 | UPDATE users SET name='Alice' WHERE id=5; | 67ms\n",
    "2024-06-01 09:12:14 | SELECT * FROM transactions WHERE status='failed'; | 5344ms\n",
    "2024-06-01 09:12:15 | DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '1 day'; | 908ms\n",
    "2024-06-01 09:12:16 | SELECT COUNT(*) FROM users; | 321ms\n",
    "2024-06-01 09:12:17 | INSERT INTO logs(message) VALUES('test'); | 45ms\n",
    "2024-06-01 09:12:18 | SELECT * FROM orders WHERE status='pending'; | 1023ms\n",
]

def octal_mode(path: str) -> int:
    """Return the permission bits of `path` as an octal integer (e.g. 0o644)."""
    return stat.S_IMODE(os.stat(path).st_mode)

def test_logs_directory_exists_with_correct_permissions():
    assert os.path.isdir(DIR_PATH), (
        f"Required directory '{DIR_PATH}' is missing."
    )
    mode = octal_mode(DIR_PATH)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory '{DIR_PATH}' must have permissions {oct(expected_mode)}, "
        f"but has {oct(mode)}."
    )

def test_queries_log_exists_with_correct_permissions_and_content():
    assert os.path.isfile(LOG_PATH), (
        f"Required log file '{LOG_PATH}' is missing."
    )

    mode = octal_mode(LOG_PATH)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File '{LOG_PATH}' must have permissions {oct(expected_mode)}, "
        f"but has {oct(mode)}."
    )

    with open(LOG_PATH, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert lines == EXPECTED_LINES, (
        f"Contents of '{LOG_PATH}' do not match the expected template.\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{''.join(EXPECTED_LINES)}\n"
        f"Actual   ({len(lines)} lines):\n{''.join(lines)}"
    )