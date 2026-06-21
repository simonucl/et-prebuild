# test_initial_state.py
#
# Pytest suite that validates the filesystem and Git repository *before*
# the student performs any actions for the “finance-data” backup task.
#
# This test file asserts the following pre-conditions:
#   1. Required directory hierarchy exists with the expected (or more permissive)
#      permissions.
#   2. /home/user/projects/finance-data is a valid Git repository.
#   3. The repository contains exactly one commit whose SHA-1 is
#      7fd1a60b01f91b314f5996f35b385144ae4a9b0f.
#   4. The commit’s tree contains a README.md file with the expected contents.
#
# NOTE:  • We do *not* check for the presence of the output file
#          /home/user/backup/checks/finance_head.log, in accordance with the
#          grading-harness rules.
#        • Only the Python standard library and pytest are used.

import os
import stat
import subprocess
import textwrap
import pytest

USER_HOME = "/home/user"
PROJECTS_DIR = os.path.join(USER_HOME, "projects")
REPO_DIR = os.path.join(PROJECTS_DIR, "finance-data")
BACKUP_DIR = os.path.join(USER_HOME, "backup")
CHECKS_DIR = os.path.join(BACKUP_DIR, "checks")

EXPECTED_HEAD_SHA = "7fd1a60b01f91b314f5996f35b385144ae4a9b0f"
EXPECTED_README_CONTENT = "# Finance Data\n\nInitial dataset.\n"


@pytest.mark.parametrize(
    "path",
    [
        PROJECTS_DIR,
        REPO_DIR,
        BACKUP_DIR,
        CHECKS_DIR,
    ],
)
def test_directories_exist(path):
    """
    Verify that all required directories exist and are indeed directories.
    """
    assert os.path.exists(
        path
    ), f"Required directory {path!r} is missing."
    assert os.path.isdir(
        path
    ), f"Expected {path!r} to be a directory, but it is not."


def _assert_mode_at_least(path: str, minimum_octal_mode: int):
    """
    Helper that asserts `path`'s mode has *at least* the bits specified
    in `minimum_octal_mode` (e.g. 0o755).  Extra permission bits (e.g. the
    sticky bit) are allowed.
    """
    mode = stat.S_IMODE(os.stat(path).st_mode)
    missing_bits = minimum_octal_mode & (~mode)
    assert (
        missing_bits == 0
    ), (
        f"{path} permissions are {oct(mode)}, but they must include at least "
        f"{oct(minimum_octal_mode)} (missing bits {oct(missing_bits)})."
    )


def test_directory_permissions():
    """
    Ensure directory permissions satisfy the specification.

    • project, repo, and backup dirs: at least 0755
    • checks dir: at least 0775 (group-write bit required)
    """
    _assert_mode_at_least(PROJECTS_DIR, 0o755)
    _assert_mode_at_least(REPO_DIR, 0o755)
    _assert_mode_at_least(BACKUP_DIR, 0o755)
    _assert_mode_at_least(CHECKS_DIR, 0o775)  # group-write


def _git(*args, cwd=REPO_DIR) -> str:
    """
    Run a git command inside the finance-data repository and return stdout.

    Raises a pytest failure with a descriptive message if git is unavailable
    or the command fails.
    """
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.fail("'git' executable not found on PATH; it is required for the tests.")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Git command 'git {' '.join(args)}' failed with exit code "
            f"{exc.returncode}.\nstdout:\n{exc.stdout}\nstderr:\n{exc.stderr}"
        )
    return proc.stdout.strip()


def test_git_repository_state():
    """
    Verify that the repo is valid and on the expected single commit.
    """
    # Confirm that .git directory exists
    git_dir = os.path.join(REPO_DIR, ".git")
    assert os.path.isdir(
        git_dir
    ), f"Expected Git repository at {REPO_DIR!r}, but .git directory is missing."

    # Confirm HEAD SHA
    head_sha = _git("rev-parse", "HEAD")
    assert (
        head_sha == EXPECTED_HEAD_SHA
    ), f"HEAD commit SHA is {head_sha}, expected {EXPECTED_HEAD_SHA}."

    # Ensure there is exactly one commit
    commit_count = int(_git("rev-list", "--count", "HEAD"))
    assert (
        commit_count == 1
    ), f"Repository should have exactly 1 commit, but has {commit_count}."

    # Confirm that README.md exists in the working tree
    readme_path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(
        readme_path
    ), f"README.md is missing from repository at {readme_path}."

    # Validate README.md content
    with open(readme_path, "r", encoding="utf-8") as fp:
        actual_content = fp.read()
    assert (
        actual_content == EXPECTED_README_CONTENT
    ), textwrap.dedent(
        f"""
        README.md content mismatch.

        Expected:
        {EXPECTED_README_CONTENT!r}

        Found:
        {actual_content!r}
        """
    )