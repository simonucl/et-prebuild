# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present before the student performs the release-prep steps described
# in the assignment.  If any of these tests fail, the starting state is
# incorrect and the exercise cannot be completed as specified.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest
import textwrap

WEBSITE_DIR = Path("/home/user/projects/website")
PACKAGE_JSON = WEBSITE_DIR / "package.json"
CHANGELOG_MD = WEBSITE_DIR / "CHANGELOG.md"
RELEASE_LOG = WEBSITE_DIR / "release.log"


@pytest.fixture(scope="session")
def expected_package_json_text():
    """
    The exact text that must be present in /home/user/projects/website/package.json
    including the terminating newline.
    """
    return textwrap.dedent(
        """\
        {
          "name": "awesome-website",
          "version": "1.2.3",
          "description": "A demo website",
          "scripts": {
            "start": "node server.js"
          }
        }
        """
    )


@pytest.fixture(scope="session")
def expected_changelog_text():
    """
    The exact text that must be present in /home/user/projects/website/CHANGELOG.md
    including the terminating newline.
    """
    return textwrap.dedent(
        """\
        ## [1.2.3] - 2024-05-20
        ### Fixed
        - Resolved navigation bug.
        """
    )


def test_website_directory_exists():
    assert WEBSITE_DIR.exists(), (
        f"Required directory {WEBSITE_DIR} is missing. "
        "The entire project tree must already exist."
    )
    assert WEBSITE_DIR.is_dir(), f"{WEBSITE_DIR} exists but is not a directory."


def test_package_json_exists_and_exact_contents(expected_package_json_text):
    assert PACKAGE_JSON.exists(), f"Expected file {PACKAGE_JSON} is missing."
    assert PACKAGE_JSON.is_file(), f"{PACKAGE_JSON} exists but is not a regular file."

    actual = PACKAGE_JSON.read_text(encoding="utf-8")
    expected = expected_package_json_text

    assert actual == expected, (
        f"{PACKAGE_JSON} contents differ from the expected starting state.\n"
        "If you have already modified this file, revert it so that only the "
        'line containing `"version": "1.2.3"` is present, exactly as shown.\n\n'
        "---- Expected ----\n"
        f"{expected}\n"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_changelog_exists_and_exact_contents(expected_changelog_text):
    assert CHANGELOG_MD.exists(), f"Expected file {CHANGELOG_MD} is missing."
    assert CHANGELOG_MD.is_file(), f"{CHANGELOG_MD} exists but is not a regular file."

    actual = CHANGELOG_MD.read_text(encoding="utf-8")
    expected = expected_changelog_text

    assert actual == expected, (
        f"{CHANGELOG_MD} contents differ from the expected starting state.\n"
        "Make sure the changelog has exactly three lines (plus the final newline) "
        "shown in the task description.\n\n"
        "---- Expected ----\n"
        f"{expected}\n"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_release_log_does_not_exist_yet():
    assert not RELEASE_LOG.exists(), (
        f"{RELEASE_LOG} should NOT exist before the release steps are performed.\n"
        "It must be created by the student during the exercise."
    )