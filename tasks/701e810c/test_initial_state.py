# test_initial_state.py
#
# Pytest suite that validates the pristine state of the operating system
# before the student generates `/home/user/compliance_audit.log`.
#
# What we assert:
#   1. The Git repository exists at /home/user/compliance_repo.
#   2. The repository is valid (has a .git directory).
#   3. The HEAD commit hash, short hash, author name, and remote URL are all
#      exactly as described in the specification.
#   4. The audit log **does not yet exist**; the student must create it.
#
# Any deviation from these expectations will yield a clear, actionable
# assertion message.

import os
import subprocess
import pytest


REPO_PATH = "/home/user/compliance_repo"
EXPECTED_FULL_HASH = "51f2c3d7b991c7aa0123456789abcdefabcde999"
EXPECTED_SHORT_HASH = "51f2c3d"
EXPECTED_AUTHOR_NAME = "Sam Auditor"
EXPECTED_REMOTE_URL = "https://example.com/internal/compliance_repo.git"
AUDIT_LOG_PATH = "/home/user/compliance_audit.log"


def _git(cmd, cwd=REPO_PATH) -> str:
    """
    Helper to run a git command inside the repository and return stripped output.
    Raises subprocess.CalledProcessError if the command fails.
    """
    result = subprocess.check_output(["git"] + cmd, cwd=cwd, text=True)
    return result.strip()


def test_repository_directory_exists():
    assert os.path.isdir(REPO_PATH), (
        f"Expected Git repository directory '{REPO_PATH}' to exist but it was "
        "not found. Ensure the repository is present before starting the task."
    )


def test_repository_is_valid_git_repo():
    git_dir = os.path.join(REPO_PATH, ".git")
    assert os.path.isdir(git_dir), (
        f"Directory '{REPO_PATH}' exists but is not a Git repository "
        f"(missing '{git_dir}')."
    )


def test_head_commit_hash():
    full_hash = _git(["rev-parse", "HEAD"])
    assert full_hash == EXPECTED_FULL_HASH, (
        "HEAD commit hash mismatch.\n"
        f"  Expected: {EXPECTED_FULL_HASH}\n"
        f"  Found:    {full_hash}"
    )

    short_hash = _git(["rev-parse", "--short", "HEAD"])
    assert short_hash == EXPECTED_SHORT_HASH, (
        "Short (7-character) commit hash mismatch.\n"
        f"  Expected: {EXPECTED_SHORT_HASH}\n"
        f"  Found:    {short_hash}"
    )


def test_head_commit_author():
    author = _git(["log", "-1", "--pretty=format:%an"])
    assert author == EXPECTED_AUTHOR_NAME, (
        "Commit author name mismatch.\n"
        f"  Expected: {EXPECTED_AUTHOR_NAME}\n"
        f"  Found:    {author}"
    )


def test_origin_remote_url():
    remote_url = _git(["remote", "get-url", "origin"])
    assert remote_url == EXPECTED_REMOTE_URL, (
        "Origin remote URL mismatch.\n"
        f"  Expected: {EXPECTED_REMOTE_URL}\n"
        f"  Found:    {remote_url}"
    )


def test_audit_log_not_present_yet():
    assert not os.path.exists(AUDIT_LOG_PATH), (
        f"Audit log '{AUDIT_LOG_PATH}' already exists, but it should be created "
        "by the student as part of the task. Remove the file before testing."
    )