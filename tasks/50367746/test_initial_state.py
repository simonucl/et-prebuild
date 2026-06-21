# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# before the student starts working on the assignment described in the prompt.
#
# The assertions enforce that the repository /home/user/storage-utils is in the
# expected pristine state (version 1.2.0, single initial commit on `main`,
# specific file contents, etc.).  If any of these tests fail, it means the
# sandbox was not prepared correctly **before** the student begins.

import subprocess
import sys
from pathlib import Path

import pytest

REPO_DIR = Path("/home/user/storage-utils").resolve()
CLEANUP_SH = REPO_DIR / "cleanup.sh"
VERSION_FILE = REPO_DIR / "VERSION"
CHANGELOG = REPO_DIR / "CHANGELOG.md"


@pytest.fixture(scope="session")
def git_available() -> None:
    """Ensure the `git` CLI is available."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("git is not available in the execution environment")


def test_repository_directory_exists():
    assert REPO_DIR.is_dir(), f"Expected Git repo directory {REPO_DIR} to exist."


# --------------------------------------------------------------------------- #
# File presence & contents
# --------------------------------------------------------------------------- #
def test_cleanup_sh_exists_and_content():
    assert CLEANUP_SH.is_file(), f"{CLEANUP_SH} is missing."
    content = CLEANUP_SH.read_text().splitlines()
    assert content, f"{CLEANUP_SH} is empty."

    # Minimal structural checks for the initial placeholder script
    assert content[0].strip() == "#!/usr/bin/env bash", (
        f"{CLEANUP_SH} should start with the bash shebang."
    )

    # The script is supposed to echo a Freed line with hard-coded number 123.
    expected_fragment = 'echo "Freed ${freed} MiB"'
    assert any(expected_fragment in line for line in content), (
        f"{CLEANUP_SH} should contain the line {expected_fragment!r}"
    )

    # The initial script should set freed=123
    assert any("freed=123" in line.replace(" ", "") for line in content), (
        f"{CLEANUP_SH} should set freed=123 in the initial state."
    )


def test_version_file_content():
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} is missing."
    raw = VERSION_FILE.read_text()
    assert raw == "1.2.0\n", (
        f"{VERSION_FILE} must contain exactly '1.2.0' followed by a single newline. "
        f"Found: {raw!r}"
    )


def test_changelog_initial_content():
    assert CHANGELOG.is_file(), f"{CHANGELOG} is missing."

    expected = [
        "## [1.2.0] - 2023-05-01",
        "### Changed",
        "- Improved file deletion speed.",
        "## [1.1.0] - 2023-04-15",
        "### Added",
        "- Initial cleanup implementation.",
    ]

    actual_lines = CHANGELOG.read_text().splitlines()
    # The first six lines should match the expected list exactly.
    assert actual_lines[: len(expected)] == expected, (
        f"{CHANGELOG} does not have the expected initial content.\n"
        f"Expected first lines:\n{expected}\nGot:\n{actual_lines[:len(expected)]}"
    )


# --------------------------------------------------------------------------- #
# Git metadata
# --------------------------------------------------------------------------- #
@pytest.mark.usefixtures("git_available")
def test_git_repository_initial_state():
    # Verify that REPO_DIR is a git repository and obtain meta-data
    try:
        toplevel = subprocess.check_output(
            ["git", "-C", str(REPO_DIR), "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"{REPO_DIR} is not a Git repository (git rev-parse failed): {exc}")

    assert Path(toplevel).resolve() == REPO_DIR, (
        f"{REPO_DIR} should be the top-level of the repository, "
        f"but git reports {toplevel}"
    )

    # Branch should be 'main' (not yet the feature branch)
    branch = subprocess.check_output(
        ["git", "-C", str(REPO_DIR), "rev-parse", "--abbrev-ref", "HEAD"],
        text=True,
    ).strip()
    assert branch == "main", f"Initial branch expected to be 'main', got '{branch}'."

    # Exactly one commit should exist
    commit_count = int(
        subprocess.check_output(
            ["git", "-C", str(REPO_DIR), "rev-list", "--count", "HEAD"],
            text=True,
        ).strip()
    )
    assert commit_count == 1, f"Repository should have exactly one commit; found {commit_count}."

    # Commit message verification
    commit_msg = subprocess.check_output(
        ["git", "-C", str(REPO_DIR), "log", "-1", "--format=%s"],
        text=True,
    ).strip()
    expected_msg = "chore: initial import 1.2.0"
    assert commit_msg == expected_msg, (
        f"Initial commit message should be {expected_msg!r}, got {commit_msg!r}."
    )

    # No tags should exist yet
    tags = subprocess.check_output(
        ["git", "-C", str(REPO_DIR), "tag", "--list"],
        text=True,
    ).splitlines()
    assert tags == [], f"Repository should start with no tags, but found: {tags}"


# --------------------------------------------------------------------------- #
# End of test_initial_state.py
# --------------------------------------------------------------------------- #