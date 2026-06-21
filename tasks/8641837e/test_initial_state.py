# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student begins the task.  The required artefacts listed in
# the assignment specification must *not* exist yet.  If any of them
# are already present, the environment is dirty and should be cleaned
# before grading proceeds.

import os
import pwd
import stat
import pytest

HOME = "/home/user"
AUDIT_DIR = os.path.join(HOME, "audit_reports")
SCRIPT_PATH = os.path.join(AUDIT_DIR, "disk_audit.sh")
CRON_PATH = os.path.join(AUDIT_DIR, "cron_schedule.txt")
TRAIL_PATH = os.path.join(AUDIT_DIR, "audit_trail.log")


def _human(path):
    """Return a human-readable form of the path for error messages"""
    return f"'{path}'"


def test_home_directory_exists():
    """Sanity-check that the /home/user directory exists and is a directory."""
    assert os.path.isdir(HOME), (
        f"Expected the home directory {_human(HOME)} to exist before the "
        "exercise starts."
    )


@pytest.mark.parametrize(
    "path, description",
    [
        (AUDIT_DIR, "audit_reports directory"),
        (SCRIPT_PATH, "disk_audit.sh script"),
        (CRON_PATH, "cron_schedule.txt file"),
        (TRAIL_PATH, "audit_trail.log file"),
    ],
)
def test_task_artefacts_absent(path, description):
    """
    None of the artefacts the student is supposed to create should exist
    before the task begins.  Their presence would indicate a contaminated
    starting environment.
    """
    assert not os.path.exists(path), (
        f"The {description} {_human(path)} already exists. "
        "The environment must be clean before the student attempts the task."
    )


def test_no_residual_permissions():
    """
    If the audit_reports directory *does* exist for some unforeseen reason,
    ensure it is not a mis-configured leftover from a previous run
    (e.g. wrong owner, wrong mode).  This test is only precautionary and
    will be skipped unless the directory is present.
    """
    if not os.path.exists(AUDIT_DIR):
        pytest.skip("audit_reports directory absent, no permission checks needed.")

    # Directory exists: verify it is empty and not yet prepared.
    # 1. It should contain no files relevant to this exercise.
    unwanted = [
        name
        for name in os.listdir(AUDIT_DIR)
        if name in {os.path.basename(SCRIPT_PATH),
                    os.path.basename(CRON_PATH),
                    os.path.basename(TRAIL_PATH)}
    ]
    assert not unwanted, (
        "Found unexpected files inside the pre-existing "
        f"{_human(AUDIT_DIR)} directory: {unwanted}"
    )

    # 2. Owner should be the current user.
    uid = os.stat(AUDIT_DIR).st_uid
    current_uid = os.getuid()
    assert uid == current_uid, (
        f"The directory {_human(AUDIT_DIR)} exists but is not owned by the "
        "current un-privileged user."
    )

    # 3. Mode should be writable by user (at least 0o700) so the student
    #    can place files there.
    mode = stat.S_IMODE(os.stat(AUDIT_DIR).st_mode)
    assert mode & stat.S_IWUSR, (
        f"The directory {_human(AUDIT_DIR)} exists but is not writable by the "
        "current user (mode {:o}).".format(mode)
    )