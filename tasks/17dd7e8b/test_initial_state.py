# test_initial_state.py
#
# This test-suite verifies the **initial** filesystem state _before_ the
# student executes the single-command solution.  It confirms that the
# prerequisite directories and files exist with the correct contents /
# permissions, and that none of the **output** artefacts are present yet.

import os
import stat
from pathlib import Path

import pytest


HOME = Path("/home/user")

# Paths that must already exist
UTILS_DIR = HOME / "utils"
HEARTBEAT_SCRIPT = UTILS_DIR / "heartbeat.sh"
SYSTEMD_USER_DIR = HOME / ".config" / "systemd" / "user"

# Paths that must NOT exist prior to the student's command
SERVICE_FILE = SYSTEMD_USER_DIR / "my_utility.service"
LOG_FILE = HOME / "my_utility_service_creation.log"


@pytest.fixture(scope="module")
def heartbeat_contents():
    """Return the expected (canonical) contents of heartbeat.sh."""
    return (
        "#!/usr/bin/env bash\n"
        'date +"%Y-%m-%d %H:%M:%S - heartbeat"\n'
    )


def test_utils_directory_exists_and_perms():
    assert UTILS_DIR.is_dir(), (
        f"Required directory {UTILS_DIR} does not exist. "
        "It should be present before running the task."
    )

    mode = UTILS_DIR.stat().st_mode & 0o777
    assert mode == 0o755, (
        f"Directory {UTILS_DIR} should have permissions 755 "
        f"but has {oct(mode)}."
    )


def test_heartbeat_script_exists_is_executable_and_contents(heartbeat_contents):
    assert HEARTBEAT_SCRIPT.is_file(), (
        f"Required script {HEARTBEAT_SCRIPT} is missing."
    )

    # Executable check
    assert os.access(HEARTBEAT_SCRIPT, os.X_OK), (
        f"Script {HEARTBEAT_SCRIPT} must be executable."
    )

    # Content check, byte-for-byte
    actual = HEARTBEAT_SCRIPT.read_text(encoding="utf-8")
    assert actual == heartbeat_contents, (
        f"Script {HEARTBEAT_SCRIPT} does not have the expected contents.\n"
        "Expected:\n"
        f"{heartbeat_contents!r}\nGot:\n{actual!r}"
    )


def test_systemd_user_directory_exists_and_perms():
    assert SYSTEMD_USER_DIR.is_dir(), (
        f"Directory {SYSTEMD_USER_DIR} should exist before the task begins."
    )

    mode = SYSTEMD_USER_DIR.stat().st_mode & 0o777
    assert mode == 0o700, (
        f"Directory {SYSTEMD_USER_DIR} should have permissions 700 "
        f"but has {oct(mode)}."
    )


@pytest.mark.parametrize("path", [SERVICE_FILE, LOG_FILE])
def test_output_files_do_not_preexist(path: Path):
    assert not path.exists(), (
        f"File {path} should NOT exist prior to running the student's single "
        "command. Its presence would indicate the task has already been "
        "performed or the environment is not clean."
    )