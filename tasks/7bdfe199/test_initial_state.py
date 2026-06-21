# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
for the “edge_project” deployment task.

These tests must run **before** the student performs any action.
They assert that:
1. The source project directory and devices_master.tsv exist exactly as expected.
2. The devices_master.tsv file content is byte-for-byte correct.
3. The deploy_batch directory (and its target files) do NOT yet exist.

Only the Python standard library and pytest are used.
"""

import io
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "edge_project"
MASTER_TSV = PROJECT_DIR / "devices_master.tsv"
DEPLOY_DIR = PROJECT_DIR / "deploy_batch"

# --------------------------------------------------------------------------- #
# Expected content of /home/user/edge_project/devices_master.tsv
# (using real tab characters, Unix newlines, and a trailing newline)
# --------------------------------------------------------------------------- #

_EXPECTED_MASTER_LINES = [
    "device_id\tmodel\tfirmware_version\tip_address\tuptime_hours\tcity\tready_for_deploy",
    "gw-001\tA1\t1.0.3\t192.168.0.11\t240\tNewYork\tyes",
    "gw-002\tB2\t1.0.1\t10.0.0.50\t12\tBerlin\tno",
    "gw-003\tA1\t1.0.4\t192.168.0.30\t48\tNewYork\tyes",
    "gw-004\tC3\t1.2.0\t172.16.1.10\t5\tTokyo\tyes",
    "gw-005\tB2\t1.0.1\t10.0.0.60\t96\tBerlin\tyes",
]
EXPECTED_MASTER_CONTENT = "\n".join(_EXPECTED_MASTER_LINES) + "\n"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_bytes(path: Path) -> bytes:
    """
    Return the full raw bytes of a file.

    Using bytes instead of str guards against silent newline / encoding changes.
    """
    return path.read_bytes()


def read_text(path: Path) -> str:
    """Convenience wrapper around pathlib read_text with explicit UTF-8."""
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Required project directory missing: {PROJECT_DIR}\n"
        "Create it or adjust the path."
    )


def test_devices_master_exists():
    assert MASTER_TSV.is_file(), (
        f"Source file missing: {MASTER_TSV}\n"
        "The task requires this file to be present before any action is taken."
    )


def test_devices_master_content_exact():
    actual = read_bytes(MASTER_TSV)
    expected = EXPECTED_MASTER_CONTENT.encode("utf-8")
    diff_msg = io.StringIO()
    if actual != expected:
        # Produce a small diff-style output for easier debugging.
        actual_text = actual.decode("utf-8", errors="replace").splitlines(keepends=True)
        expected_text = EXPECTED_MASTER_CONTENT.splitlines(keepends=True)
        diff_msg.write("devices_master.tsv content mismatch.\n")
        diff_msg.write("First differing line (expected vs. actual):\n")
        for idx, (exp, act) in enumerate(zip(expected_text, actual_text), 1):
            if exp != act:
                diff_msg.write(f"Line {idx} expected: {exp!r}\n")
                diff_msg.write(f"Line {idx} actual  : {act!r}\n")
                break
        else:
            if len(expected_text) != len(actual_text):
                diff_msg.write(
                    "File lengths differ "
                    f"(expected {len(expected_text)} lines, "
                    f"got {len(actual_text)} lines).\n"
                )
    assert actual == expected, diff_msg.getvalue()


def test_deploy_batch_not_present_yet():
    """
    The deployment directory should NOT exist at the start.
    It will be created by the student during the task.
    """
    assert not DEPLOY_DIR.exists(), (
        f"The directory {DEPLOY_DIR} already exists, but the task "
        "requires it to be created as part of the solution. "
        "Remove it before running the exercise."
    )