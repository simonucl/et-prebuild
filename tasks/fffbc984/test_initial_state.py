# test_initial_state.py
"""
Pytest suite to validate the *initial* filesystem state **before** the student
performs any actions for the “sys-hardener” minor-release task.

It checks:
1. The repository directory exists.
2. /home/user/sys-hardener/config.yaml exists and its `version` scalar is
   exactly '1.3.4'.
3. /home/user/sys-hardener/CHANGELOG.md exists and its first three
   non-empty lines match the expected 1.3.3 section.
4. The new 1.4.0 changelog header must *not* be present yet.

Only stdlib + pytest are used.
"""

from pathlib import Path
import pytest

REPO_ROOT = Path("/home/user/sys-hardener")
CONFIG_PATH = REPO_ROOT / "config.yaml"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"


def test_repository_directory_exists():
    assert REPO_ROOT.is_dir(), (
        f"Repository directory {REPO_ROOT} does not exist. "
        "The project should be checked out to this exact path."
    )


def test_config_yaml_version_is_1_3_4():
    assert CONFIG_PATH.is_file(), f"Required file {CONFIG_PATH} is missing."

    lines = CONFIG_PATH.read_text(encoding="utf-8").splitlines()
    version_lines = [ln for ln in lines if ln.strip().startswith("version:")]

    assert version_lines, (
        f"{CONFIG_PATH} does not contain a line starting with 'version:'."
    )

    # Take the first matching line and extract the value after the colon
    version_value = version_lines[0].split("version:", 1)[1].strip()
    assert version_value == "1.3.4", (
        f"Expected version '1.3.4' in {CONFIG_PATH}, found '{version_value}'. "
        "The file must reflect the *pre-bump* version."
    )


def test_changelog_top_section_is_for_1_3_3():
    assert CHANGELOG_PATH.is_file(), f"Required file {CHANGELOG_PATH} is missing."

    # Collect the first three non-blank lines
    non_empty = [
        ln.rstrip("\n")
        for ln in CHANGELOG_PATH.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]

    expected = [
        "## [1.3.3] - 2023-07-01",
        "### Fixed",
        "- Corrected sysctl typo that prevented IPv6 RA filtering.",
    ]

    assert non_empty[:3] == expected, (
        "CHANGELOG.md does not start with the expected 1.3.3 section.\n"
        f"Expected first three non-empty lines:\n{expected}\n"
        f"Actual first three non-empty lines:\n{non_empty[:3]}"
    )


def test_changelog_does_not_contain_new_version_header():
    """
    The student has not yet performed the version bump, so the new header
    must be absent.
    """
    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    unexpected_header = "## [1.4.0] - 2023-08-15"
    assert unexpected_header not in content, (
        f"Found premature changelog header '{unexpected_header}'. "
        "The file must reflect the state *before* the release bump."
    )