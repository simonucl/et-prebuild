# test_initial_state.py
#
# Pytest suite that validates the initial state of the repository
# BEFORE the student performs the version-bump task.
#
# What we check:
#   1. /home/user/utils exists and is a directory.
#   2. /home/user/utils/VERSION exists, is a regular file and contains
#      exactly "1.4.2\n" (a single trailing newline, nothing else).
#   3. /home/user/utils/CHANGELOG.md exists, is a regular file and matches
#      the expected introductory paragraph plus the 1.4.2 section.  The
#      file must end with a single newline and contain no extra text.
#
# We deliberately DO NOT test for bump.log (or any other output artefacts)
# because they should not exist yet.

from pathlib import Path

UTILS_DIR = Path("/home/user/utils")
VERSION_FILE = UTILS_DIR / "VERSION"
CHANGELOG_FILE = UTILS_DIR / "CHANGELOG.md"


def test_utils_directory_exists():
    assert UTILS_DIR.exists(), f"Expected directory {UTILS_DIR} to exist."
    assert UTILS_DIR.is_dir(), f"{UTILS_DIR} exists but is not a directory."


def test_version_file_content():
    assert VERSION_FILE.exists(), (
        f"Expected {VERSION_FILE} to exist. "
        "Create the file with the current version number."
    )
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a regular file."

    content = VERSION_FILE.read_text(encoding="utf-8")
    expected = "1.4.2\n"

    assert (
        content == expected
    ), (
        f"{VERSION_FILE} must contain exactly {expected!r} "
        f"(found {content!r}). Ensure there is a single trailing newline "
        "and no additional whitespace."
    )


def test_changelog_initial_content():
    assert CHANGELOG_FILE.exists(), (
        f"Expected {CHANGELOG_FILE} to exist. "
        "Create the file with the introductory changelog text."
    )
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} exists but is not a regular file."

    content = CHANGELOG_FILE.read_text(encoding="utf-8")

    expected = (
        "# Changelog\n"
        "\n"
        "All notable changes to this project will be documented in this file.\n"
        "\n"
        "## [1.4.2] - 2023-09-28\n"
        "### Added\n"
        "- Initial release of data-parsing utilities.\n"
    )

    assert (
        content == expected
    ), (
        f"{CHANGELOG_FILE} does not match the expected initial content. "
        "Ensure the file has exactly the following (blank lines are "
        "significant):\n\n"
        f"{expected!r}\n\nFound:\n\n{content!r}"
    )