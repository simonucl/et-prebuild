# test_initial_state.py
#
# This Pytest suite validates the *initial* filesystem state before the
# student performs any work.  All checks are intentionally the inverse of
# the “expected artefacts after successful completion” list: we confirm
# that nothing has been created yet, while the project directory itself
# already exists.
#
# If any of these tests fail, it means the environment is *not* in the
# pristine state required for the exercise, and the student might obtain
# false-positive results.

import os
import stat
import pytest

HOME_DIR = "/home/user"
PROJECT_DIR = f"{HOME_DIR}/project"

DB_FILE        = f"{PROJECT_DIR}/iot_devices.db"
CSV_FILE       = f"{PROJECT_DIR}/firmware_report.csv"
DEPLOY_LOGFILE = f"{PROJECT_DIR}/deployment.log"


def _human_mode(path: str) -> str:
    """Return the Unix permission bits in a human-readable string (e.g. 'rw-r--r--')."""
    mode = os.stat(path).st_mode
    return stat.filemode(mode)


def test_project_directory_exists_and_is_writable():
    """
    The base project directory *must* exist before the student starts,
    because all work happens inside it.
    """
    assert os.path.exists(PROJECT_DIR), (
        f"Required directory {PROJECT_DIR!r} does not exist."
        " The exercise instructions specify that all work starts in that"
        " directory; please create it (mkdir -p)."
    )

    assert os.path.isdir(PROJECT_DIR), (
        f"{PROJECT_DIR!r} exists but is not a directory."
    )

    # Sanity-check that the user (owner) has read/write permissions.
    st = os.stat(PROJECT_DIR)
    owner_perms = stat.S_IMODE(st.st_mode) & 0o700  # rwx for owner
    assert owner_perms & stat.S_IRUSR, (
        f"Owner does not have read permission on {PROJECT_DIR!r} "
        f"(mode={_human_mode(PROJECT_DIR)})."
    )
    assert owner_perms & stat.S_IWUSR, (
        f"Owner does not have write permission on {PROJECT_DIR!r} "
        f"(mode={_human_mode(PROJECT_DIR)})."
    )


@pytest.mark.parametrize(
    "path,description",
    [
        (DB_FILE,        "SQLite database iot_devices.db"),
        (CSV_FILE,       "CSV firmware report"),
        (DEPLOY_LOGFILE, "deployment log"),
    ],
)
def test_target_files_do_not_yet_exist(path, description):
    """
    None of the output artefacts should exist *before* the student
    begins the exercise.  Their presence would indicate that the
    environment is contaminated or that someone has already carried out
    part of the task.
    """
    assert not os.path.exists(path), (
        f"{description} must not exist at the beginning of the exercise "
        f"(unexpected path present: {path!r}).  Start with a clean slate."
    )