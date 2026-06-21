# test_initial_state.py
#
# This pytest suite validates that the starting filesystem / repository
# state is exactly as expected *before* the student performs any actions
# described in the task specification.

import os
import subprocess
from pathlib import Path

import pytest

REPO_PATH = Path("/home/user/etl-pipeline")
README_PATH = REPO_PATH / "README.md"
COMMIT_LOG_PATH = Path("/home/user/etl_commit.log")


def git(*args: str) -> str:
    """
    Run a git command inside REPO_PATH and return its stdout as str.
    """
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_PATH,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def test_repository_directory_exists():
    assert REPO_PATH.exists(), f"Expected repository directory {REPO_PATH} to exist."
    assert REPO_PATH.is_dir(), f"{REPO_PATH} exists but is not a directory."


def test_git_repository_is_initialized():
    git_dir = REPO_PATH / ".git"
    assert git_dir.exists() and git_dir.is_dir(), (
        f"{REPO_PATH} is not a Git repository (missing .git directory)."
    )


def test_on_branch_main_and_clean_worktree():
    current_branch = git("rev-parse", "--abbrev-ref", "HEAD")
    assert (
        current_branch == "main"
    ), f"Expected current branch to be 'main', got '{current_branch}'."

    status_output = git("status", "--porcelain")
    assert (
        status_output == ""
    ), "Git working tree is not clean; expected no staged/unstaged/untracked changes."


def test_branch_update_readme_sales_not_present():
    branches = git("branch", "--list", "update-readme-sales")
    assert (
        branches == ""
    ), "Branch 'update-readme-sales' already exists; the exercise expects it to be created by the student."


def test_readme_exists_and_has_expected_contents():
    assert README_PATH.exists(), f"Expected README file at {README_PATH}."
    assert README_PATH.is_file(), f"{README_PATH} exists but is not a regular file."

    contents = README_PATH.read_text(encoding="utf-8")
    expected = "ETL Pipeline\n\n"
    assert (
        contents == expected
    ), (
        "README.md contents are not as expected.\n"
        f"Expected exactly:\n{repr(expected)}\nGot:\n{repr(contents)}"
    )


def test_initial_commit_contains_only_readme():
    tree_files = git("ls-tree", "--name-only", "-r", "HEAD").splitlines()
    assert tree_files == ["README.md"], (
        "Initial commit should contain only 'README.md'. "
        f"Found: {tree_files}"
    )


def test_commit_log_not_present_yet():
    assert not COMMIT_LOG_PATH.exists(), (
        f"Commit log {COMMIT_LOG_PATH} already exists; it should be created "
        "only after the student completes the exercise."
    )