# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state **before**
# the student performs any action.  It ensures that the starting
# conditions match the specification so that later grading logic is
# meaningful and reliable.
#
# The tests deliberately FAIL if any part of the required initial state
# is missing or has been unintentionally modified.

import os
import stat
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "finops-tool")
VERSION_FILE = os.path.join(PROJECT_DIR, "version.txt")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")
BUMP_LOG_FILE = os.path.join(PROJECT_DIR, "bump.log")


@pytest.fixture(scope="module")
def project_dir_stat():
    """Return os.stat_result for the project directory."""
    if not os.path.isdir(PROJECT_DIR):
        pytest.fail(f"Required directory missing: {PROJECT_DIR}")
    return os.stat(PROJECT_DIR)


def test_project_directory_exists_with_correct_permissions(project_dir_stat):
    # Mask to the permission bits only
    perms = stat.S_IMODE(project_dir_stat.st_mode)
    expected_perms = 0o755
    assert (
        perms == expected_perms
    ), f"{PROJECT_DIR} should have permissions {oct(expected_perms)}, found {oct(perms)}."


def _assert_file_permissions(path, expected_perms):
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert (
        perms == expected_perms
    ), f"{path} should have permissions {oct(expected_perms)}, found {oct(perms)}."


def test_version_file_contents_and_permissions():
    assert os.path.isfile(
        VERSION_FILE
    ), f"Required file missing: {VERSION_FILE!r}"

    _assert_file_permissions(VERSION_FILE, 0o644)

    with open(VERSION_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()

    expected_content = "2.1.4\n"
    assert (
        content == expected_content
    ), (
        f"{VERSION_FILE} should contain exactly {expected_content!r} "
        f"but found {content!r}."
    )


def test_changelog_file_contents_and_permissions():
    assert os.path.isfile(
        CHANGELOG_FILE
    ), f"Required file missing: {CHANGELOG_FILE!r}"

    _assert_file_permissions(CHANGELOG_FILE, 0o644)

    with open(CHANGELOG_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()

    expected_content = (
        "# Changelog\n"
        "\n"
        "## [2.1.4] - 2023-07-15\n"
        "### Fixed\n"
        "- Fixed tagging bug in cost explorer sync (#32)\n"
        "\n"
        "## [2.1.3] - 2023-06-10\n"
        "### Added\n"
        "- Added forecast cost anomaly detection (#28)\n"
    )

    assert (
        content == expected_content
    ), (
        f"{CHANGELOG_FILE} does not match the expected initial contents.\n"
        "---- Expected ----\n"
        f"{expected_content}\n"
        "---- Found ----\n"
        f"{content}\n"
    )


def test_bump_log_file_does_not_exist_yet():
    assert not os.path.exists(
        BUMP_LOG_FILE
    ), f"{BUMP_LOG_FILE} should NOT exist in the initial state."