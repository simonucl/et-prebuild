# test_initial_state.py
#
# This pytest suite verifies that the operating-system state **before**
# the student starts working is exactly as expected.
#
# It checks only the *pre-existing* artefacts (no output files),
# in accordance with the project requirements.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONFIG_LOG = HOME / "config_changes.log"

# ---------------------------------------------------------------------------
# Canonical contents of /home/user/config_changes.log (must end with '\n')
# ---------------------------------------------------------------------------

EXPECTED_CONFIG_LOG_CONTENT = (
    "2024-06-01 10:15:23 HOST=web01 USER=root ACTION=CREATE TYPE=FILE PATH=/etc/nginx/nginx.conf\n"
    "2024-06-01 10:17:05 HOST=web01 USER=root ACTION=MODIFY TYPE=PERMISSION CMD=chmod 644 /etc/nginx/nginx.conf\n"
    "2024-06-01 10:20:10 HOST=db01 USER=admin ACTION=MODIFY TYPE=CONTENT CMD=vim /etc/mysql/my.cnf\n"
    "2024-06-01 10:21:22 HOST=web01 USER=root ACTION=MODIFY TYPE=PERMISSION CMD=chown root:root /etc/nginx/nginx.conf\n"
    "2024-06-01 10:23:45 HOST=web01 USER=root ACTION=DELETE TYPE=FILE PATH=/tmp/test.tmp\n"
    "2024-06-01 10:25:50 HOST=db01 USER=admin ACTION=MODIFY TYPE=PERMISSION CMD=chmod 600 /etc/mysql/my.cnf\n"
)

EXPECTED_CONFIG_LOG_HASH = hashlib.sha256(
    EXPECTED_CONFIG_LOG_CONTENT.encode("utf-8")
).hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_home_directory_exists():
    """Ensure the /home/user directory exists and is a directory."""
    assert HOME.exists(), (
        f"Expected home directory {HOME} to exist, but it does not."
    )
    assert HOME.is_dir(), (
        f"Expected {HOME} to be a directory, but it's not."
    )


def test_config_log_exists_and_is_file():
    """Ensure /home/user/config_changes.log exists as a regular file."""
    assert CONFIG_LOG.exists(), (
        f"Expected log file {CONFIG_LOG} to exist, but it does not."
    )
    assert CONFIG_LOG.is_file(), (
        f"Expected {CONFIG_LOG} to be a regular file, but it's not."
    )


def test_config_log_contents_match_exactly():
    """
    Verify that the contents of config_changes.log are *exactly* the
    canonical lines defined above (including the final newline).
    """
    actual_content = CONFIG_LOG.read_text(encoding="utf-8")
    assert actual_content.endswith("\n"), (
        f"{CONFIG_LOG} must end with a single trailing newline (\\n)."
    )

    actual_hash = hashlib.sha256(actual_content.encode("utf-8")).hexdigest()
    assert (
        actual_hash == EXPECTED_CONFIG_LOG_HASH
    ), (
        "Contents of {file} do not match the expected baseline.\n"
        "If the file was modified, revert it to the exact state shown in the "
        "task description.".format(file=CONFIG_LOG)
    )