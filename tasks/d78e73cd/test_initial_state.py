# test_initial_state.py
#
# This pytest suite validates the filesystem **before** the student runs the
# required single-command solution.  If any test here fails, the repository
# is already in an unexpected state.

import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
BUMP_SCRIPT = PROJECT_ROOT / "scripts" / "bump_patch.sh"
BUMP_LOG = PROJECT_ROOT / "bump.log"


def read_text(path: Path) -> str:
    """Utility: read file content exactly as text."""
    return path.read_text(encoding="utf-8")


def test_version_file_exists_with_correct_content():
    assert VERSION_FILE.exists(), f"Missing VERSION file at {VERSION_FILE}"
    contents = read_text(VERSION_FILE)
    assert contents == "1.2.3\n", (
        "VERSION file must contain exactly '1.2.3' followed by a newline "
        f"(found {contents!r})"
    )


def test_changelog_initial_state():
    assert CHANGELOG_FILE.exists(), f"Missing CHANGELOG.md at {CHANGELOG_FILE}"
    changelog = read_text(CHANGELOG_FILE).splitlines(keepends=True)

    expected_lines = [
        "## [1.2.3] - 2023-11-01\n",
        "### Fixed\n",
        "- initial release\n",
    ]

    assert changelog[:3] == expected_lines, (
        "CHANGELOG.md initial three lines do not match the expected 1.2.3 "
        "section.\n"
        f"Expected: {expected_lines!r}\n"
        f"Found   : {changelog[:3]!r}"
    )

    # Ensure no 1.2.4 section has been added yet.
    for line in changelog:
        assert "## [1.2.4]" not in line, (
            "CHANGELOG.md already contains a 1.2.4 section; "
            "the bump must not have been performed yet."
        )


def test_bump_script_exists_and_executable():
    assert BUMP_SCRIPT.exists(), f"Missing bump script at {BUMP_SCRIPT}"
    mode = BUMP_SCRIPT.stat().st_mode
    assert mode & stat.S_IXUSR, (
        f"{BUMP_SCRIPT} is not executable by the user (mode {oct(mode)})"
    )


def test_bump_log_not_present_yet():
    assert not BUMP_LOG.exists(), (
        f"{BUMP_LOG} already exists; bump should not have run yet."
    )