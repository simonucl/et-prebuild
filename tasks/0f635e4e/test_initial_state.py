# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student’s solution runs.
#
# It checks only the pre-existing snapshot input—NOT any output locations.

import os
import stat
import pytest

# Constants describing the expected initial state
HOME_DIR = "/home/user"
SNAPSHOT_DIR = os.path.join(HOME_DIR, "audit_samples")
SNAPSHOT_FILE = os.path.join(SNAPSHOT_DIR, "perms_report.txt")

EXPECTED_LINES = [
    "-rwxr-xr-x\n",
    "-rw-r--r--\n",
    "drwxr-xr-x\n",
    "-rwxr-xr-x\n",
    "-rw-------\n",
    "drwxr-x---\n",
    "-rwxr-xr-x\n",
    "-rw-r--r--\n",
    "-rw-r--r--\n",
    "drwxr-xr-x\n",
]


def _human_readable_mode(path: str) -> str:
    """
    Helper that returns the `ls -l`-style permission string for *path*
    (first 10 chars: file type + rwx bits).
    """
    mode = os.lstat(path).st_mode
    perms = [
        stat.S_ISDIR(mode) and "d" or "-",
        mode & stat.S_IRUSR and "r" or "-",
        mode & stat.S_IWUSR and "w" or "-",
        mode & stat.S_IXUSR and "x" or "-",
        mode & stat.S_IRGRP and "r" or "-",
        mode & stat.S_IWGRP and "w" or "-",
        mode & stat.S_IXGRP and "x" or "-",
        mode & stat.S_IROTH and "r" or "-",
        mode & stat.S_IWOTH and "w" or "-",
        mode & stat.S_IXOTH and "x" or "-",
    ]
    return "".join(perms)


@pytest.fixture(scope="module")
def snapshot_content():
    """Read the snapshot file and return its raw lines."""
    if not os.path.exists(SNAPSHOT_FILE):
        pytest.fail(
            f"Required snapshot file is missing: {SNAPSHOT_FILE}",
            pytrace=False,
        )
    with open(SNAPSHOT_FILE, "r", encoding="ascii", newline="") as fh:
        return fh.readlines()


def test_snapshot_directory_exists():
    assert os.path.isdir(
        SNAPSHOT_DIR
    ), f"Directory {SNAPSHOT_DIR} is required but not present or not a directory."


def test_snapshot_file_exists_and_is_regular():
    assert os.path.isfile(
        SNAPSHOT_FILE
    ), f"File {SNAPSHOT_FILE} is required but not present."
    assert stat.S_ISREG(
        os.stat(SNAPSHOT_FILE).st_mode
    ), f"Path {SNAPSHOT_FILE} exists but is not a regular file."


def test_snapshot_file_has_10_expected_lines(snapshot_content):
    assert (
        len(snapshot_content) == 10
    ), f"Snapshot should have exactly 10 lines, found {len(snapshot_content)}."


def test_each_line_is_10_chars_plus_newline(snapshot_content):
    bad_lines = [
        (idx + 1, line) for idx, line in enumerate(snapshot_content) if len(line) != 11
    ]
    assert (
        not bad_lines
    ), "Each line must be exactly 10 chars plus newline. Offenders:\n" + "\n".join(
        f"Line {num}: {repr(txt)}" for num, txt in bad_lines
    )


def test_snapshot_file_contents_match_expected(snapshot_content):
    assert (
        snapshot_content == EXPECTED_LINES
    ), "Snapshot file content does not match the expected baseline."


def test_snapshot_file_permissions_are_world_readable():
    """
    The snapshot file itself should be world-readable so downstream
    scripts can open it without privilege escalation.
    """
    mode_string = _human_readable_mode(SNAPSHOT_FILE)
    assert mode_string[7] == "r", (
        f"Snapshot file {SNAPSHOT_FILE} should be world-readable; "
        f"current mode is {mode_string}"
    )