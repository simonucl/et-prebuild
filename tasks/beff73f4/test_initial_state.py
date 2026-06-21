# test_initial_state.py
#
# This pytest suite verifies that the required Git repository already
# exists **before** the student performs any action.  It confirms:
#   1. The repository directory is present.
#   2. The directory is a valid Git repository (contains a .git folder).
#   3. Git is installed and operational.
#   4. The list of currently-tracked files matches the specification
#      (order and content).
#   5. Every expected tracked file is physically present on disk.
#
# NOTE: We intentionally do NOT check for /home/user/git_files.log
# because that file should be created *after* the student runs their
# solution command.


import os
import subprocess
from pathlib import Path

import pytest

REPO_PATH = Path("/home/user/demo_repo")

# The truth value (expected tracked files, in exact order)
EXPECTED_TRACKED_FILES = [
    "README.md",
    "scripts/run.sh",
    "src/main.py",
]


def run_git_cmd(*args) -> subprocess.CompletedProcess:
    """
    Helper to run a git command inside the target repository and return
    the CompletedProcess.  All stderr is captured so pytest output
    remains clean.
    """
    return subprocess.run(
        ["git", "-C", str(REPO_PATH), *args],
        capture_output=True,
        text=True,
        check=False,  # we'll inspect returncode ourselves
    )


def test_repository_directory_exists():
    assert REPO_PATH.is_dir(), (
        f"Expected Git repository directory '{REPO_PATH}' was not found. "
        "Make sure the repository is present at the correct location."
    )


def test_git_directory_exists():
    git_dir = REPO_PATH / ".git"
    assert git_dir.is_dir(), (
        f"Directory '{REPO_PATH}' exists, but it is not a Git repository "
        f"(missing '{git_dir}')."
    )


def test_git_is_installed_and_usable():
    proc = run_git_cmd("--version")
    assert proc.returncode == 0, (
        "Git does not appear to be installed or is not functioning "
        f"properly. stderr:\n{proc.stderr}"
    )


def test_tracked_files_match_expectation():
    """
    Uses `git ls-files` to retrieve the list of tracked files and checks
    that it matches the required list exactly (order included).
    """
    proc = run_git_cmd("ls-files")
    assert proc.returncode == 0, (
        "`git ls-files` failed inside the repository. stderr:\n"
        f"{proc.stderr}"
    )

    tracked_files = [line.rstrip("\n") for line in proc.stdout.splitlines()]
    assert tracked_files == EXPECTED_TRACKED_FILES, (
        "The set (or order) of tracked files in the repository does not "
        "match the project specification.\n"
        f"Expected:\n{EXPECTED_TRACKED_FILES}\n"
        f"Found:\n{tracked_files}"
    )


@pytest.mark.parametrize("relative_path", EXPECTED_TRACKED_FILES)
def test_each_tracked_file_exists_on_disk(relative_path):
    """
    Confirms that every expected tracked file physically exists in the
    working tree.
    """
    file_path = REPO_PATH / relative_path
    assert file_path.is_file(), (
        f"Expected tracked file '{file_path}' is missing on disk."
    )