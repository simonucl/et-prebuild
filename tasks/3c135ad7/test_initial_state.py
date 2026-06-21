# test_initial_state.py
#
# Pytest suite that verifies the *starting* state of the operating-system /
# filesystem **before** the student performs any actions for the exercise
# “incident-23145 hot-fix”.
#
# These tests purposefully avoid checking for any files, directories, branches,
# or tags that are expected to be CREATED by the student.  They only assert
# the presence and correctness of the initial repository and its single file.

import subprocess
from pathlib import Path

import pytest

# ---- Constants ----------------------------------------------------------------

REPO_PATH = Path("/home/user/infra-config").resolve()
CONFIG_FILE = REPO_PATH / "config" / "serviceA.yml"

EXPECTED_FILE_LINES = [
    "service_name: serviceA",
    "replicas: 3",
    "image: serviceA:1.2.0",
]

# ---- Helper -------------------------------------------------------------------


def git(*args: str) -> str:
    """
    Run a git command inside REPO_PATH and return stdout as str (stripped).
    """
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


# ---- Tests --------------------------------------------------------------------


def test_repository_directory_exists():
    assert REPO_PATH.is_dir(), (
        f"Expected Git repository directory {REPO_PATH} to exist, "
        "but it is missing."
    )


def test_repository_is_a_git_repo():
    git_dir = REPO_PATH / ".git"
    assert git_dir.is_dir(), (
        f"Directory {REPO_PATH} is not a Git repository (no .git folder found)."
    )


def test_current_branch_is_main():
    head_branch = git("rev-parse", "--abbrev-ref", "HEAD")
    assert head_branch == "main", (
        f"Repository should start on branch 'main', but HEAD is on '{head_branch}'."
    )


def test_working_directory_is_clean():
    status_output = git("status", "--porcelain")
    assert status_output == "", (
        "Working directory is not clean. Expected no modified or untracked "
        "files at the start of the exercise."
    )


def test_exactly_one_tracked_file_and_its_path():
    tracked_files = git("ls-files").splitlines()
    assert tracked_files == ["config/serviceA.yml"], (
        "The repository should contain exactly one tracked file "
        "'config/serviceA.yml'. "
        f"Found tracked files: {tracked_files or '<<none>>'}"
    )


def test_single_initial_commit():
    commit_count = int(git("rev-list", "--count", "HEAD"))
    assert commit_count == 1, (
        f"Expected exactly one commit in the initial repository, found {commit_count}."
    )


def test_config_file_exists_and_contents_are_correct():
    assert CONFIG_FILE.is_file(), (
        f"Expected configuration file {CONFIG_FILE} to exist, but it is missing."
    )

    file_text = CONFIG_FILE.read_text(encoding="utf-8").rstrip("\n")
    actual_lines = file_text.splitlines()
    assert actual_lines == EXPECTED_FILE_LINES, (
        f"Contents of {CONFIG_FILE} are not as expected.\n"
        f"Expected:\n{EXPECTED_FILE_LINES}\n"
        f"Actual:\n{actual_lines}"
    )