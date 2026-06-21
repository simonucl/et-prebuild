# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system /
# filesystem **before** the student carries out the assignment.
#
# The assignment requires the student to create:
#   /home/user/vuln_scan/
#   ├── openssl_policy.out
#   └── scan_report.log
#
# Therefore, none of those items should be present **yet**.  In addition,
# the test verifies that the tools the student must rely on (`apt-cache`)
# are available and functional.
#
# Only the Python standard library and pytest are used.

import os
import subprocess
import shutil
import textwrap
import pytest
from pathlib import Path

HOME_DIR = Path("/home/user")
SCAN_DIR = HOME_DIR / "vuln_scan"
OPENSSL_OUT = SCAN_DIR / "openssl_policy.out"
REPORT_LOG = SCAN_DIR / "scan_report.log"


def _run_cmd(cmd):
    """
    Helper to execute `cmd` and return (returncode, stdout, stderr).
    """
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_home_directory_exists():
    """
    The base home directory must exist so the student has somewhere to work.
    """
    assert HOME_DIR.is_dir(), (
        f"Expected base directory {HOME_DIR} to exist, "
        "but it is missing. The exercise environment is not set up correctly."
    )


def test_scan_dir_absent():
    """
    The /home/user/vuln_scan directory should NOT exist before the student
    starts the task.  Its presence would indicate a dirty / pre-populated
    workspace, which could invalidate the exercise.
    """
    assert not SCAN_DIR.exists(), (
        f"Found unexpected path {SCAN_DIR}. "
        "The workspace must start clean. "
        "Remove this directory (and its contents) before beginning the task."
    )


@pytest.mark.parametrize("filepath", [OPENSSL_OUT, REPORT_LOG])
def test_output_files_absent(filepath):
    """
    Neither of the expected output files should exist yet.
    """
    assert not filepath.exists(), (
        f"Found unexpected file {filepath}. "
        "The initial state must not contain any of the deliverables."
    )


def test_apt_cache_available():
    """
    The `apt-cache` executable must be present in PATH; the student will rely
    on it to query the OpenSSL package version.
    """
    apt_cache_path = shutil.which("apt-cache")
    assert apt_cache_path, (
        "The `apt-cache` command is not available in PATH. "
        "Install the 'apt' userland utilities or ensure PATH is correctly set."
    )


def test_apt_cache_policy_openssl_runs():
    """
    Running `apt-cache policy openssl` should succeed (exit code 0) and emit
    non-empty stdout.  This guarantees that the host's package database is
    in a usable state and the 'openssl' package is at least known to APT.
    """
    retcode, stdout, stderr = _run_cmd(["apt-cache", "policy", "openssl"])

    # Diagnostic context in case of failure
    ctx = textwrap.dedent(
        f"""
        Command: apt-cache policy openssl
        Return code: {retcode}
        Stdout (first 200 chars):
        {stdout[:200]!r}
        Stderr (first 200 chars):
        {stderr[:200]!r}
        """
    ).strip()

    assert retcode == 0, f"`apt-cache policy openssl` failed to run.\n{ctx}"
    assert stdout.strip(), (
        "`apt-cache policy openssl` produced empty output; "
        "package metadata may be missing.\n" + ctx
    )