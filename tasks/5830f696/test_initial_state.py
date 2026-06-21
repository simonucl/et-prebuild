# test_initial_state.py
#
# Pytest suite that validates the *starting* state of the operating system /
# filesystem before the student begins the “patch-release” exercise.
#
# These tests assert that the repository, files and directories are exactly in
# the expected pristine condition.  Any failure pin-points what is missing,
# changed or unexpectedly present.
#
# NOTE: Do *not* modify this file.  The automated evaluation system relies on
# these assertions to guarantee a known baseline before the student’s
# solution is executed.

import os
import subprocess
from datetime import datetime

import pytest

HOME = "/home/user"
REPO_ROOT = os.path.join(HOME, "projects", "acme-service")
VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")
CHANGELOG_FILE = os.path.join(REPO_ROOT, "CHANGELOG.md")
AUDIT_DIR = os.path.join(HOME, "audit")
AUDIT_FILE = os.path.join(AUDIT_DIR, "acme-service_version_bump.log")


def run_git(cmd, cwd=REPO_ROOT) -> str:
    """
    Helper: run a git command and return stdout as a decoded str (stripped).
    """
    result = subprocess.check_output(["git", *cmd], cwd=cwd)
    return result.decode().strip()


@pytest.fixture(scope="session")
def repo_exists():
    """
    Ensure that the repository directory and its .git folder exist.
    """
    if not os.path.isdir(REPO_ROOT):
        pytest.fail(f"Repository directory {REPO_ROOT!r} does not exist.")
    if not os.path.isdir(os.path.join(REPO_ROOT, ".git")):
        pytest.fail(f"{REPO_ROOT!r} is not a Git repository (missing .git).")
    return True


def test_version_file_initial_content(repo_exists):
    assert os.path.isfile(VERSION_FILE), (
        f"VERSION file expected at {VERSION_FILE!r} but was not found."
    )
    with open(VERSION_FILE, "r", encoding="utf-8") as fp:
        contents = fp.read()
    expected = "2.4.1\n"
    assert contents == expected, (
        f"VERSION file should contain exactly {expected!r} but found {contents!r}"
    )


def test_changelog_initial_structure(repo_exists):
    assert os.path.isfile(CHANGELOG_FILE), (
        f"CHANGELOG.md expected at {CHANGELOG_FILE!r} but was not found."
    )
    with open(CHANGELOG_FILE, "r", encoding="utf-8") as fp:
        lines = [line.rstrip("\n") for line in fp]

    # 1) First non-blank line must be '# Changelog'
    first_non_blank = next((ln for ln in lines if ln.strip()), None)
    assert first_non_blank == "# Changelog", (
        "The first non-blank line of CHANGELOG.md must be '# Changelog'."
    )

    # 2) Existing section for 2.4.1 must be present.
    assert any("## [2.4.1]" in ln for ln in lines), (
        "CHANGELOG.md does not contain an entry for version 2.4.1."
    )

    # 3) No section for 2.4.2 should exist yet.
    assert not any("## [2.4.2]" in ln for ln in lines), (
        "CHANGELOG.md already contains an entry for 2.4.2; "
        "this should be added by the student."
    )


def test_git_repository_state_clean(repo_exists):
    # Ensure HEAD is on branch 'main'
    branch = run_git(["symbolic-ref", "--short", "HEAD"])
    assert branch == "main", (
        f"Repository should be on 'main' branch but is on {branch!r}"
    )

    # Ensure there is exactly one commit.
    commit_count = int(run_git(["rev-list", "--count", "HEAD"]))
    assert commit_count == 1, (
        f"Repository should have exactly 1 commit but has {commit_count}."
    )

    # Working tree must be clean.
    status = run_git(["status", "--porcelain"])
    assert status == "", "Working tree is not clean; expected no untracked or modified files."


def test_audit_file_absent_initially():
    """
    The audit directory may or may not exist, but the version bump log file
    must *not* exist before the student performs the task.
    """
    if os.path.exists(AUDIT_FILE):
        pytest.fail(
            f"Audit file {AUDIT_FILE!r} already exists. "
            "It should be created only after completing the task."
        )

    # If the audit directory exists, ensure it is indeed a directory.
    if os.path.exists(AUDIT_DIR):
        assert os.path.isdir(AUDIT_DIR), (
            f"{AUDIT_DIR!r} exists but is not a directory."
        )


def test_system_time_available():
    """
    Sanity check: the system clock must be accessible so the student can log
    an ISO-8601 timestamp later.  This is also a subtle guard against sandbox
    misconfiguration where /etc/localtime or /usr/share/zoneinfo is missing.
    """
    try:
        # Should succeed without raising.
        datetime.utcnow()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to obtain UTC time via datetime.utcnow(): {exc}")