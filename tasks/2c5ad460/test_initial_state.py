# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student performs any action.  It deliberately checks
# that the project is still on version 1.4.2 and that no 1.4.3
# section has been inserted yet.

import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/experiments")
VERSION_FILE = BASE_DIR / "VERSION"
CHANGELOG_FILE = BASE_DIR / "CHANGELOG.md"


@pytest.fixture(scope="module")
def changelog_lines():
    """Return CHANGELOG.md split into *raw* lines (including possible blanks)."""
    try:
        text = CHANGELOG_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(
            f"Expected changelog file missing: {CHANGELOG_FILE}",
            pytrace=False,
        )
    return text.splitlines()


def test_directory_layout():
    """The /home/user/experiments directory must exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing. "
        "Have you mounted / created the repository correctly?"
    )


def test_version_file_exists_and_content():
    """
    Ensure VERSION exists and contains exactly '1.4.2\\n'.
    Any deviation means the bump was done prematurely or the
    starting point is wrong.
    """
    assert VERSION_FILE.is_file(), f"Missing VERSION file at {VERSION_FILE}"
    content = VERSION_FILE.read_text(encoding="utf-8")
    assert (
        content == "1.4.2\n"
    ), "VERSION file must contain exactly '1.4.2' followed by a newline at the initial state."


def test_changelog_starts_with_expected_block(changelog_lines):
    """
    The very top of CHANGELOG.md should describe version 1.4.2.
    We strip leading blank lines, then check the first four
    non-empty lines.
    """
    non_empty = [ln for ln in changelog_lines if ln.strip()]

    expected_block = [
        "# Changelog",
        "## [1.4.2] - 2023-08-22",
        "### Fixed",
        "- Resolved metrics logging race condition.",
    ]

    # We compare element-wise for clearer failure reports.
    for idx, expected in enumerate(expected_block):
        try:
            observed = non_empty[idx]
        except IndexError:  # pragma: no cover
            pytest.fail(
                f"CHANGELOG.md is missing expected line {idx + 1!r}: {expected!r}",
                pytrace=False,
            )
        assert (
            observed == expected
        ), f"Line {idx + 1} of CHANGELOG.md expected {expected!r} but found {observed!r}."


def test_changelog_does_not_yet_contain_1_4_3(changelog_lines):
    """
    Verify that the new version 1.4.3 has *not* been added yet.
    This ensures the test runs before the task is performed.
    """
    joined = "\n".join(changelog_lines)
    assert (
        "## [1.4.3]" not in joined
    ), "CHANGELOG.md already contains a 1.4.3 section – initial state is incorrect."