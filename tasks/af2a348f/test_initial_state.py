# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student runs any commands.  It deliberately
# fails fast and with helpful error messages whenever something is
# missing or already modified.
#
# It checks:
#   1. Presence and permissions of /home/user/logs and combined.log
#   2. Exact contents (11 lines) of combined.log
#   3. Absence of /home/user/alerts and its expected output files

import os
import stat
import pytest
from pathlib import Path


HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
COMBINED_LOG = LOGS_DIR / "combined.log"
ALERTS_DIR = HOME / "alerts"
HIGH_SEVERITY = ALERTS_DIR / "high_severity.log"
STATS = ALERTS_DIR / "stats.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _mode(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o755) for *path*.
    """
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Expected data
# --------------------------------------------------------------------------- #
EXPECTED_LINES = [
    "2023-03-21 10:15:43,221 INFO  [AUTH] User login succeeded uid=233\n",
    "2023-03-21 10:16:02,101 ERROR [API] ERR4152 - Failed to fetch resource id=34\n",
    "2023-03-21 10:16:45,312 WARNING [DB] Connection slow, t=527ms\n",
    "2023-03-21 10:17:11,998 ERROR [API] ERR5021 - Null pointer exception id=78\n",
    "2023-03-21 10:17:45,902 CRITICAL [SECURITY] ERR9001 - Multiple failed login attempts uid=122\n",
    "2023-03-21 10:18:10,455 INFO  [SCHED] Job 18 completed in 1234ms\n",
    "2023-03-21 10:19:03,211 ERROR [DB] ERR3004 - Timeout while querying orders\n",
    "2023-03-21 10:20:47,599 CRITICAL [API] ERR5500 - Data corruption detected id=12\n",
    "2023-03-21 10:21:12,772 DEBUG [CACHE] Cache miss key=session:233\n",
    "2023-03-21 10:21:45,001 ERROR [FS] ERR6400 - Disk full path=/var/data\n",
    "2023-03-21 10:23:11,650 ERROR [API] ERR5021 - Null pointer exception id=78  # duplicate of an earlier line for deduplication testing\n",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists_and_has_correct_permissions():
    assert LOGS_DIR.exists(), (
        f"Required directory {LOGS_DIR} does not exist.\n"
        "The initial test harness should have created it."
    )
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
    mode = _mode(LOGS_DIR)
    assert mode == 0o755, (
        f"Directory {LOGS_DIR} has permissions {oct(mode)}, "
        "expected 0o755."
    )


def test_combined_log_exists_with_correct_permissions():
    assert COMBINED_LOG.exists(), f"Required file {COMBINED_LOG} is missing."
    assert COMBINED_LOG.is_file(), f"{COMBINED_LOG} exists but is not a regular file."
    mode = _mode(COMBINED_LOG)
    assert mode == 0o644, (
        f"File {COMBINED_LOG} has permissions {oct(mode)}, "
        "expected 0o644."
    )


def test_combined_log_has_expected_contents():
    with COMBINED_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    # Helpful diff if something is wrong
    assert actual_lines == EXPECTED_LINES, (
        f"{COMBINED_LOG} does not match the expected 11-line content.\n"
        "Differences:\n"
        + "".join(
            pytest.diffutil.unified_diff(
                EXPECTED_LINES, actual_lines, lineterm=""
            )
        )
    )


def test_alerts_directory_does_not_yet_exist():
    assert not ALERTS_DIR.exists(), (
        f"{ALERTS_DIR} already exists. The student should create it during "
        "task execution, but it must not be present at the start."
    )


def test_output_files_do_not_exist_yet():
    for path in (HIGH_SEVERITY, STATS):
        assert not path.exists(), (
            f"Output file {path} is already present. The student should "
            "generate it during the task, not beforehand."
        )