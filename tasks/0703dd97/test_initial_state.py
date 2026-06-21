# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student performs the version-bump task for the “cloud-migrate” project.
#
# What is verified:
# 1. Required directory `/home/user/cloud-migrate` exists.
# 2. File `/home/user/cloud-migrate/VERSION`
#    • exists,
#    • contains exactly "1.2.3\n" (one line, LF newline, nothing else).
# 3. File `/home/user/cloud-migrate/CHANGELOG.md`
#    • exists,
#    • contains exactly the two-line header and the bullet line shown in the
#      task description – with Unix line endings – and nothing else.
# 4. File `/home/user/cloud-migrate/version_bump.log`
#    • must **NOT** exist yet.
#
# Failure messages are explicit so that the learner immediately knows what is
# missing or incorrect.

from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/cloud-migrate")
VERSION_FILE = BASE_DIR / "VERSION"
CHANGELOG_FILE = BASE_DIR / "CHANGELOG.md"
LOG_FILE = BASE_DIR / "version_bump.log"

EXPECTED_VERSION_CONTENT = "1.2.3\n"
EXPECTED_CHANGELOG_CONTENT = (
    "## [1.2.3] - 2023-09-30\n"
    "### Added\n"
    "- Initial deployment pipeline for staging.\n"
)


def test_project_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected directory {BASE_DIR} to exist. "
        "Create it before proceeding with the task."
    )


def test_version_file_initial_state():
    assert VERSION_FILE.is_file(), (
        f"Missing {VERSION_FILE}. It must exist with the original version string."
    )

    data = VERSION_FILE.read_bytes()
    expected = EXPECTED_VERSION_CONTENT.encode()
    assert (
        data == expected
    ), (
        f"{VERSION_FILE} contents are incorrect.\n"
        f"Expected (byte-exact): {EXPECTED_VERSION_CONTENT!r}\n"
        f"Found:                  {data.decode(errors='replace')!r}"
    )


def test_changelog_initial_state():
    assert CHANGELOG_FILE.is_file(), (
        f"Missing {CHANGELOG_FILE}. The changelog must be present before you start."
    )

    data = CHANGELOG_FILE.read_bytes()
    expected = EXPECTED_CHANGELOG_CONTENT.encode()
    assert (
        data == expected
    ), (
        f"{CHANGELOG_FILE} contents are incorrect.\n"
        "It must contain only the initial 1.2.3 entry exactly as described.\n"
        "Ensure line endings are Unix (LF) and there are no extra or missing lines."
    )


def test_log_file_absence():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist yet. "
        "It must be created only after performing the version bump."
    )