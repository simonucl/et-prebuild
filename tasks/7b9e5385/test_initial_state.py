# test_initial_state.py
#
# This pytest suite verifies that the lab starts from the expected
# pristine state *before* the student writes and executes their
# hardening script.  It checks:
#   • the presence and exact contents of the three sample files
#   • the absence of any backups, log files, or hardening script
#   • that the required hardening lines are NOT yet present
#
# Only Python stdlib + pytest are used.

from pathlib import Path
import os
import stat
import pytest

BASE_DIR = Path("/home/user/hardening_test")

FILES_EXPECTED = {
    "sshd_config": {
        "lines": [
            "# Sample OpenSSH daemon configuration for the lab",
            "Port 22",
            "Protocol 2",
            "HostKey /etc/ssh/ssh_host_rsa_key",
            "HostKey /etc/ssh/ssh_host_ecdsa_key",
            "HostKey /etc/ssh/ssh_host_ed25519_key",
            "# End of file",
        ],
        "hardening_line": "PermitRootLogin no",
    },
    "sysctl.conf": {
        "lines": [
            "# Kernel sysctl configuration",
            "vm.swappiness = 10",
            "fs.file-max = 65535",
            "# End of file",
        ],
        "hardening_line": "net.ipv4.ip_forward = 0",
    },
    "login.defs": {
        "lines": [
            "# Shadow password suite configuration",
            "UID_MIN                  1000",
            "UID_MAX                 60000",
            "UMASK                    077",
            "# End of file",
        ],
        "hardening_line": "PASS_MAX_DAYS   90",
    },
}

SCRIPT_PATH = BASE_DIR / "apply_hardening.sh"
LOG_PATH = BASE_DIR / "hardening.log"


def read_file_lines(path: Path):
    """
    Read a text file and return a list of lines without trailing newlines.
    """
    return path.read_text(encoding="utf-8").splitlines()


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Required directory {BASE_DIR} is missing."


@pytest.mark.parametrize("filename", FILES_EXPECTED.keys())
def test_sample_file_exists(filename):
    path = BASE_DIR / filename
    assert path.is_file(), f"Sample file {path} is missing."


@pytest.mark.parametrize("filename,meta", FILES_EXPECTED.items())
def test_sample_file_contents_pristine(filename, meta):
    """
    Verify each sample file contains exactly the expected lines and that
    the hardening line is NOT yet present.
    """
    path = BASE_DIR / filename
    actual_lines = read_file_lines(path)
    expected_lines = meta["lines"]

    assert (
        actual_lines == expected_lines
    ), f"{path} contents differ from the expected pristine state."

    hardening_line = meta["hardening_line"]
    assert (
        hardening_line not in actual_lines
    ), f"{path} already contains the hardening line '{hardening_line}', but it should not."


@pytest.mark.parametrize("filename", FILES_EXPECTED.keys())
def test_no_backup_files_yet(filename):
    """
    .orig backups should not exist before the hardening script is run.
    """
    backup_path = BASE_DIR / f"{filename}.orig"
    assert not backup_path.exists(), f"Backup file {backup_path} should NOT exist yet."


def test_no_hardening_log_yet():
    assert not LOG_PATH.exists(), f"Log file {LOG_PATH} should NOT exist before the script is run."


def test_hardening_script_absent_or_not_executable_yet():
    """
    The student has not created the script yet, so either it is absent or
    present but not executable.  We allow non-existence to avoid failing
    students who create it later.
    """
    if SCRIPT_PATH.exists():
        mode = SCRIPT_PATH.stat().st_mode
        is_executable = mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        assert (
            not is_executable
        ), f"{SCRIPT_PATH} is already executable, but the initial state should have no runnable script."