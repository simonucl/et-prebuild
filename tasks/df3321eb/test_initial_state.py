# test_initial_state.py
#
# Pytest suite to validate that the operating-system / filesystem
# is in a pristine state *before* the student performs the task
# described in the prompt.
#
# The task will eventually create:
#   /home/user/workspace/exp_42_dns/
#   ├── scripts/
#   └── artifacts/
#       ├── dns_resolution_results.csv
#       └── run.log
#
# None of the above must exist yet.  These tests assert that the
# workspace, sub-directories and artefact files are *absent* so that
# the experiment starts from a clean slate.
#
# ONLY stdlib + pytest are used, as required.

import os
import stat
import shutil
from pathlib import Path

# Base paths that will be created by the student's solution
BASE_DIR = Path("/home/user/workspace/exp_42_dns")
SCRIPTS_DIR = BASE_DIR / "scripts"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

CSV_FILE = ARTIFACTS_DIR / "dns_resolution_results.csv"
LOG_FILE = ARTIFACTS_DIR / "run.log"


def _describe_path(p: Path) -> str:
    """Human-readable description used in assertion messages."""
    return f"'{p}' (type: {'file' if p.is_file() else 'directory' if p.is_dir() else 'missing'})"


def test_exp_directory_absent():
    """
    The top-level experiment directory must not exist yet.
    A pre-existing directory indicates that the workspace is *not* clean,
    which could hide bugs in the student’s forthcoming commands.
    """
    assert not BASE_DIR.exists(), (
        f"Expected a clean state, but found existing path {_describe_path(BASE_DIR)}.\n"
        "Please remove it before starting the task so the grader can "
        "verify the directories and files you create."
    )


def test_subdirectories_absent():
    """
    Neither 'scripts/' nor 'artifacts/' should be present before the task starts.
    """
    for p in (SCRIPTS_DIR, ARTIFACTS_DIR):
        assert not p.exists(), (
            f"Found unexpected pre-existing {_describe_path(p)}.\n"
            "The environment must be clean before you begin."
        )


def test_artifact_files_absent():
    """
    The artefact files specified in the task must *not* be present yet.
    """
    for p in (CSV_FILE, LOG_FILE):
        assert not p.exists(), (
            f"Artefact file {_describe_path(p)} already exists, "
            "but this should only be created by your solution script."
        )


def test_getent_available_for_resolution():
    """
    Ensure that a basic resolver utility is available to the student.
    While any POSIX resolver (dig, host, nslookup, getent) is acceptable,
    we check for 'getent' because it is ubiquitous on most Linux systems
    and requires no special privileges.

    This is not a filesystem cleanliness check, but a sanity check that
    the student has a viable tool to implement the solution without sudo.
    """
    assert shutil.which("getent") is not None, (
        "'getent' command not found in PATH. "
        "A resolver utility (getent/host/dig/nslookup) must be available "
        "for the student to complete the task."
    )


def test_home_directory_permissions():
    """
    Confirm that /home/user and /home/user/workspace (if it exists) are
    writable by the current (non-privileged) user.  This avoids surprises
    when the student tries to create directories or files.
    """
    home = Path("/home/user")
    assert home.exists(), "The expected home directory '/home/user' is missing."

    # home must be writable; workspace *may* not exist yet, but if it does, it must be writable.
    for p in (home, home / "workspace"):
        if p.exists():
            mode = p.stat().st_mode
            is_writable = bool(mode & stat.S_IWUSR)
            assert is_writable, (
                f"The directory '{p}' is not writable by the current user. "
                "Please fix permissions so the experiment can create files."
            )