# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the
# “IoT device synchronisation” exercise _before_ the student runs any
# commands.  The tests deliberately **do not** check for the post-sync
# outcome; they only enforce that the sandbox starts from the expected
# baseline so that the student’s single synchronisation command can be
# graded reliably.

import os
from pathlib import Path

SRC_ROOT = Path("/home/user/edge_source")
DST_ROOT = Path("/home/user/iot_device/edge_app")
LOG_DIR  = Path("/home/user/deployment_logs")
LOG_FILE = LOG_DIR / "sync_2024.log"


# ---------- helpers -----------------------------------------------------------------

def _assert_file_contents(path: Path, expected: str) -> None:
    """Assert that `path` exists (regular file) and its contents match `expected`."""
    assert path.exists(), f"Expected file {path} to exist."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."
    actual = path.read_text()
    assert actual == expected, (
        f"File {path} has unexpected contents.\n"
        f"Expected (repr): {repr(expected)}\n"
        f"Actual   (repr): {repr(actual)}"
    )


# ---------- tests -------------------------------------------------------------------

def test_source_tree_files_exist_and_content():
    """Verify the freshly-built release tree exists and holds the correct files."""
    assert SRC_ROOT.exists(), f"Source root directory {SRC_ROOT} is missing."
    assert SRC_ROOT.is_dir(), f"Source root {SRC_ROOT} is not a directory."

    _assert_file_contents(SRC_ROOT / "app.py", 'print("Edge app v1.1.0")\n')
    _assert_file_contents(SRC_ROOT / "version.txt", "1.1.0\n")
    _assert_file_contents(SRC_ROOT / "config.yaml", "setting: prod\n")

    # Ensure there are no unexpected extra files that might influence rsync logic.
    allowed = {"app.py", "version.txt", "config.yaml"}
    extra = {p.name for p in SRC_ROOT.iterdir()} - allowed
    assert not extra, (
        f"Source directory {SRC_ROOT} contains unexpected extra files/directories: {sorted(extra)}. "
        "The initial state must match the specification exactly."
    )


def test_destination_tree_initial_state():
    """Destination (IoT device) directory starts with outdated files and legacy temp file."""
    assert DST_ROOT.exists(), f"Destination root directory {DST_ROOT} is missing."
    assert DST_ROOT.is_dir(), f"Destination root {DST_ROOT} is not a directory."

    _assert_file_contents(DST_ROOT / "app.py", 'print("Edge app v1.0.0")\n')
    _assert_file_contents(DST_ROOT / "version.txt", "1.0.0\n")

    # The legacy temp file must exist before sync so the student's command can remove it.
    _assert_file_contents(DST_ROOT / "old.tmp", "legacy\n")

    # File config.yaml must NOT yet exist in the destination.
    config_path = DST_ROOT / "config.yaml"
    assert not config_path.exists(), (
        f"Destination file {config_path} should *not* exist before synchronisation."
    )


def test_deployment_logs_absent():
    """No deployment log directory or file should exist before the student starts."""
    assert not LOG_DIR.exists(), (
        f"Directory {LOG_DIR} unexpectedly exists before any deployment; it should be "
        "created by the student's solution."
    )
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} is present prematurely. It must be created by the student."
    )