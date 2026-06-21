# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any actions for the described task.
#
# The tests assert that:
#   • The repository /home/user/projects/policy-docs exists, is a clean Git repo
#     on branch “master”, and its HEAD hash is the expected value.
#   • policy.md exists inside that repo, contains at least one line, and does
#     NOT yet include the line that the student must append.
#   • The audits directory (/home/user/audits) does not yet exist.
#
# Any failure provides a clear explanation of what is missing or incorrect.
#
# Only the Python stdlib and pytest are used.

import subprocess
from pathlib import Path
import pytest
import os

REPO_PATH = Path("/home/user/projects/policy-docs")
EXPECTED_HEAD_HASH = "e2d2d78a8ecf18f3d3cdd671b7f1b1d8f8020000"
EXPECTED_BRANCH = "master"
POLICY_FILE = REPO_PATH / "policy.md"
AUDITS_DIR = Path("/home/user/audits")
AUDIT_FILE = AUDITS_DIR / "latest_audit.log"
NEW_LINE = "* All stored data must be encrypted at rest."


def _git(cmd, cwd=REPO_PATH):
    """
    Helper to run a git command and return its stdout as str.

    Raises pytest failure if git exits non-zero.
    """
    result = subprocess.run(
        ["git", *cmd],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Git command failed: git {' '.join(cmd)}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
    return result.stdout.strip()


def test_repository_exists_and_is_git_repo():
    assert REPO_PATH.is_dir(), (
        f"Expected repository directory {REPO_PATH} to exist "
        "but it does not."
    )
    git_dir = REPO_PATH / ".git"
    assert git_dir.is_dir(), (
        f"{REPO_PATH} exists but is not a Git repository "
        f"(missing {git_dir})."
    )


def test_branch_is_master_and_head_hash_matches():
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    assert branch == EXPECTED_BRANCH, (
        f"Repository should be on branch '{EXPECTED_BRANCH}', "
        f"but is on '{branch}'."
    )

    head_hash = _git(["rev-parse", "HEAD"])
    assert head_hash == EXPECTED_HEAD_HASH, (
        "HEAD hash does not match the expected initial commit.\n"
        f" Expected: {EXPECTED_HEAD_HASH}\n"
        f" Found:    {head_hash}\n"
        "The repository must start from the known clean state."
    )


def test_working_tree_is_clean():
    status = _git(["status", "--porcelain"])
    assert status == "", (
        "Working tree is not clean. The initial repository must have "
        "no untracked or modified files.\n"
        f"git status --porcelain output:\n{status}"
    )


def test_policy_md_exists_and_has_content_without_new_line():
    assert POLICY_FILE.is_file(), (
        f"Expected file {POLICY_FILE} to exist in the repository."
    )
    content = POLICY_FILE.read_text(encoding="utf-8").splitlines()
    assert content, f"{POLICY_FILE} should contain at least one line of text."
    last_line = content[-1]
    assert last_line != NEW_LINE, (
        f"The line '{NEW_LINE}' already exists at the end of "
        f"{POLICY_FILE}, but it should be appended by the student later."
    )


def test_audits_directory_and_file_do_not_exist_yet():
    assert not AUDITS_DIR.exists(), (
        f"Directory {AUDITS_DIR} should NOT exist before the task begins."
    )
    # Even if someone created /home/user/audits without the file, still fail;
    # the directory must be absent entirely.
    assert not AUDIT_FILE.exists(), (
        f"Audit file {AUDIT_FILE} should NOT exist before the task begins."
    )