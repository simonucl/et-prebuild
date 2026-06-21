# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the operating system /
# filesystem before the student runs any commands for the “configuration
# manager” task.  It confirms that the required log directory and log file are
# present with the correct permissions and **exact** content, while
# intentionally *not* checking for the output artefact
# (/home/user/config_logs/user_change_count.log).

import os
import stat
from pathlib import Path

import pytest


CONFIG_DIR = Path("/home/user/config_logs")
CHANGE_LOG = CONFIG_DIR / "changes.log"


@pytest.fixture(scope="module")
def change_log_contents():
    """
    Read the contents of changes.log once and share it across tests.
    """
    try:
        return CHANGE_LOG.read_text(encoding="utf-8")
    except FileNotFoundError:
        # Let the individual tests raise the more descriptive assertion.
        return ""


def test_config_dir_exists():
    assert CONFIG_DIR.exists(), (
        "Expected directory '/home/user/config_logs' does not exist."
    )
    assert CONFIG_DIR.is_dir(), (
        "'/home/user/config_logs' exists but is not a directory."
    )

    mode = CONFIG_DIR.stat().st_mode & 0o777
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory '/home/user/config_logs' should have permissions "
        f"0755, but has {oct(mode)}."
    )


def test_change_log_exists_and_is_file():
    assert CHANGE_LOG.exists(), (
        "Log file '/home/user/config_logs/changes.log' is missing."
    )
    assert CHANGE_LOG.is_file(), (
        "'/home/user/config_logs/changes.log' exists but is not a regular file."
    )

    mode = CHANGE_LOG.stat().st_mode & 0o777
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File '/home/user/config_logs/changes.log' should have permissions "
        f"0644, but has {oct(mode)}."
    )


def test_change_log_content_exact(change_log_contents):
    """
    Validate that changes.log contains exactly the eight expected lines
    (no more, no less), in the correct order and with no extra whitespace.
    """
    expected_lines = [
        "[2023-07-18 09:15:23] user=alice file=/etc/nginx/nginx.conf action=modified",
        "[2023-07-18 10:41:02] user=bob file=/etc/ssh/sshd_config action=modified",
        "[2023-07-19 08:20:17] user=alice file=/etc/nginx/sites-enabled/default action=created",
        "[2023-07-19 11:05:44] user=carol file=/etc/cron.d/backup action=deleted",
        "[2023-07-20 14:12:31] user=bob file=/etc/hosts action=modified",
        "[2023-07-21 07:55:09] user=alice file=/etc/nginx/nginx.conf action=modified",
        "[2023-07-21 12:00:00] user=carol file=/etc/passwd action=modified",
        "[2023-07-22 09:30:45] user=alice file=/etc/nginx/sites-available/site1 action=created",
    ]

    # Split without keeping the trailing newline so comparisons are exact.
    actual_lines = change_log_contents.splitlines()

    assert actual_lines == expected_lines, (
        "The contents of '/home/user/config_logs/changes.log' do not match the "
        "expected initial state.\n\n"
        "Expected:\n"
        + "\n".join(expected_lines)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )