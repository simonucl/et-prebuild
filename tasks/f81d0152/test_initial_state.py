# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the filesystem
# before the student performs any action on the “support-tool”.
#
# The tests purposefully fail if anything has already been modified,
# thereby protecting against tasks that run in the wrong order.
#
# Only standard library + pytest are used.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
TOOL_DIR = HOME / "support-tool"
VERSION_FILE = TOOL_DIR / "VERSION"
CHANGELOG_FILE = TOOL_DIR / "CHANGELOG.md"
DIAGNOSTICS_DIR = TOOL_DIR / "diagnostics"


@pytest.fixture(scope="session")
def version_contents():
    if not VERSION_FILE.exists():
        pytest.skip(f"VERSION file not present at expected location: {VERSION_FILE}")
    return VERSION_FILE.read_text(encoding="utf-8")


def test_support_tool_directory_exists():
    assert TOOL_DIR.is_dir(), (
        f"Required directory missing: {TOOL_DIR}. "
        "The initial repository should be checked out at this path."
    )


def test_version_file_contains_original_version(version_contents):
    expected = "0.9.7\n"
    assert (
        version_contents == expected
    ), (
        f"{VERSION_FILE} should contain exactly one line "
        f"with '0.9.7' and a single trailing newline. "
        f"Found:\n{repr(version_contents)}"
    )


def test_changelog_initial_header():
    assert CHANGELOG_FILE.exists(), (
        f"CHANGELOG.md missing at expected path: {CHANGELOG_FILE}"
    )

    with CHANGELOG_FILE.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    # Ensure we have at least three lines to check.
    assert len(lines) >= 3, (
        f"{CHANGELOG_FILE} should start with three lines:\n"
        "# Changelog\\n## [Unreleased]\\n(blank line)\\n"
        f"Found only {len(lines)} line(s)."
    )

    line1_expected = "# Changelog\n"
    line2_expected = "## [Unreleased]\n"

    assert (
        lines[0] == line1_expected
    ), (
        f"First line of {CHANGELOG_FILE} must be exactly {line1_expected!r}. "
        f"Found: {lines[0]!r}"
    )
    assert (
        lines[1] == line2_expected
    ), (
        f"Second line of {CHANGELOG_FILE} must be exactly {line2_expected!r}. "
        f"Found: {lines[1]!r}"
    )
    assert (
        lines[2].strip() == ""
    ), (
        "Third line of CHANGELOG.md should be blank to separate "
        "'## [Unreleased]' from subsequent content."
    )


def test_diagnostics_directory_does_not_exist_yet():
    assert not DIAGNOSTICS_DIR.exists(), (
        f"The diagnostics directory {DIAGNOSTICS_DIR} "
        "should NOT exist before the student runs their script."
    )