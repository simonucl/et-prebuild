# test_initial_state.py
#
# This pytest suite verifies that the repository is in its ORIGINAL state
# *before* the student applies the required patch-level bump.  It checks:
#
#   • VERSION file still says 1.4.2
#   • CHANGELOG.md starts with the 1.4.2 section (i.e. no 1.4.3 section yet)
#   • version_update.log exists but does NOT yet contain the 1.4.3 audit line
#
# If any of these assertions fail, the setup is already in the “after” state
# or is otherwise inconsistent with the task description, and the exercise
# should not proceed.

import pathlib
import pytest

# --------------------------------------------------------------------------- #
# Paths used throughout the tests                                             #
# --------------------------------------------------------------------------- #
BASE_DIR      = pathlib.Path("/home/user/infrastructure-tools/service-monitor")
VERSION_FILE  = BASE_DIR / "VERSION"
CHANGELOG_MD  = BASE_DIR / "CHANGELOG.md"
AUDIT_LOG     = pathlib.Path("/home/user/version_update.log")

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
NEW_VERSION_STR           = "1.4.3"
NEW_VERSION_AUDIT_LINE    = "2023-10-05 v1.4.3 semantic bump prepared"
CURRENT_VERSION_STR       = "1.4.2"
CURRENT_CHANGELOG_HEADER  = "## [1.4.2] - 2023-09-10"


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_repository_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected repository directory {BASE_DIR} to exist, but it is missing."
    )


def test_version_file_contains_original_version():
    assert VERSION_FILE.is_file(), (
        f"Expected VERSION file at {VERSION_FILE} to exist, but it is missing."
    )

    contents = VERSION_FILE.read_text(encoding="utf-8")
    assert contents == f"{CURRENT_VERSION_STR}\n", (
        "VERSION file should contain the original version "
        f"'{CURRENT_VERSION_STR}\\n' but found:\n{repr(contents)}"
    )
    # Guard against accidental pre-increment
    assert NEW_VERSION_STR not in contents, (
        f"VERSION file already contains '{NEW_VERSION_STR}', "
        "but the bump should not have happened yet."
    )


def test_changelog_starts_with_original_section():
    assert CHANGELOG_MD.is_file(), (
        f"Expected CHANGELOG.md at {CHANGELOG_MD} to exist, but it is missing."
    )

    with CHANGELOG_MD.open("r", encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\n")

    # Ensure the 1.4.2 header is still first
    assert first_line == CURRENT_CHANGELOG_HEADER, (
        "First line of CHANGELOG.md should be the header for version 1.4.2 "
        f"({CURRENT_CHANGELOG_HEADER!r}) but found {first_line!r}."
    )

    # Ensure the new 1.4.3 section is NOT yet present at the top
    assert first_line != f"## [{NEW_VERSION_STR}] - 2023-10-05", (
        "CHANGELOG.md already contains the 1.4.3 header at the top, "
        "but it should only be added by the student."
    )


def test_audit_log_exists_and_has_no_new_version_entry():
    # The log must exist (it might be empty or contain older entries).
    assert AUDIT_LOG.is_file(), (
        f"Expected audit log at {AUDIT_LOG} to exist, but it is missing."
    )

    lines = [
        ln.strip("\n") for ln in AUDIT_LOG.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]

    if lines:
        last_line = lines[-1]
        assert last_line != NEW_VERSION_AUDIT_LINE, (
            "Audit log already contains the 1.4.3 audit entry:\n"
            f"    {NEW_VERSION_AUDIT_LINE}\n"
            "but this should only be written after the student completes the task."
        )