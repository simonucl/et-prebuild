# test_initial_state.py
#
# This test-suite asserts that the repository *before* the student starts
# matches the specification provided in the exercise description.
#
# It intentionally verifies only the “initial” state – i.e. it checks that
# the student has NOT yet performed the required release-bump steps.
#
# Requirements checked:
#   1. Repository /home/user/app exists and is a valid git repo.
#   2. VERSION file exists and contains exactly “2.3.4\n”.
#   3. CHANGELOG.md’s very first non-blank line documents version 2.3.4.
#   4. No .release_log file is present yet.
#   5. The lightweight tag v2.3.4 exists and points at HEAD.
#   6. No tag called v2.3.5 exists yet.
#
# Only Python’s stdlib and pytest are used.

import os
import re
import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_path() -> Path:
    """Return the absolute Path object to the repository root."""
    path = Path("/home/user/app").resolve()
    return path


def run_git(repo: Path, *args: str) -> str:
    """
    Helper around `git -C <repo> …` that returns stdout (stripped).
    Raises pytest failure on non-zero exit.
    """
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        pytest.fail(
            f"git command failed: git -C {repo} {' '.join(args)}\n"
            f"stdout: {completed.stdout}\n"
            f"stderr: {completed.stderr}"
        )
    return completed.stdout.strip()


# --------------------------------------------------------------------------- #
# 1. Repository & basic structure                                             #
# --------------------------------------------------------------------------- #
def test_repository_exists_and_is_git(repo_path: Path) -> None:
    assert repo_path.is_dir(), f"Repository directory {repo_path} is missing."
    git_dir = repo_path / ".git"
    assert git_dir.is_dir(), f"{git_dir} directory is missing – not a git repo."
    # Basic sanity: `git rev-parse HEAD` should work.
    head = run_git(repo_path, "rev-parse", "--verify", "HEAD")
    assert re.fullmatch(r"[0-9a-f]{40}", head), "Could not determine git HEAD commit."


# --------------------------------------------------------------------------- #
# 2. VERSION file                                                             #
# --------------------------------------------------------------------------- #
def test_version_file_contents(repo_path: Path) -> None:
    version_file = repo_path / "VERSION"
    assert version_file.is_file(), f"{version_file} does not exist."
    data = version_file.read_bytes()
    expected = b"2.3.4\n"
    assert (
        data == expected
    ), f"{version_file} should contain exactly {expected!r} but contains {data!r}."


# --------------------------------------------------------------------------- #
# 3. CHANGELOG.md top section                                                 #
# --------------------------------------------------------------------------- #
def test_changelog_top_section_is_for_234(repo_path: Path) -> None:
    changelog_file = repo_path / "CHANGELOG.md"
    assert changelog_file.is_file(), f"{changelog_file} does not exist."

    lines = changelog_file.read_text(encoding="utf-8").splitlines()

    # Find first non-blank line
    first_idx = next((i for i, ln in enumerate(lines) if ln.strip()), None)
    assert (
        first_idx is not None
    ), f"{changelog_file} appears to be empty or only contains blank lines."

    header_line = lines[first_idx].rstrip()
    header_pattern = re.compile(
        r"^##\s+2\.3\.4\s+[–-]\s+\d{4}-\d{2}-\d{2}$"
    )  # allow en-dash or hyphen
    assert header_pattern.match(
        header_line
    ), (
        "The first changelog header should document version 2.3.4, e.g.\n"
        "## 2.3.4 – 2024-02-10\n"
        f"but found: {header_line!r}"
    )

    # Next line should be a bullet item
    try:
        bullet_line = lines[first_idx + 1].rstrip()
    except IndexError:
        pytest.fail(
            f"{changelog_file} is missing bullet lines after the 2.3.4 header."
        )

    bullet_pattern = re.compile(r"^\*\s+.+")
    assert bullet_pattern.match(
        bullet_line
    ), f"Expected a bullet line after the header, but found: {bullet_line!r}"

    # Third line should be blank
    try:
        blank_line = lines[first_idx + 2]
    except IndexError:
        pytest.fail(
            f"{changelog_file} should contain a blank line after the bullet list."
        )

    assert (
        blank_line.strip() == ""
    ), "A blank line must follow the bullet list of the 2.3.4 section."


# --------------------------------------------------------------------------- #
# 4. .release_log must NOT exist yet                                          #
# --------------------------------------------------------------------------- #
def test_release_log_absence(repo_path: Path) -> None:
    release_log = repo_path / ".release_log"
    assert (
        not release_log.exists()
    ), f"{release_log} should NOT exist before the student performs the release."


# --------------------------------------------------------------------------- #
# 5. Git tags                                                                 #
# --------------------------------------------------------------------------- #
def test_git_tag_234_exists_and_points_at_head(repo_path: Path) -> None:
    # Tag v2.3.4 must exist
    tags = run_git(repo_path, "tag", "--list", "v2.3.4").splitlines()
    assert (
        "v2.3.4" in tags
    ), "Expected a lightweight tag named 'v2.3.4' in the repository."

    # It must point at HEAD
    head_commit = run_git(repo_path, "rev-parse", "HEAD")
    tag_commit = run_git(repo_path, "rev-parse", "v2.3.4")
    assert (
        head_commit == tag_commit
    ), "Tag 'v2.3.4' should reference HEAD, but it does not."


def test_git_tag_235_does_not_exist_yet(repo_path: Path) -> None:
    tags = run_git(repo_path, "tag", "--list", "v2.3.5").splitlines()
    assert (
        not tags
    ), "Tag 'v2.3.5' already exists, but it should NOT be created before the task is done."