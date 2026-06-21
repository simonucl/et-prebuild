# test_initial_state.py
#
# This test-suite verifies that the sandbox starts in the **expected clean
# state** *before* the student attempts the synchronisation exercise.
#
# What we check:
# 1. The “remote host” directory tree exists and contains **exactly** the
#    three reference log files with the correct byte-for-byte contents.
# 2. No local staging or output artefacts (/home/user/local_logs or
#    /home/user/synced_logs, tarball, report) are present yet.
#
# If any of these tests fail, the student starts from an unexpected
# environment and should be informed with a clear, specific message.
#
# NOTE:  Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest


REMOTE_DIR = Path("/home/user/remote_host/var/logs")
LOCAL_STAGE_DIR = Path("/home/user/local_logs")
LOCAL_SYNC_DIR = Path("/home/user/synced_logs")
TARBALL_PATH = LOCAL_SYNC_DIR / "nightly_logs_20230502.tar.gz"
REPORT_PATH = LOCAL_SYNC_DIR / "sync_report.txt"

# Expected files and their exact byte contents (including trailing newline)
EXPECTED_LOGS = {
    "app1.log": (
        b"2023-05-01 12:00:00 INFO App1 started\n"
        b"2023-05-01 12:05:00 ERROR Something failed\n"
    ),
    "app2.log": b"2023-05-01 13:00:00 INFO App2 heartbeat\n",
    "sys.log": b"May  1 14:00:00 host kernel: Boot complete\n",
}


def test_remote_directory_exists():
    """The mounted 'remote host' log directory must exist."""
    assert REMOTE_DIR.is_dir(), (
        f"Required directory '{REMOTE_DIR}' is missing. "
        "The remote host volume is not mounted at the expected path."
    )


def test_remote_directory_contains_only_expected_logs():
    """The remote log directory must contain *exactly* the three expected .log files."""
    present = {p.name for p in REMOTE_DIR.iterdir() if p.is_file()}
    expected = set(EXPECTED_LOGS.keys())

    # Missing files?
    missing = expected - present
    # Unexpected extras?
    extras = present - expected

    assert not missing, (
        f"The following expected log files are missing from {REMOTE_DIR}: {sorted(missing)}"
    )
    assert not extras, (
        f"Unexpected files found in {REMOTE_DIR}: {sorted(extras)}. "
        "Directory must contain only the three reference *.log files."
    )


@pytest.mark.parametrize("filename,expected_bytes", EXPECTED_LOGS.items())
def test_remote_logs_have_correct_content(filename, expected_bytes):
    """Each remote .log file must match the canonical byte content."""
    path = REMOTE_DIR / filename
    assert path.is_file(), f"Expected file '{path}' is missing."

    actual = path.read_bytes()
    assert (
        actual == expected_bytes
    ), f"Contents of '{path}' differ from the reference data."


def test_no_local_staging_directory_yet():
    """/home/user/local_logs must **not** exist before the task starts."""
    assert not LOCAL_STAGE_DIR.exists(), (
        f"Staging directory '{LOCAL_STAGE_DIR}' already exists. "
        "The environment should start clean — nothing should have been copied yet."
    )


def test_no_local_synced_directory_or_outputs_yet():
    """
    /home/user/synced_logs *and* the required artefacts must not pre-exist.
    The student is expected to create them.
    """
    assert not LOCAL_SYNC_DIR.exists(), (
        f"Output directory '{LOCAL_SYNC_DIR}' already exists. "
        "It should be created by the student's script, not pre-supplied."
    )

    # Even if the directory somehow exists, the artefacts absolutely must not.
    assert not TARBALL_PATH.exists(), (
        f"Tarball '{TARBALL_PATH}' is unexpectedly present before synchronisation."
    )
    assert not REPORT_PATH.exists(), (
        f"Report file '{REPORT_PATH}' is unexpectedly present before synchronisation."
    )