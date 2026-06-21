# test_initial_state.py
#
# Pytest suite to validate the initial operating-system / filesystem state
# BEFORE the student begins the task.  These tests assert that:
#   • /home/user/devops exists
#   • /home/user/devops/server.log exists, has mode 644 and contains the
#     expected seven lines (and only those seven lines)
#   • The output files that the student must create
#       – /home/user/devops/security_alerts.log
#       – /home/user/devops/blacklist.txt
#     do NOT yet exist
#
# If any assertion fails, the error message will explain what is wrong so the
# learner can correct the environment before proceeding.

import os
import stat
import textwrap
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants (full, absolute paths only)
# --------------------------------------------------------------------------- #
DEVOPS_DIR            = Path("/home/user/devops")
SERVER_LOG            = DEVOPS_DIR / "server.log"
SECURITY_ALERTS_LOG   = DEVOPS_DIR / "security_alerts.log"
BLACKLIST_TXT         = DEVOPS_DIR / "blacklist.txt"

EXPECTED_SERVER_LOG_CONTENT = textwrap.dedent(
    """\
    2024-05-15 10:01:22 INFO User login succeeded: user=alice ip=192.168.1.10
    2024-05-15 10:05:03 SECURITY ALERT Failed password attempt: user=root ip=203.0.113.45
    2024-05-15 10:07:45 ERROR Database connection timeout
    2024-05-15 10:12:11 SECURITY ALERT Multiple invalid login attempts: user=bob ip=198.51.100.23
    2024-05-15 10:15:55 INFO Cron job finished
    2024-05-15 10:17:20 SECURITY ALERT Failed password attempt: user=carol ip=203.0.113.45
    2024-05-15 10:20:00 INFO Backup completed
    """
).splitlines(keepends=False)   # results in a list of seven lines


# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #
def _file_mode(path: Path) -> int:
    """Return the permission bits (e.g., 0o644) of a file or directory."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_devops_directory_exists():
    assert DEVOPS_DIR.is_dir(), f"Required directory missing: {DEVOPS_DIR}"


def test_server_log_exists_and_mode():
    assert SERVER_LOG.is_file(), f"Required file missing: {SERVER_LOG}"
    mode = _file_mode(SERVER_LOG)
    assert mode == 0o644, (
        f"{SERVER_LOG} should have permission mode 644, "
        f"but is {oct(mode)}"
    )


def test_server_log_contents_exact():
    contents = SERVER_LOG.read_text(encoding="utf-8").splitlines(keepends=False)
    assert contents == EXPECTED_SERVER_LOG_CONTENT, (
        f"{SERVER_LOG} does not contain the expected contents.\n"
        f"Expected ({len(EXPECTED_SERVER_LOG_CONTENT)} lines):\n"
        + "\n".join(EXPECTED_SERVER_LOG_CONTENT)
        + "\n\nActual ({len(contents)} lines):\n"
        + "\n".join(contents)
    )


def test_output_files_do_not_yet_exist():
    for path in (SECURITY_ALERTS_LOG, BLACKLIST_TXT):
        assert not path.exists(), (
            f"{path} should NOT exist before the task is performed."
        )