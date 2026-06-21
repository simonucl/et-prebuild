# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student carries out the synchronisation task.
#
# ❗  Do NOT modify these tests.  Make your solution satisfy them.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOCAL_SRC = HOME / "test_env" / "local_src"
REMOTE_DST = HOME / "test_env" / "remote_dst"
SYNC_LOGS = HOME / "sync_logs"
FILE1 = LOCAL_SRC / "file1.txt"
FILE2 = LOCAL_SRC / "file2.txt"
FILE3 = LOCAL_SRC / "file3.txt"      # should not exist yet

EXPECTED_CONTENTS = {
    FILE1: "QA sync test file 1\n",
    FILE2: "QA sync test file 2\n",
}


@pytest.fixture(scope="module")
def _verify_running_on_unix():
    # Basic sanity-check: these tasks only make sense on POSIX
    if os.name != "posix":
        pytest.skip("Filesystem checks are intended for a POSIX system only.")


def _is_readable_by_owner(path: Path) -> bool:
    """Return True if the file is readable by its owner."""
    st_mode = path.stat().st_mode
    return bool(st_mode & stat.S_IRUSR)


def _list_regular_children(directory: Path):
    """Return list of child paths that are regular files or dirs (skip '.' and '..')."""
    return [directory / name for name in os.listdir(directory)]


# ---------------------------------------------------------------------------
# Directory existence & structure
# ---------------------------------------------------------------------------

def test_local_src_directory_exists(_verify_running_on_unix):
    assert LOCAL_SRC.is_dir(), (
        f"Required directory {LOCAL_SRC} does not exist or is not a directory."
    )


def test_local_src_contains_exactly_two_files():
    assert FILE1.exists(), f"Missing file: {FILE1}"
    assert FILE2.exists(), f"Missing file: {FILE2}"
    unexpected = [p for p in _list_regular_children(LOCAL_SRC)
                  if p.name not in {"file1.txt", "file2.txt"}]
    assert not unexpected, (
        f"{LOCAL_SRC} should only contain file1.txt and file2.txt at the start, "
        f"but found extra entries: {', '.join(str(p) for p in unexpected)}"
    )


def test_file3_not_present_yet():
    assert not FILE3.exists(), (
        f"{FILE3} should NOT exist before the student creates it."
    )


def test_remote_dst_directory_is_empty():
    assert REMOTE_DST.is_dir(), (
        f"Required directory {REMOTE_DST} does not exist or is not a directory."
    )

    children = _list_regular_children(REMOTE_DST)
    assert len(children) == 0, (
        f"{REMOTE_DST} is expected to be empty at task start, "
        f"but found: {', '.join(str(p) for p in children)}"
    )


def test_sync_logs_directory_absent():
    assert not SYNC_LOGS.exists(), (
        f"{SYNC_LOGS} should NOT exist before any synchronisation runs."
    )


# ---------------------------------------------------------------------------
# File contents & permissions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filepath, expected_content", EXPECTED_CONTENTS.items())
def test_initial_file_contents(filepath: Path, expected_content: str):
    assert filepath.is_file(), f"{filepath} should be a regular file."
    with filepath.open("r", encoding="utf-8") as fh:
        actual = fh.read()
    assert actual == expected_content, (
        f"Content mismatch in {filepath}.\n"
        f"Expected: {expected_content!r}\n"
        f"Got:      {actual!r}"
    )


@pytest.mark.parametrize("filepath", [FILE1, FILE2])
def test_initial_file_permissions_readable(filepath: Path):
    assert _is_readable_by_owner(filepath), (
        f"{filepath} is not readable by its owner. "
        "Ensure it has at least 0644 permissions."
    )