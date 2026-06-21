# test_initial_state.py
#
# Pytest suite that validates the initial repository state *before* the
# student performs any actions for the “minor semantic-version bump” task.
#
# It asserts that:
#   • Required files/directories exist exactly as described.
#   • VERSION contains only “2.4.7\n”.
#   • terraform/main.tf contains *exactly two* occurrences of “v2.4.7”
#     and zero of “v2.5.0”.
#   • CHANGELOG.md already has the 2.4.7 section and *no* 2.5.0 section.
#   • logs/ exists, is writable, empty, and no version-bump.log is present.
#
# If any assertion fails, the message pin-points what is out of place
# so the learner knows what to fix.

import os
import stat
from pathlib import Path
import pytest

ROOT = Path("/home/user/projects/infra-scripts")
VERSION_FILE = ROOT / "VERSION"
TERRAFORM_FILE = ROOT / "terraform" / "main.tf"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
LOGS_DIR = ROOT / "logs"
AUDIT_LOG = LOGS_DIR / "version-bump.log"


def test_directory_structure_exists():
    assert ROOT.is_dir(), f"Expected directory {ROOT} to exist."
    assert VERSION_FILE.is_file(), f"Missing VERSION file at {VERSION_FILE}."
    assert TERRAFORM_FILE.is_file(), f"Missing Terraform file at {TERRAFORM_FILE}."
    assert CHANGELOG_FILE.is_file(), f"Missing CHANGELOG.md at {CHANGELOG_FILE}."
    assert LOGS_DIR.is_dir(), f"Missing logs directory at {LOGS_DIR}."


def test_version_file_content():
    content = VERSION_FILE.read_text(encoding="utf-8")
    assert content == "2.4.7\n", (
        f"{VERSION_FILE} should contain exactly '2.4.7\\n' but contains {repr(content)}"
    )


def test_terraform_occurrences():
    text = TERRAFORM_FILE.read_text(encoding="utf-8")
    old_count = text.count("v2.4.7")
    new_count = text.count("v2.5.0")
    assert old_count == 2, (
        f"{TERRAFORM_FILE} should contain 'v2.4.7' exactly 2 times, found {old_count}."
    )
    assert new_count == 0, (
        f"{TERRAFORM_FILE} should not yet contain 'v2.5.0' before the bump, "
        f"but found {new_count} occurrences."
    )


def test_changelog_does_not_yet_have_new_section():
    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert "## [2.5.0]" not in content, (
        f"{CHANGELOG_FILE} already contains a 2.5.0 section—should be added during the task, not before."
    )
    assert "## [2.4.7] - 2023-06-02" in content, (
        f"{CHANGELOG_FILE} is missing expected section header '## [2.4.7] - 2023-06-02'."
    )


def test_logs_directory_empty_and_writable():
    # Directory should be writable by current user
    mode = LOGS_DIR.stat().st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, f"{LOGS_DIR} is not writable by the current user."
    # Directory should be empty before the task begins
    entries = list(LOGS_DIR.iterdir())
    assert entries == [], (
        f"{LOGS_DIR} should be empty before the task starts, but contains: "
        f"{', '.join(e.name for e in entries)}"
    )
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should not exist before the version bump is performed."
    )