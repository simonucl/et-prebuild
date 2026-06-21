# test_initial_state.py
#
# Pytest suite that verifies the machine is in the **initial** (pre-task)
# state for the “deployment SSH key-pair” exercise.
#
# The key-pair, its public deployment entry, and the setup log **must not**
# exist yet.  Only the user’s ~/.ssh directory is expected to be present.

import subprocess
from pathlib import Path

import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIVATE_KEY = SSH_DIR / "project_dev_rsa"
PUBLIC_KEY = SSH_DIR / "project_dev_rsa.pub"

PROJECT_DIR = HOME / "project"
ACCESS_DIR = PROJECT_DIR / ".access"
AUTHORIZED_DEVS = ACCESS_DIR / "authorized_devs"

LOG_FILE = HOME / "ssh_setup.log"

COMMENT_STRING = "project_dev@example.com"


def run_cmd(cmd):
    """
    Helper that runs `cmd` and returns (rc, stdout, stderr)
    without raising; keeps the test code compact.
    """
    proc = subprocess.run(
        cmd, shell=False, capture_output=True, text=True, check=False
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_ssh_directory_exists():
    """
    The base ~/.ssh directory must already be present; if it is missing
    something is very wrong with the container image.
    """
    assert SSH_DIR.is_dir(), (
        f"Expected directory {SSH_DIR} to exist but it is missing."
    )


@pytest.mark.parametrize(
    "path,expected_mode",
    [
        (PRIVATE_KEY, "600"),
        (PUBLIC_KEY, "644"),
    ],
)
def test_key_files_absent(path, expected_mode):
    """
    Neither the private key nor the public key should exist before
    the student starts the task.
    """
    assert not path.exists(), (
        f"{path} unexpectedly exists. The workspace should not yet contain "
        f"the deployment key-pair."
    )


def test_authorized_devs_does_not_contain_comment():
    """
    The project's authorized_devs file (if it exists) must NOT yet contain
    the new key-pair's comment string.  If the file does not exist at all,
    that is also acceptable for the initial state.
    """
    if not AUTHORIZED_DEVS.exists():
        pytest.skip(
            f"{AUTHORIZED_DEVS} does not exist yet — this is fine for the "
            "initial state."
        )

    content = AUTHORIZED_DEVS.read_text().splitlines()
    matches = [line for line in content if COMMENT_STRING in line]
    assert not matches, (
        f"{AUTHORIZED_DEVS} already contains a line with the comment "
        f"‘{COMMENT_STRING}’.  The student has apparently already modified "
        "the file, which should not be the case in the initial state."
    )


def test_setup_log_absent():
    """
    The summary log should only appear **after** the student performs the
    required steps.
    """
    assert not LOG_FILE.exists(), (
        f"Unexpected log file {LOG_FILE} found.  The setup actions seem to "
        "have been run already, but this test suite checks the pre-task "
        "state."
    )