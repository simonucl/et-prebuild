# test_initial_state.py
#
# This test-suite validates that the starting filesystem state for the
# Kubernetes operator repository is exactly as expected *before* the
# learner performs any actions.
#
# It checks:
#   1. The repository directory exists.
#   2. VERSION contains exactly "1.2.3\n".
#   3. CHANGELOG.md contains exactly the 4 expected lines and nothing else.
#
# If any assertion fails the accompanying error message should make it clear
# what is missing or differs from the required initial state.

from pathlib import Path
import pytest

REPO_DIR = Path("/home/user/k8s-operator")
VERSION_FILE = REPO_DIR / "VERSION"
CHANGELOG_FILE = REPO_DIR / "CHANGELOG.md"

EXPECTED_VERSION_CONTENT = "1.2.3\n"

EXPECTED_CHANGELOG_CONTENT = (
    "## [1.2.3] - 2023-07-01\n"
    "### Changed\n"
    "- Fixed reconciliation loop bug.\n"
    "\n"
)


def test_repository_directory_exists():
    assert REPO_DIR.exists(), f"Required directory {REPO_DIR} is missing."
    assert REPO_DIR.is_dir(), f"{REPO_DIR} exists but is not a directory."


def test_version_file_initial_content():
    assert VERSION_FILE.exists(), f"Required file {VERSION_FILE} is missing."

    content = VERSION_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_VERSION_CONTENT
    ), (
        f"{VERSION_FILE} content mismatch.\n"
        f"Expected byte-exact:\n{repr(EXPECTED_VERSION_CONTENT)}\n"
        f"Found:\n{repr(content)}"
    )


def test_changelog_initial_content():
    assert CHANGELOG_FILE.exists(), f"Required file {CHANGELOG_FILE} is missing."

    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_CHANGELOG_CONTENT
    ), (
        f"{CHANGELOG_FILE} content mismatch.\n"
        "It must contain exactly the following (byte-perfect) at task start:\n"
        f"{repr(EXPECTED_CHANGELOG_CONTENT)}\n"
        "Found:\n"
        f"{repr(content)}"
    )

    # Additional explicit line-count check for clarity
    expected_lines = EXPECTED_CHANGELOG_CONTENT.splitlines(keepends=True)
    found_lines = content.splitlines(keepends=True)
    assert len(found_lines) == len(
        expected_lines
    ), (
        f"{CHANGELOG_FILE} should contain {len(expected_lines)} lines, "
        f"but contains {len(found_lines)}."
    )