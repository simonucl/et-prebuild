# test_initial_state.py
"""
Pytest suite that verifies the **initial** state of the workspace
*before* the student performs any action on the version bump task.

The tests assert that:

1. The project directory exists at /home/user/project.
2. /home/user/project/VERSION exists and contains exactly "1.2.3\n".
3. /home/user/project/CHANGELOG.md exists and contains only the pre-bump
   changelog text (no extra lines, no missing lines).
4. /home/user/version_bump.log does NOT exist yet.

If any assertion fails, the student’s workspace is not in the expected
starting state and subsequent grading will be unreliable.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
VERSION_FILE = PROJECT_DIR / "VERSION"
CHANGELOG = PROJECT_DIR / "CHANGELOG.md"
LOG_FILE = HOME / "version_bump.log"

# ---------- EXPECTED BYTE-EXACT CONTENTS ----------
EXPECTED_VERSION_CONTENT = b"1.2.3\n"

EXPECTED_CHANGELOG_CONTENT = (
    b"# Changelog\n"
    b"\n"
    b"## [1.2.3] - 2023-07-12\n"
    b"### Added\n"
    b"- Initial release.\n"
)

# ----------------------- TESTS -----------------------


def test_project_directory_exists():
    assert PROJECT_DIR.exists(), (
        f"Required directory {PROJECT_DIR} is missing."
    )
    assert PROJECT_DIR.is_dir(), (
        f"{PROJECT_DIR} exists but is not a directory."
    )


def test_version_file_initial_content():
    assert VERSION_FILE.exists(), (
        f"Required file {VERSION_FILE} is missing."
    )
    assert VERSION_FILE.is_file(), (
        f"{VERSION_FILE} exists but is not a regular file."
    )

    content = VERSION_FILE.read_bytes()
    assert content == EXPECTED_VERSION_CONTENT, (
        f"{VERSION_FILE} should contain exactly {EXPECTED_VERSION_CONTENT!r} "
        f"but contains {content!r}."
    )


def test_changelog_initial_content():
    assert CHANGELOG.exists(), (
        f"Required file {CHANGELOG} is missing."
    )
    assert CHANGELOG.is_file(), (
        f"{CHANGELOG} exists but is not a regular file."
    )

    content = CHANGELOG.read_bytes()
    assert content == EXPECTED_CHANGELOG_CONTENT, (
        f"{CHANGELOG} does not match the expected initial content.\n"
        f"Expected (bytes):\n{EXPECTED_CHANGELOG_CONTENT!r}\n\n"
        f"Found (bytes):\n{content!r}"
    )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"File {LOG_FILE} should NOT exist before the task is performed."
    )