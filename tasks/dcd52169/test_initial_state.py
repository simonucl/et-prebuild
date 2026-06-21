# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student starts working on the “30-second high-frequency snapshot”
# task.  Nothing related to incident_001 should exist yet – the student is
# expected to create everything from scratch.
#
# Requirements verified here (all MUST be absent):
#   • /home/user/incident_001/metrics/           (directory)
#   • /home/user/incident_001/metrics/cpu.log    (file)
#   • /home/user/incident_001/metrics/mem.log    (file)
#   • /home/user/incident_001/metrics/disk.log   (file)
#   • /home/user/incident_001/metrics/net.log    (file)
#   • /home/user/incident_001/summary.log        (file)
#
# Only the Python stdlib + pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
INCIDENT_DIR = HOME / "incident_001"
METRICS_DIR = INCIDENT_DIR / "metrics"

RAW_LOGS = {
    "CPU": METRICS_DIR / "cpu.log",
    "MEM": METRICS_DIR / "mem.log",
    "DISK": METRICS_DIR / "disk.log",
    "NET": METRICS_DIR / "net.log",
}

SUMMARY_FILE = INCIDENT_DIR / "summary.log"


def _assert_path_absent(p: Path):
    """
    Helper ensuring a path does *not* exist on the filesystem.
    Produces a clear assertion message if the object is unexpectedly present.
    """
    assert not p.exists(), (
        f"Initial-state requirement violated: {p} already exists.\n"
        "The workspace must start clean so the student can create the file/"
        "directory as part of the exercise."
    )


def test_home_directory_exists():
    """Sanity check: /home/user itself must exist (pre-provided by the platform)."""
    assert HOME.is_dir(), "Fixture error: expected base home directory /home/user to exist."


def test_incident_directory_absent():
    """The incident_001 directory must NOT exist yet."""
    _assert_path_absent(INCIDENT_DIR)


def test_metrics_directory_absent():
    """The metrics subdirectory must NOT exist yet."""
    _assert_path_absent(METRICS_DIR)


@pytest.mark.parametrize("log_name, log_path", RAW_LOGS.items())
def test_raw_logs_absent(log_name, log_path):
    """None of the four raw metric logs should pre-exist."""
    _assert_path_absent(log_path)


def test_summary_file_absent():
    """The summary.log must NOT exist before collection."""
    _assert_path_absent(SUMMARY_FILE)