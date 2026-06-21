# test_initial_state.py
#
# This pytest suite verifies that the pre-seeded “inventory-svc” working copy
# is present and in the exact state described in the assignment **before**
# the student performs any actions.

import os
import subprocess
import pytest
from pathlib import Path

REPO_PATH = Path("/home/user/repos/inventory-svc")
EXPECTED_BRANCH = "main"
EXPECTED_SHORT_HASH = "2f3e5a7"


def git(cmd: str) -> str:
    """
    Run a git command inside REPO_PATH and return stdout as str with no trailing
    newline.  Anything written to stderr or a non-zero exit triggers failure.
    """
    result = subprocess.run(
        ["git"] + cmd.split(),
        cwd=REPO_PATH,
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stderr.strip():
        pytest.fail(
            f"Running `git {cmd}` produced unexpected stderr output:\n{result.stderr}"
        )
    return result.stdout.strip()


def test_repository_initial_state():
    # 1. The working copy directory must exist.
    assert REPO_PATH.is_dir(), (
        f"Expected repository directory {REPO_PATH} to exist, "
        "but it is missing."
    )

    # 2. It must be a git repository (i.e., '.git' directory present).
    git_dir = REPO_PATH / ".git"
    assert git_dir.is_dir(), (
        f"Directory {REPO_PATH} exists but does not appear to be a git "
        f"repository (missing {git_dir})."
    )

    # 3. HEAD must point to the expected default branch.
    head_branch = git("rev-parse --abbrev-ref HEAD")
    assert head_branch == EXPECTED_BRANCH, (
        "Repository is on an unexpected branch.\n"
        f"Expected branch : {EXPECTED_BRANCH}\n"
        f"Actual branch   : {head_branch}\n"
        "Ensure the default branch is checked out."
    )

    # 4. The short hash of HEAD must match the pre-seeded value.
    head_short_hash = git("rev-parse --short HEAD")
    assert head_short_hash == EXPECTED_SHORT_HASH, (
        "HEAD commit hash does not match the pre-seeded repository state.\n"
        f"Expected short hash : {EXPECTED_SHORT_HASH}\n"
        f"Actual short hash   : {head_short_hash}"
    )