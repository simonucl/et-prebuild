# test_initial_state.py
#
# Pytest suite that validates the _initial_ filesystem state before the
# student performs any action on the microservice repository.
#
# It asserts that:
#   • /home/user/microservice exists and is a directory
#   • /home/user/microservice/version.txt exists and contains exactly "1.2.4\n"
#   • /home/user/microservice/CHANGELOG.md exists and contains the expected
#     baseline changelog for version 1.2.4
#   • /home/user/microservice/bump.log does NOT exist yet
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path

import pytest

MICROSERVICE_DIR = Path("/home/user/microservice")
VERSION_FILE = MICROSERVICE_DIR / "version.txt"
CHANGELOG_FILE = MICROSERVICE_DIR / "CHANGELOG.md"
BUMP_LOG_FILE = MICROSERVICE_DIR / "bump.log"

EXPECTED_VERSION_CONTENT = "1.2.4\n"

EXPECTED_CHANGELOG_CONTENT = (
    "# Changelog\n\n"
    "## [1.2.4] - 2023-01-15\n"
    "### Added\n"
    "- Initial release.\n"
)


@pytest.fixture(scope="module")
def microservice_dir():
    """Return the microservice directory Path object, asserting it exists."""
    assert MICROSERVICE_DIR.exists(), (
        f"Directory {MICROSERVICE_DIR} is missing. "
        "The initial repository should already be present."
    )
    assert MICROSERVICE_DIR.is_dir(), (
        f"{MICROSERVICE_DIR} exists but is not a directory."
    )
    return MICROSERVICE_DIR


def test_version_file_exists_and_correct(microservice_dir):
    assert VERSION_FILE.exists(), (
        f"{VERSION_FILE} is missing. It must be present before the bump."
    )
    assert VERSION_FILE.is_file(), (
        f"{VERSION_FILE} exists but is not a regular file."
    )

    content = VERSION_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_VERSION_CONTENT, (
        f"{VERSION_FILE} content mismatch.\n"
        f"Expected: {repr(EXPECTED_VERSION_CONTENT)}\n"
        f"Found:    {repr(content)}"
    )


def test_changelog_file_exists_and_correct(microservice_dir):
    assert CHANGELOG_FILE.exists(), (
        f"{CHANGELOG_FILE} is missing. It must be present before the bump."
    )
    assert CHANGELOG_FILE.is_file(), (
        f"{CHANGELOG_FILE} exists but is not a regular file."
    )

    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CHANGELOG_CONTENT, (
        f"{CHANGELOG_FILE} content mismatch.\n"
        "It should contain exactly the baseline changelog for version 1.2.4.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CHANGELOG_CONTENT!r}\n"
        "---- Found ----\n"
        f"{content!r}"
    )


def test_bump_log_not_present_yet(microservice_dir):
    assert not BUMP_LOG_FILE.exists(), (
        f"{BUMP_LOG_FILE} should NOT exist before the version bump is executed."
    )


def test_no_unexpected_files(microservice_dir):
    """
    Ensure that only the expected baseline files are present in the directory.
    This guards against stray files that might interfere with the assignment.
    """
    expected = {VERSION_FILE.name, CHANGELOG_FILE.name}
    actual = {p.name for p in microservice_dir.iterdir()}
    unexpected = actual - expected
    # Allow dotfiles (e.g. .gitkeep) if present; ignore them.
    unexpected = {name for name in unexpected if not name.startswith(".")}
    assert not unexpected, (
        "Unexpected files found in the microservice directory before the bump:\n"
        + "\n".join(sorted(unexpected))
    )