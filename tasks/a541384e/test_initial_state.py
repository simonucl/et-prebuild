# test_initial_state.py
#
# This test-suite validates the **initial** repository/OS state that must be
# present *before* the student begins the exercise.  It purposefully asserts
# the pre-change conditions (e.g., TIMEOUT == 3, VERSION == "1.4.2", etc.).
#
# If any of these tests fail, the starting snapshot is wrong and the
# instructions cannot be completed as written.

import os
import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
REPO_ROOT = Path("/home/user/uptime-dashboard")
MONITOR_PY = REPO_ROOT / "monitor.py"
VERSION_FILE = REPO_ROOT / "VERSION"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
BUMP_LOG = REPO_ROOT / "bump.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Return UTF-8 text from *path* or raise an assertion with context."""
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Could not read {path}: {exc}") from exc


# --------------------------------------------------------------------------- #
# Tests – filesystem
# --------------------------------------------------------------------------- #
def test_repository_directory_exists():
    assert REPO_ROOT.is_dir(), f"Directory {REPO_ROOT} is missing."


def test_monitor_py_contains_timeout_3():
    contents = read_text(MONITOR_PY)
    assert (
        "TIMEOUT = 3" in contents
    ), "monitor.py should still declare 'TIMEOUT = 3' at the start of the exercise."


def test_offset_timeout_5_not_present():
    contents = read_text(MONITOR_PY)
    assert (
        "TIMEOUT = 5" not in contents
    ), "monitor.py already contains 'TIMEOUT = 5'; it should still be 3 before the exercise."


def test_version_file_is_1_4_2():
    contents = read_text(VERSION_FILE)
    expected = "1.4.2\n"
    assert (
        contents == expected
    ), f"VERSION file should contain exactly {expected!r} before the bump, found {contents!r}."


def test_changelog_starts_with_expected_unreleased_block():
    contents = read_text(CHANGELOG)
    # Expected top 7 lines (byte-for-byte)
    expected_top = (
        "# Changelog\n"
        "\n"
        "## [Unreleased]\n"
        "### Fixed\n"
        "- None yet\n"
        "\n"
        "## [1.4.2] - 2023-11-20\n"
    )
    early_slice = contents[: len(expected_top)]
    assert (
        early_slice == expected_top
    ), (
        "CHANGELOG.md does not start with the expected pre-exercise text.\n"
        "Expected start:\n"
        f"{expected_top!r}\n\n"
        "Actual start:\n"
        f"{early_slice!r}"
    )


def test_version_1_4_3_not_yet_in_changelog():
    contents = read_text(CHANGELOG)
    assert (
        "## [1.4.3]" not in contents
    ), "CHANGELOG.md already lists version 1.4.3; this should only appear after the exercise."


def test_bump_log_does_not_exist_yet():
    assert (
        not BUMP_LOG.exists()
    ), f"{BUMP_LOG} is already present; it should only be created after completing the exercise."


# --------------------------------------------------------------------------- #
# Tests – Git status
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "git_cmd",
    [
        ["git", "rev-parse", "--is-inside-work-tree"],
        ["git", "status", "--porcelain"],
    ],
)
def test_git_repository_clean(git_cmd):
    """
    1. Confirm we are inside a Git repository.
    2. Confirm the working tree is clean (no local modifications).
    """
    result = subprocess.run(
        git_cmd,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=False,
    )

    cmd_display = " ".join(git_cmd)
    assert (
        result.returncode == 0
    ), f"Command '{cmd_display}' failed with exit code {result.returncode}:\n{result.stderr}"

    if git_cmd[-1] == "--porcelain":
        assert (
            result.stdout.strip() == ""
        ), "Git working tree is not clean at the start of the exercise:\n" + result.stdout


# --------------------------------------------------------------------------- #
# Sanity check – student hasn't already created the final VERSION file
# --------------------------------------------------------------------------- #
def test_no_premature_version_bump():
    contents = read_text(VERSION_FILE)
    assert (
        contents.strip() != "1.4.3"
    ), "VERSION file already shows 1.4.3; the bump should happen during the exercise."