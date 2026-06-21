# test_initial_state.py
#
# This pytest suite validates the workstation’s initial filesystem state
# before the student runs any commands.  It checks that:
#
# 1. The directory /home/user/logs exists and has 0755 permissions.
# 2. The file  /home/user/logs/system.log exists, has 0644 permissions,
#    and contains *exactly* the five expected log lines (newline-terminated).
#
# NOTE:  Output artefacts such as
#        /home/user/logs/incident_ERRORs_20230515.log
#        are deliberately *not* tested here, because they should not exist
#        prior to the student’s action.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
SYSTEM_LOG = LOG_DIR / "system.log"

EXPECTED_SYSTEM_LOG_LINES = [
    "[2023-05-15 10:03:17] [INFO] System booting\n",
    "[2023-05-15 10:05:42] [ERROR] Failed to mount /dev/sda1\n",
    "[2023-05-15 10:07:03] [WARNING] Low disk space\n",
    "[2023-05-15 10:12:55] [ERROR] Network unreachable\n",
    "[2023-05-15 10:15:00] [INFO] User login: alice\n",
]


def _mode(path: Path) -> int:
    """Return the permission bits (e.g., 0o755) for the given path."""
    return stat.S_IMODE(path.stat().st_mode)


def test_logs_directory_exists_and_permissions():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _mode(LOG_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{LOG_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


def test_system_log_exists_permissions_and_contents():
    assert SYSTEM_LOG.exists(), f"Required file {SYSTEM_LOG} is missing."
    assert SYSTEM_LOG.is_file(), f"{SYSTEM_LOG} exists but is not a regular file."

    expected_mode = 0o644
    actual_mode = _mode(SYSTEM_LOG)
    assert (
        actual_mode == expected_mode
    ), f"{SYSTEM_LOG} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."

    # Read and validate file contents exactly.
    with SYSTEM_LOG.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert (
        lines == EXPECTED_SYSTEM_LOG_LINES
    ), (
        f"{SYSTEM_LOG} contents do not match the expected log lines.\n"
        f"Expected ({len(EXPECTED_SYSTEM_LOG_LINES)} lines):\n"
        + "".join(EXPECTED_SYSTEM_LOG_LINES)
        + "\nGot ({len(lines)} lines):\n"
        + "".join(lines)
    )


@pytest.mark.skip(reason="Output artefacts are intentionally not tested in the initial state.")
def test_placeholder_for_output_file():
    """
    This test is intentionally skipped to remind future maintainers
    that the output file must NOT exist before the student runs their command.
    """
    pass