# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating-system /
# filesystem before the student performs any actions for the “incident-tools”
# emergency patch release exercise.
#
# It asserts that:
#   • the repository /home/user/incident-tools is present and is a git repo
#   • VERSION and package.json both show 1.2.3
#   • CHANGELOG.md has NOT yet been updated to 1.2.4
#   • git history matches the three expected commits after v1.2.3
#   • tag v1.2.4 does **not** exist, while v1.2.3 does
#   • the release log artefact for 1.2.4 is not yet present
#
# Only the Python standard library and pytest are used.

import json
import subprocess
from pathlib import Path

import pytest

REPO_PATH = Path("/home/user/incident-tools")
VERSION_FILE = REPO_PATH / "VERSION"
PACKAGE_JSON = REPO_PATH / "package.json"
CHANGELOG = REPO_PATH / "CHANGELOG.md"
RELEASE_LOGS_DIR = REPO_PATH / ".release_logs"
RELEASE_JSON = RELEASE_LOGS_DIR / "release_1.2.4.json"

EXPECTED_CURRENT_VERSION = "1.2.3"
NEW_VERSION = "1.2.4"

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _run_git(args):
    """Run a git command inside the repository and return (stdout, stderr)."""
    completed = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip(), completed.stderr.strip()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_repository_exists_and_is_git_repo():
    assert REPO_PATH.is_dir(), f"Repository directory {REPO_PATH} is missing."
    git_dir = REPO_PATH / ".git"
    assert git_dir.is_dir(), f"{REPO_PATH} exists but is not a git repository (missing .git directory)."


def test_version_file_contains_expected_version():
    assert VERSION_FILE.is_file(), f"VERSION file not found at {VERSION_FILE}."
    content = VERSION_FILE.read_text().strip()
    assert (
        content == EXPECTED_CURRENT_VERSION
    ), f"VERSION file should contain '{EXPECTED_CURRENT_VERSION}', found '{content}'."


def test_package_json_version_field():
    assert PACKAGE_JSON.is_file(), f"package.json not found at {PACKAGE_JSON}."
    try:
        data = json.loads(PACKAGE_JSON.read_text())
    except json.JSONDecodeError as exc:
        pytest.fail(f"package.json is not valid JSON: {exc}")

    version = data.get("version")
    assert (
        version == EXPECTED_CURRENT_VERSION
    ), f"package.json version field should be '{EXPECTED_CURRENT_VERSION}', found '{version}'."


def test_changelog_not_yet_updated():
    """
    The new 1.2.4 section must NOT yet be present in the CHANGELOG.
    """
    assert CHANGELOG.is_file(), f"CHANGELOG.md not found at {CHANGELOG}."
    changelog_text = CHANGELOG.read_text()
    forbidden_heading = f"## [{NEW_VERSION}]"
    assert (
        forbidden_heading not in changelog_text
    ), f"CHANGELOG.md already contains heading '{forbidden_heading}' but it should not exist before the release is cut."


def test_expected_git_commits_and_tags():
    # Ensure tag v1.2.3 exists
    tags_stdout, _ = _run_git(["tag", "-l", "v1.2.3"])
    assert (
        "v1.2.3" in tags_stdout.splitlines()
    ), "Expected git tag v1.2.3 to exist but it was not found."

    # Ensure tag v1.2.4 does NOT yet exist
    tags_stdout_124, _ = _run_git(["tag", "-l", "v1.2.4"])
    assert (
        "v1.2.4" not in tags_stdout_124.splitlines()
    ), "Git tag v1.2.4 already exists but should not be created until after the student performs the release."

    # Verify the last three commit messages after v1.2.3
    log_stdout, _ = _run_git(
        ["log", "--format=%s", "v1.2.3..HEAD"]  # commit subjects only
    )
    commit_messages = log_stdout.splitlines()
    expected_messages = [
        "fix(parser): handle null bytes in log stream",
        "chore(deps): bump lodash from 4.17.20 to 4.17.21",
        "docs: update contact escalation path",
    ]

    assert (
        commit_messages == expected_messages
    ), (
        "Unexpected commit messages after tag v1.2.3.\n"
        f"Expected (top-to-bottom): {expected_messages}\n"
        f"Found: {commit_messages}"
    )


def test_release_log_artifact_not_present_yet():
    """
    The machine-readable audit artefact for 1.2.4 must not pre-exist before the
    student creates it.
    """
    assert (
        not RELEASE_JSON.exists()
    ), f"Release log artefact {RELEASE_JSON} already exists; it should only be created during the release process."