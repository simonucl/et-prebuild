# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem state
# is ready for the student to carry out the exercise described in the
# assignment.  It purposefully does NOT look for any of the files the
# student is asked to create or modify (e.g. resolution.log).
#
# Checked pre-conditions:
#   1. The directory /home/user/projects/project-lambda/ exists.
#   2. That directory is writable by the current user.
#   3. The hostname "localhost" resolves to 127.0.0.1.
#   4. At least one common DNS-lookup CLI utility is available
#      (host, dig, nslookup or getent), so the student can choose which
#      one-liner they prefer.
#
# If any of these assertions fail, the error message will explain exactly
# what is missing or misconfigured.

from pathlib import Path
import os
import socket
import shutil
import stat
import pytest

PROJECT_DIR = Path("/home/user/projects/project-lambda")

@pytest.mark.describe("Pre-condition: required project directory exists")
def test_project_directory_exists():
    assert PROJECT_DIR.exists(), (
        f"Required directory '{PROJECT_DIR}' is missing. "
        "It must exist before the exercise begins."
    )
    assert PROJECT_DIR.is_dir(), (
        f"Path '{PROJECT_DIR}' exists but is not a directory."
    )

@pytest.mark.describe("Pre-condition: project directory is writable")
def test_project_directory_is_writable():
    # Use os.access with os.W_OK and additionally attempt to open a temp file
    # to ensure real write access (some filesystems may report W_OK yet be
    # read-only at runtime).
    assert os.access(PROJECT_DIR, os.W_OK), (
        f"Directory '{PROJECT_DIR}' is not writable by the current user."
    )
    test_file = PROJECT_DIR / ".pytest_write_test"
    try:
        with test_file.open("w") as fp:
            fp.write("write-test")
        # Verify file actually got created with the correct permissions
        st_mode = test_file.stat().st_mode
        assert stat.S_ISREG(st_mode), (
            f"Could not create a regular file inside '{PROJECT_DIR}'. "
            "Check directory permissions."
        )
    finally:
        # Clean up silently; ignore errors if file was never created.
        try:
            test_file.unlink()
        except FileNotFoundError:
            pass

@pytest.mark.describe("Pre-condition: localhost resolves to 127.0.0.1")
def test_localhost_resolves_to_loopback():
    try:
        addr = socket.gethostbyname("localhost")
    except Exception as exc:  # pragma: no cover
        pytest.fail(
            f"Python was unable to resolve 'localhost' at all: {exc}\n"
            "Name resolution must be functional for the exercise."
        )
    assert addr == "127.0.0.1", (
        f"'localhost' resolved to '{addr}', but the exercise expects it to "
        "resolve to '127.0.0.1'. Please ensure /etc/hosts or DNS is correct."
    )

COMMON_DNS_CMDS = ("host", "dig", "nslookup", "getent")

@pytest.mark.describe("Pre-condition: at least one standard DNS utility exists")
def test_common_dns_cli_available():
    found_cmds = [cmd for cmd in COMMON_DNS_CMDS if shutil.which(cmd)]
    assert found_cmds, (
        "None of the common DNS lookup utilities "
        f"({', '.join(COMMON_DNS_CMDS)}) were found in $PATH. "
        "The student needs at least one of these commands to craft the "
        "required one-liner."
    )