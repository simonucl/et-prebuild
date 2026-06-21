# test_initial_state.py
#
# Pytest suite to validate the initial state of the operating system /
# Git repository *before* the student performs any actions for the task
# “create a lightweight tag `experiment_ready` and write `git_tags.log`”.
#
# The checks intentionally assert the *absence* of the final-state artefacts
# (the tag and the log file) and the correctness of the repository’s clean
# starting point.

import os
import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
REPO_ROOT = Path("/home/user/experiments/model-training")
README_PATH = REPO_ROOT / "README.md"
GIT_DIR = REPO_ROOT / ".git"
TAG_NAME = "experiment_ready"
LOG_PATH = REPO_ROOT / "git_tags.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def git(*args: str) -> str:
    """
    Run a git command inside the repository and return its stdout as text.
    """
    cmd = ["git", "-C", str(REPO_ROOT), *args]
    return subprocess.check_output(cmd, text=True).strip()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_repository_directory_exists():
    assert REPO_ROOT.is_dir(), (
        f"Repository directory {REPO_ROOT} is missing. "
        "The initial repository should already exist."
    )
    assert GIT_DIR.is_dir(), (
        f"Directory {GIT_DIR} not found. A valid Git repository "
        "was expected to be present before starting the task."
    )


def test_readme_exists_and_content():
    assert README_PATH.is_file(), (
        f"{README_PATH} is missing. The initial repository must contain "
        "a committed README.md file."
    )

    content = README_PATH.read_text(encoding="utf-8")
    expected = "Model training experiments\n"
    assert content == expected, (
        f"{README_PATH} has unexpected contents.\n"
        f"Expected: {expected!r}\n"
        f"Found:    {content!r}"
    )


def test_branch_is_main_and_head_is_valid_commit():
    # Verify current branch
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    assert branch == "main", (
        f"The current Git branch should be 'main' but is '{branch}'."
    )

    # Verify HEAD points to a valid commit object
    head_hash = git("rev-parse", "HEAD")
    assert len(head_hash) == 40, "HEAD is not pointing to a valid commit hash."


def test_repository_has_no_tags_yet():
    tags = git("tag", "--list")
    assert tags == "", (
        "The repository should start with zero tags, "
        f"but found the following tags: {tags}"
    )


def test_experiment_ready_tag_absent():
    # Explicitly check that the specific tag does NOT yet exist.
    tag_ref_path = GIT_DIR / "refs" / "tags" / TAG_NAME
    assert not tag_ref_path.exists(), (
        f"Tag '{TAG_NAME}' unexpectedly exists at {tag_ref_path}. "
        "The student must create it during the task; it should not "
        "be present beforehand."
    )


def test_git_tags_log_is_absent():
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} already exists but should be created only after the "
        "tagging operation. Ensure the workspace starts clean."
    )