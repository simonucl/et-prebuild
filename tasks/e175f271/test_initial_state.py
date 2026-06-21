# test_initial_state.py
#
# This test-suite validates that the working directory for the
# “Acme Cost Optimizer” project is in the **initial** state *before*
# the student performs any actions.  All paths are absolute and the
# checks are intentionally strict so that a failure message pin-points
# the first thing that is out of place.

from pathlib import Path
import re
import pytest

PROJECT_ROOT = Path("/home/user/acme-cost-optimizer")
VERSION_FILE = PROJECT_ROOT / "version.txt"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
RELEASE_LOG = PROJECT_ROOT / "release.log"


def test_project_directory_exists():
    assert PROJECT_ROOT.exists(), f"Expected directory {PROJECT_ROOT} to exist."
    assert PROJECT_ROOT.is_dir(), f"{PROJECT_ROOT} exists but is not a directory."


def test_version_file_initial_content():
    assert VERSION_FILE.exists(), f"Expected file {VERSION_FILE} to exist."
    content = VERSION_FILE.read_text(encoding="utf-8")
    expected = "2.5.4\n"
    assert content == expected, (
        f"{VERSION_FILE} should contain exactly '{expected!r}' "
        f"but found '{content!r}'."
    )


def test_changelog_initial_header_and_section():
    assert CHANGELOG_FILE.exists(), f"Expected file {CHANGELOG_FILE} to exist."

    lines = CHANGELOG_FILE.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 2, (
        f"{CHANGELOG_FILE} should have at least two lines; found only {len(lines)}."
    )

    header_line = lines[0]
    section_line = lines[1]

    # Exact values from the spec
    expected_header = "## [2.5.4] - 2024-03-28"
    expected_section = "### Fixed"

    # First line: header with version and date
    assert header_line == expected_header, (
        f"First line of {CHANGELOG_FILE} should be '{expected_header}', "
        f"but found '{header_line}'."
    )

    # Second line: section indicator
    assert section_line == expected_section, (
        f"Second line of {CHANGELOG_FILE} should be '{expected_section}', "
        f"but found '{section_line}'."
    )

    # Basic sanity: ensure the very next non-blank line after the section
    # starts with a dash bullet so the file structure is intact.
    # (This guards against accidental header/section duplication.)
    for line in lines[2:]:
        if line.strip():  # first non-blank line after header + section
            assert line.startswith("- "), (
                f"Expected a bullet list after '{expected_section}' but found: '{line}'."
            )
            break


def test_release_log_absent_initially():
    assert not RELEASE_LOG.exists(), (
        f"{RELEASE_LOG} should NOT exist before the release is prepared."
    )