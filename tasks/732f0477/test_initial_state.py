# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# before the student performs any actions for the deployment task.
#
# Checked items (all must already be true):
# 1. The directory /home/user/remote/sample-app.git exists.
# 2. It is a *bare* Git repository.
# 3. HEAD points to refs/heads/main.
# 4. The repository contains exactly one commit.
# 5. The single commit message is exactly "Initial version 2.0.0".
# 6. The VERSION file in that commit contains exactly "2.0.0\n".
#
# NOTE: We intentionally do *not* test for any of the output artifacts
# the student will produce (clone, new branch, update.log, etc.).

import os
import subprocess
import shutil
import pytest

BARE_REPO_PATH = "/home/user/remote/sample-app.git"


def run_git_gitdir(args):
    """
    Run a git command with --git-dir set to the bare repository.
    Returns stdout decoded to str with trailing newline stripped.
    Raises subprocess.CalledProcessError on failure.
    """
    completed = subprocess.run(
        ["git", f"--git-dir={BARE_REPO_PATH}", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )
    return completed.stdout.rstrip("\n")


@pytest.fixture(scope="session")
def git_available():
    """Ensure git is available on the system."""
    git_path = shutil.which("git")
    assert git_path is not None, (
        "Git executable not found in PATH. "
        "These tests require git to be installed and accessible."
    )
    return git_path


def test_bare_repo_directory_exists(git_available):
    assert os.path.isdir(
        BARE_REPO_PATH
    ), f"Expected bare repository directory {BARE_REPO_PATH!r} to exist."


def test_repository_is_bare(git_available):
    is_bare = run_git_gitdir(["rev-parse", "--is-bare-repository"])
    assert (
        is_bare.strip() == "true"
    ), f"Repository at {BARE_REPO_PATH} is not marked as bare."


def test_head_points_to_main_branch(git_available):
    head_ref = run_git_gitdir(["symbolic-ref", "HEAD"])
    assert (
        head_ref.strip() == "refs/heads/main"
    ), f"HEAD should point to 'refs/heads/main', found {head_ref!r}."


def test_single_initial_commit_count(git_available):
    commit_count = run_git_gitdir(["rev-list", "--count", "HEAD"])
    assert (
        commit_count == "1"
    ), f"Expected exactly one commit in the bare repository, found {commit_count}."


def test_initial_commit_message(git_available):
    message = run_git_gitdir(["log", "-1", "--pretty=%B"])
    assert (
        message == "Initial version 2.0.0"
    ), "Initial commit message should be exactly 'Initial version 2.0.0'."


def test_version_file_contents(git_available):
    version_contents = run_git_gitdir(["show", "HEAD:VERSION"])
    expected = "2.0.0\n"
    assert (
        version_contents == expected.rstrip("\n")
        or version_contents == expected  # depends on git stripping newline
    ), (
        f"VERSION file in initial commit should contain {expected!r}. "
        f"Found {version_contents!r}."
    )