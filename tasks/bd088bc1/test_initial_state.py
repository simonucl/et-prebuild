# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system /
# filesystem before the student begins the task described in the prompt.
#
# What we verify:
#   1. The file `/home/user/target_ip.txt` exists, is a regular file,
#      and contains exactly one line: "127.0.0.1".
#   2. The standard `ping` utility is available and can be executed by the
#      current (non-root) user.
#
# What we deliberately do **NOT** verify (per the authoring rules):
#   • The existence or contents of any output artefacts that the student
#     is expected to create (e.g. /home/user/logs or ping_summary.log).

import os
import stat
import subprocess
import sys
from pathlib import Path
import shutil
import pytest


TARGET_FILE = Path("/home/user/target_ip.txt")
EXPECTED_IP = "127.0.0.1"


def test_target_ip_file_exists_and_is_regular():
    """
    The target IP file must exist *before* the student starts the task
    so they have an address to test against.
    """
    assert TARGET_FILE.exists(), (
        f"Required file {TARGET_FILE} is missing. "
        "It should contain the IPv4 address to test."
    )

    # Ensure it is a regular file (not a directory, symlink to dir, etc.)
    file_stat = TARGET_FILE.stat()
    assert stat.S_ISREG(file_stat.st_mode), (
        f"{TARGET_FILE} exists but is not a regular file."
    )


def test_target_ip_file_contains_exactly_one_line_with_expected_ip():
    """
    The file must contain exactly one line and *nothing else*:
    '127.0.0.1' (optionally followed by a single newline).
    """
    content = TARGET_FILE.read_bytes()

    # Disallow leading/trailing whitespace other than a single newline at EOL.
    # Decode strictly to catch any stray non-ASCII bytes.
    decoded = content.decode("utf-8")

    # Splitlines keeps behaviour consistent across \n / \r\n endings
    lines = decoded.splitlines()

    assert len(lines) == 1, (
        f"{TARGET_FILE} should contain exactly one line, "
        f"but found {len(lines)} lines."
    )

    assert lines[0].strip() == EXPECTED_IP, (
        f"The only line in {TARGET_FILE} must be '{EXPECTED_IP}', "
        f"but found: '{lines[0]}'."
    )


def test_ping_utility_is_available():
    """
    The standard `ping` utility must be present in PATH and executable.
    We do *not* perform the full 3-packet test here; we only ensure the tool
    exists and that the current user can invoke it.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, (
        "The 'ping' executable could not be found in PATH. "
        "It is required for the task."
    )

    # Try a single ping to 127.0.0.1 with one packet.
    # This should succeed quickly if the utility is runnable.
    try:
        completed = subprocess.run(
            [ping_path, "-c", "1", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(
            "'ping' command timed out when attempting to send 1 packet to "
            "127.0.0.1. Ensure the utility can be executed by the current user."
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"'ping' command exited with non-zero status ({exc.returncode}). "
            "Ensure the utility is functional without requiring root privileges."
        )