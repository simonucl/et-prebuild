# test_initial_state.py
#
# This test-suite verifies that the operating-system’s starting state is
# completely clean with respect to the “uptime_monitor” SSH key-pair that the
# student is about to create.  NONE of the artefacts required by the task
# should exist yet.  If *any* of them are already present, the environment is
# considered contaminated and the tests will fail with a clear explanation.
#
# NOTE: These tests purposefully assert the *absence* of the files and
# configuration that the student is going to add later.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIV_KEY = SSH_DIR / "uptime_monitor"
PUB_KEY = SSH_DIR / "uptime_monitor.pub"
AUTH_KEYS = SSH_DIR / "authorized_keys"
LOG_FILE = HOME / "monitor_key_setup.log"

MONITOR_COMMENT = "uptime_monitor"


def _file_mode(path: Path) -> int:
    """
    Return the UNIX permission bits (e.g. 0o600) for ``path`` without the file
    type bits.  If the path does not exist, raise FileNotFoundError.
    """
    st_mode = path.stat().st_mode
    # Mask out file-type bits, keep permission bits only.
    return stat.S_IMODE(st_mode)


@pytest.fixture(scope="session")
def ssh_dir_exists():
    """
    Return True if ~/.ssh exists; False otherwise.  This helper allows tests to
    branch depending on whether the directory is pre-existing.
    """
    return SSH_DIR.exists()


def test_uptime_monitor_private_key_does_not_exist():
    """/home/user/.ssh/uptime_monitor must NOT exist yet."""
    assert not PRIV_KEY.exists(), (
        f"Found unexpected private key at {PRIV_KEY}. "
        "The environment should be clean before the student starts."
    )


def test_uptime_monitor_public_key_does_not_exist():
    """/home/user/.ssh/uptime_monitor.pub must NOT exist yet."""
    assert not PUB_KEY.exists(), (
        f"Found unexpected public key at {PUB_KEY}. "
        "The environment should be clean before the student starts."
    )


def test_monitor_log_file_does_not_exist():
    """/home/user/monitor_key_setup.log must NOT exist yet."""
    assert not LOG_FILE.exists(), (
        f"Found unexpected log file at {LOG_FILE}. "
        "The environment should be clean before the student starts."
    )


def test_authorized_keys_is_clean_of_uptime_monitor():
    """
    If ~/.ssh/authorized_keys exists already, it must NOT yet contain any entry
    whose comment is literally 'uptime_monitor' (nor the exact public key line
    once produced by the task).
    """
    if not AUTH_KEYS.exists():
        # Nothing to test if the file isn't there yet.
        pytest.skip("authorized_keys does not exist yet — this is acceptable.")
    else:
        try:
            with AUTH_KEYS.open("r", encoding="utf-8") as fh:
                for lineno, line in enumerate(fh, start=1):
                    stripped = line.rstrip("\n")
                    # Quick check for the literal comment; avoids parsing the
                    # key structure in detail.
                    if stripped.endswith(MONITOR_COMMENT):
                        pytest.fail(
                            f"Line {lineno} in {AUTH_KEYS} already ends with "
                            f"the comment '{MONITOR_COMMENT}'. "
                            "The uptime_monitor key must not be present before "
                            "the student creates it."
                        )
        except UnicodeDecodeError:
            pytest.fail(
                f"Could not read {AUTH_KEYS} as UTF-8. "
                "Ensure the file is text so it can be inspected."
            )


def test_existing_ssh_directory_permissions_are_flexible(ssh_dir_exists):
    """
    The task will ultimately require ~/.ssh to be 0700, but it is acceptable
    for the directory to carry *any* permissions at the initial state.
    This test merely documents its presence or absence for debugging clarity.
    """
    if ssh_dir_exists:
        mode = _file_mode(SSH_DIR)
        # No assert on the mode; just emit diagnostic info in test output.
        print(f"Pre-existing ~/.ssh directory found with mode {oct(mode)}")
    else:
        print("No ~/.ssh directory exists yet — this is acceptable.")