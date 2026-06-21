# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state *before* the student begins work on ticket #4231.
#
# What we assert:
#   • The “remote share” directory exists with the exact three expected files
#     and their canonical contents.
#   • No additional files are present in that directory.
#   • The local workspace (/home/user/support-sync) has **not** been created
#     yet (the student must create it during the task).
#
# If any of these conditions fail, the exercise itself cannot be completed
# correctly, so we fail fast with clear, descriptive error messages.

import os
from pathlib import Path

import pytest

REMOTE_DIR = Path("/home/user/remote_share/configs")
LOCAL_WORK_DIR = Path("/home/user/support-sync")
EXPECTED_REMOTE_FILES = {
    "app.conf": b"ENV=prod\n",
    "settings.ini": b"version=2\n",
    "readme.txt": b"This is the remote config directory.\n",
}


def _read_bytes(path: Path) -> bytes:
    """Safely read file contents as bytes."""
    with path.open("rb") as fh:
        return fh.read()


@pytest.fixture(scope="session")
def remote_dir_contents():
    """Return a mapping {basename: bytes_content} for the remote directory."""
    assert REMOTE_DIR.exists(), (
        f"Required remote directory {REMOTE_DIR} is missing. "
        "The exercise expects it to be pre-mounted."
    )
    assert REMOTE_DIR.is_dir(), (
        f"{REMOTE_DIR} exists but is not a directory. "
        "It must be a directory containing the staged config files."
    )

    file_map = {}
    for p in REMOTE_DIR.iterdir():
        # Only consider regular files; fail otherwise
        assert p.is_file(), (
            f"Unexpected non-file entry found in remote directory: {p} "
            "(only regular files should be present)."
        )
        file_map[p.name] = _read_bytes(p)
    return file_map


def test_remote_directory_contents(remote_dir_contents):
    """Verify the remote directory has exactly the expected files + contents."""
    # 1. Correct set of filenames
    expected_names = set(EXPECTED_REMOTE_FILES.keys())
    actual_names = set(remote_dir_contents.keys())
    missing = expected_names - actual_names
    extra = actual_names - expected_names

    assert not missing, (
        "Remote directory is missing the following expected file(s): "
        f"{', '.join(sorted(missing))}"
    )

    assert not extra, (
        "Remote directory contains unexpected extra file(s): "
        f"{', '.join(sorted(extra))}"
    )

    # 2. Correct byte-for-byte contents
    for name, expected_bytes in EXPECTED_REMOTE_FILES.items():
        actual_bytes = remote_dir_contents[name]
        assert actual_bytes == expected_bytes, (
            f"File {REMOTE_DIR / name} content mismatch.\n"
            f"Expected bytes: {expected_bytes!r}\n"
            f"Actual bytes:   {actual_bytes!r}"
        )


def test_local_workspace_not_yet_present():
    """
    Before the student begins, /home/user/support-sync should NOT exist.
    Its presence would mean remnants from a previous run and would
    invalidate a clean test environment.
    """
    assert not LOCAL_WORK_DIR.exists(), (
        f"Local workspace {LOCAL_WORK_DIR} already exists before the task starts. "
        "Tests must run in a clean environment; please remove it before retrying."
    )