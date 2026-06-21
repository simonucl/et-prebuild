# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem *before* the student
# runs their single-command solution.  It checks that the directory tree
# and files are exactly in the expected “starting” state and that no
# “output” artefacts (e.g. the new VERSION value or release.log file)
# are present yet.
#
# The tests will fail with clear, actionable messages if anything is
# missing or already modified.

import os
from pathlib import Path

SERVICE_DIR = Path("/home/user/service")
LOGS_DIR = SERVICE_DIR / "logs"
VERSION_FILE = SERVICE_DIR / "VERSION"
CHANGELOG_FILE = SERVICE_DIR / "CHANGELOG.md"
RELEASE_LOG = LOGS_DIR / "release.log"


def test_directories_exist():
    """Verify that required directories are present."""
    assert SERVICE_DIR.is_dir(), f"Directory {SERVICE_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"Directory {LOGS_DIR} is missing."


def test_version_file_contents():
    """VERSION must exist and contain exactly '2.4.1\\n'."""
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} is missing."
    contents = VERSION_FILE.read_text(encoding="utf-8")
    expected = "2.4.1\n"
    assert contents == expected, (
        f"{VERSION_FILE} contents are incorrect.\n"
        f"Expected (repr): {repr(expected)}\n"
        f"Found    (repr): {repr(contents)}"
    )


def test_changelog_initial_contents():
    """CHANGELOG.md must match the initial state exactly."""
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} is missing."
    contents = CHANGELOG_FILE.read_text(encoding="utf-8")
    expected = (
        "# Changelog\n"
        "\n"
        "## [2.4.1] - 2023-01-15\n"
        "### Fixed\n"
        "- Memory leak in worker pool (#1220)\n"
        "\n"
    )
    assert contents == expected, (
        f"{CHANGELOG_FILE} contents do not match the required initial state.\n"
        "======= Expected =======\n"
        f"{repr(expected)}\n"
        "======== Found ========\n"
        f"{repr(contents)}"
    )


def test_release_log_does_not_exist():
    """release.log must NOT exist before the student runs their command."""
    assert not RELEASE_LOG.exists(), (
        f"{RELEASE_LOG} should not exist yet. "
        "It looks like the version bump command has already been run."
    )