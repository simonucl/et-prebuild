# test_initial_state.py
#
# This pytest suite validates the initial state of the operating-system /
# filesystem *before* the student creates `/home/user/audit/git_audit_log.txt`.
#
# It checks:
#   1. That the main repository exists and is a valid Git working tree.
#   2. That the working tree is *clean* (`git status --short` is empty).
#   3. That the HEAD hash in the main repository is the expected one.
#   4. That exactly one sub-module exists and is on the expected commit/branch.
#   5. That the sub-module directory itself is a valid Git repository.
#
# Only the standard library and `pytest` are used.

import subprocess
from pathlib import Path

import pytest

# Constants describing the expected, pristine state.
MAIN_REPO_PATH = Path("/home/user/project")
SUBMODULE_PATH = MAIN_REPO_PATH / "libs" / "json"
EXPECTED_HEAD = "7890abcd1234567890abcdef1234567890abcd"
EXPECTED_SUBMODULE_COMMIT = "abcd1234567890abcdef1234567890abcdef12"
EXPECTED_SUBMODULE_STATUS_LINE = (
    f" {EXPECTED_SUBMODULE_COMMIT} libs/json (heads/master)"
).rstrip("\n")

# Helper to run a git command inside a repository and capture stdout.
def _git(repo_path: Path, *args: str) -> str:
    """
    Run `git <args>` inside *repo_path* and return stdout (decoded to str).

    This helper raises pytest.fail with a helpful message if git returns a
    non-zero exit status so that individual tests remain readable.
    """
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.fail(
            "Git is not installed or not found in PATH. "
            "Install Git in the test environment."
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            (
                f"Git command failed: git {' '.join(args)}\n"
                f"cwd: {repo_path}\n"
                f"stdout: {exc.stdout}\n"
                f"stderr: {exc.stderr}"
            )
        )
    return completed.stdout


def test_main_repository_exists_and_is_git_repo():
    assert MAIN_REPO_PATH.is_dir(), (
        f"Expected main repository directory {MAIN_REPO_PATH} to exist, "
        "but it was not found."
    )
    git_dir = MAIN_REPO_PATH / ".git"
    assert git_dir.exists(), (
        f"Directory {MAIN_REPO_PATH} exists but is not a Git repository "
        f"(missing {git_dir})."
    )


def test_working_tree_is_clean():
    status_output = _git(MAIN_REPO_PATH, "status", "--short")

    # Git can emit either literally nothing or a single newline when clean.
    assert status_output in ("", "\n"), (
        "The main repository should be clean, but 'git status --short' produced "
        f"unexpected output:\n{status_output!r}"
    )


def test_head_commit_is_expected():
    head = _git(MAIN_REPO_PATH, "rev-parse", "HEAD").strip()
    assert (
        head == EXPECTED_HEAD
    ), f"Expected HEAD commit {EXPECTED_HEAD}, but got {head}."


def test_single_expected_submodule_and_status():
    status_output = _git(MAIN_REPO_PATH, "submodule", "status").rstrip("\n")
    assert (
        status_output == EXPECTED_SUBMODULE_STATUS_LINE
    ), (
        "Unexpected 'git submodule status' output.\n"
        f"Expected: {EXPECTED_SUBMODULE_STATUS_LINE!r}\n"
        f"Got     : {status_output!r}"
    )


def test_submodule_directory_is_git_repo_and_on_expected_commit():
    assert SUBMODULE_PATH.is_dir(), (
        f"Expected sub-module directory {SUBMODULE_PATH} to exist, "
        "but it was not found."
    )

    git_dir = SUBMODULE_PATH / ".git"
    assert git_dir.exists(), (
        f"Sub-module directory {SUBMODULE_PATH} exists but is not a Git "
        f"repository (missing {git_dir})."
    )

    submodule_head = _git(SUBMODULE_PATH, "rev-parse", "HEAD").strip()
    assert (
        submodule_head == EXPECTED_SUBMODULE_COMMIT
    ), (
        "Sub-module HEAD does not match the expected commit.\n"
        f"Expected: {EXPECTED_SUBMODULE_COMMIT}\n"
        f"Got     : {submodule_head}"
    )