# test_initial_state.py
#
# This pytest suite checks that the operating-system / filesystem state
# is pristine **before** the student starts working on the “network-health
# snapshot” exercise.  It purposely confirms that the required workspace
# directory and all artefact files are ABSENT, while at the same time
# ensuring the system has the essential networking tools that the student
# must call (`ping`, `traceroute`, `dig`).
#
# All assertions emit clear, actionable messages when they fail.
#
# Requirements verified:
#   • /home/user/net_diag must NOT exist yet.
#   • No log/JSON files from the final task may pre-exist.
#   • ping / traceroute / dig binaries must be found in $PATH.
#   • 127.0.0.1 must respond to a single ICMP echo (sanity check).
#
# Only stdlib + pytest are used.

import os
import subprocess
import shutil
from pathlib import Path

WORKSPACE = Path("/home/user/net_diag")
EXPECTED_FILES = {
    WORKSPACE / "ping_localhost.log",
    WORKSPACE / "traceroute_localhost.log",
    WORKSPACE / "dig_localhost.log",
    WORKSPACE / "diagnostic_summary.json",
}

TOOLS = {
    "ping",
    "traceroute",
    "dig",
}


def test_workspace_absent():
    """
    The dedicated workspace directory should NOT exist before the student runs
    their solution.  If it already exists, we cannot guarantee that the
    exercise runs in a clean environment.
    """
    assert not WORKSPACE.exists(), (
        f"Workspace directory {WORKSPACE} already exists but should be absent "
        "at the start of the exercise.  Remove it before proceeding."
    )


def test_required_files_absent():
    """
    None of the artefact files that the student will be asked to create should
    be present yet.
    """
    pre_existing = [p for p in EXPECTED_FILES if p.exists()]
    assert not pre_existing, (
        "The following output files already exist, but the exercise is supposed "
        f"to generate them from scratch:\n{chr(10).join(str(p) for p in pre_existing)}"
    )


def test_networking_tools_available():
    """
    Verify that the essential Linux networking diagnostics are installed and
    discoverable in the PATH.  Failing here means the student cannot complete
    the assignment without first installing packages.
    """
    missing = [tool for tool in TOOLS if shutil.which(tool) is None]
    assert not missing, (
        "The following required command-line tools are missing from PATH:\n"
        f"{', '.join(missing)}\n"
        "Install them (e.g. via apt, yum, or the appropriate package manager) "
        "before attempting the exercise."
    )


def test_loopback_pingable():
    """
    A minimal sanity check that the local networking stack is healthy: send one
    ICMP echo request to 127.0.0.1 and expect success.
    """
    ping_bin = shutil.which("ping")
    if ping_bin is None:
        pytest.skip("ping binary not found – covered in previous test")

    try:
        completed = subprocess.run(
            [ping_bin, "-c", "1", "127.0.0.1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        assert False, f"Executing `ping` failed: {exc}"

    assert completed.returncode == 0, (
        "Ping to 127.0.0.1 failed; network stack may be mis-configured.\n"
        "Command output:\n"
        f"{completed.stdout}"
    )