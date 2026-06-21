# test_initial_state.py
#
# This test-suite validates that the container is in the **initial** state
# expected **before** the student runs any of the tasks described in the
# assignment.  In short, we check that
#
#   1. The directory `/home/user/build_checks` is *not* a regular file
#      (it may be absent or already be a directory––both are acceptable).
#   2. The file  `/home/user/build_checks/dns_resolution.log` does **not**
#      yet exist – the student will create it.
#   3. The system resolver already maps the hostname ``localhost`` to
#      ``127.0.0.1``.  The student will query this and record the result.
#
# Any failure message should make it very clear what is wrong with the
# starting environment.

import os
import stat
import socket
from pathlib import Path

import pytest


BUILD_DIR = Path("/home/user/build_checks")
LOG_FILE = BUILD_DIR / "dns_resolution.log"
EXPECTED_IP = "127.0.0.1"


def _is_world_executable(mode: int) -> bool:
    """Return True if 'others' have execute permission."""
    return bool(mode & stat.S_IXOTH)


@pytest.mark.describe("Pre-task filesystem state")
class TestInitialFilesystemState:
    def test_build_checks_dir_is_absent_or_directory(self):
        """
        The path /home/user/build_checks must NOT be a regular file.
        It can be absent (typical) or already be a directory.
        """
        if BUILD_DIR.exists():
            assert BUILD_DIR.is_dir(), (
                f"Expected {BUILD_DIR} either to be absent or a directory, "
                "but a non-directory file is present. Please remove/rename it."
            )

            # If the directory already exists, ensure it is traversable.
            mode = BUILD_DIR.stat().st_mode
            assert _is_world_executable(mode), (
                f"{BUILD_DIR} exists but lacks execute ('x') permission for "
                "at least one user class.  Expected mode 755 or more permissive."
            )

    def test_dns_resolution_log_does_not_exist_yet(self):
        """
        The log file must NOT exist before the student creates it.
        """
        assert not LOG_FILE.exists(), (
            f"Found unexpected file: {LOG_FILE}.  The exercise expects this "
            "file to be created *by the student*, so it must not exist at the "
            "start of the task."
        )


@pytest.mark.describe("System resolver sanity check")
def test_localhost_resolves_to_127_0_0_1():
    """
    Sanity-check the OS resolver: 'localhost' should resolve to 127.0.0.1.
    This must already be true; otherwise the student's subsequent log file
    would contain the wrong address.
    """
    resolved_ip = socket.gethostbyname("localhost")
    assert resolved_ip == EXPECTED_IP, (
        "The hostname 'localhost' does not resolve to 127.0.0.1 "
        f"(got {resolved_ip}).  Please fix /etc/hosts or the resolver "
        "configuration before running the exercise."
    )