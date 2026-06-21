# test_initial_state.py
"""
Pytest suite that validates the **initial/clean** state of the operating
system before the student starts implementing the security-scan utility.

The checks deliberately ensure that:
1. The required mock input files and directories already exist *and* contain
   the exact expected contents.
2. The writable reports directory exists but does not yet contain any of the
   artefacts the student is supposed to create.
3. No prematurely existing script or output files can hide a missing
   implementation.
"""

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
SAMPLE_DIR = HOME / "sample_data"
REPORTS_DIR = HOME / "reports"

NETSTAT_FILE = SAMPLE_DIR / "mock_netstat.txt"
PASSWD_FILE = SAMPLE_DIR / "mock_passwd"

SCRIPT_FILE = REPORTS_DIR / "run_security_scan.sh"
YAML_REPORT = REPORTS_DIR / "infra_security_report.yml"
TIME_LOG = REPORTS_DIR / "scan_exec_time.log"


@pytest.fixture(scope="module")
def expected_netstat_content():
    # The file is expected to end with a trailing newline.
    return (
        "Proto LocalAddress  State  PID/Program\n"
        "tcp   0.0.0.0:22    LISTEN 123/sshd\n"
        "tcp   0.0.0.0:8080  LISTEN 456/nginx\n"
        "udp   0.0.0.0:53           789/dnsmasq\n"
    )


@pytest.fixture(scope="module")
def expected_passwd_content():
    # The file is expected to end with a trailing newline.
    return (
        "root:x:0:0:root:/root:/bin/bash\n"
        "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"
        "bin:x:2:2:bin:/bin:/usr/sbin/nologin\n"
        "sys:x:3:3:sys:/dev:/usr/sbin/nologin\n"
        "sync:x:4:65534:sync:/bin:/bin/sync\n"
        "user1:x:1000:1000:User One:/home/user1:/bin/bash\n"
    )


def test_required_directories_exist_and_are_dirs():
    """Verify that /home/user/sample_data and /home/user/reports exist."""
    assert SAMPLE_DIR.is_dir(), (
        f"Required directory missing: {SAMPLE_DIR}"
    )
    assert REPORTS_DIR.is_dir(), (
        f"Required directory missing: {REPORTS_DIR}"
    )


def test_reports_directory_is_writable():
    """
    The partially-prepared reports directory must be writable
    so the student can create new files there.
    """
    assert os.access(REPORTS_DIR, os.W_OK), (
        f"Directory {REPORTS_DIR} is not writable for the current user."
    )


def test_mock_netstat_file_exists_and_matches(expected_netstat_content):
    """Ensure the mock netstat file exists and its exact content is correct."""
    assert NETSTAT_FILE.is_file(), (
        f"Mock netstat file missing: {NETSTAT_FILE}"
    )
    # Read as binary to avoid newline translation surprises, then decode.
    content = NETSTAT_FILE.read_bytes().decode()
    assert content == expected_netstat_content, (
        f"Contents of {NETSTAT_FILE} do not match the expected fixture."
    )


def test_mock_passwd_file_exists_and_matches(expected_passwd_content):
    """Ensure the mock passwd file exists and its exact content is correct."""
    assert PASSWD_FILE.is_file(), (
        f"Mock passwd file missing: {PASSWD_FILE}"
    )
    content = PASSWD_FILE.read_bytes().decode()
    assert content == expected_passwd_content, (
        f"Contents of {PASSWD_FILE} do not match the expected fixture."
    )


@pytest.mark.parametrize(
    "path,description",
    [
        (SCRIPT_FILE, "execution script"),
        (YAML_REPORT, "YAML report"),
        (TIME_LOG, "execution-time log"),
    ],
)
def test_no_output_or_script_exists_yet(path: Path, description: str):
    """
    Before the student runs the pipeline, none of the deliverable artefacts
    should be present. Their presence would indicate a stale workspace or
    an incorrect initial state.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing {description} found at: {path}"
    )


def test_reports_directory_contains_no_executable_script():
    """
    Ensures there is no executable run_security_scan.sh yet.  Even if the file
    is accidentally present but *not* executable, it should be removed to
    avoid confusion.
    """
    if SCRIPT_FILE.exists():
        mode = SCRIPT_FILE.stat().st_mode
        is_exec = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert not is_exec, (
            f"{SCRIPT_FILE} should not be executable before the student "
            "implements the solution."
        )