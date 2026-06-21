# test_initial_state.py
#
# This test-suite verifies that the workspace is still in its pristine,
# pre-exercise state.  None of the artefacts that the student is asked
# to create should exist **yet**, and the user’s personal crontab must
# not already contain the required job entry.

import os
import subprocess
import sys
import shutil
import pytest

HOME = "/home/user"
MAINTENANCE_DIR = os.path.join(HOME, "project", "maintenance")

CLEANUP_SH = os.path.join(MAINTENANCE_DIR, "cleanup.sh")
MAINTENANCE_LOG = os.path.join(MAINTENANCE_DIR, "maintenance.log")
CRON_SNAPSHOT = os.path.join(MAINTENANCE_DIR, "cron_snapshot.txt")

CRON_LINE = (
    "5 */6 * * * /home/user/project/maintenance/cleanup.sh "
    ">> /home/user/project/maintenance/cleanup.log 2>&1"
)


def _pretty(path: str) -> str:
    """Return a human readable path for error messages."""
    return f"‘{path}’"


@pytest.mark.parametrize(
    "path",
    [CLEANUP_SH, MAINTENANCE_LOG, CRON_SNAPSHOT],
)
def test_files_do_not_exist_yet(path):
    """
    None of the artefacts that the student is *supposed* to create
    should exist before the exercise is started.
    """
    assert not os.path.exists(
        path
    ), (
        f"{_pretty(path)} already exists. The workspace is *not* in its initial "
        "state; please start from a clean environment."
    )


def test_crontab_does_not_yet_contain_the_job():
    """
    The user’s personal crontab must *not* yet contain the job entry that the
    student will add later.
    """
    # If the system does not have the `crontab` binary at all, the environment
    # clearly cannot already contain the entry.  We therefore skip this check
    # rather than fail.
    if shutil.which("crontab") is None:
        pytest.skip("No ‘crontab’ binary found on this system.")

    try:
        current_crontab = subprocess.check_output(
            ["crontab", "-l"], stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as exc:
        # Exit status 1 with “no crontab for …” is the usual way to signal that
        # the user has *no* crontab yet.  In that case, treat the crontab as
        # empty.
        if exc.returncode == 1:
            current_crontab = ""
        else:
            # Any other error should fail the test because it is unexpected.
            pytest.fail(
                "Could not read the current crontab via ‘crontab -l’. "
                f"Command output was:\n{exc.output}"
            )

    assert (
        CRON_LINE not in current_crontab
    ), (
        "The crontab already contains the job entry *before* the student has "
        "added it:\n\n"
        f"{CRON_LINE}\n\n"
        "Start with an empty crontab or one that does not yet contain this line."
    )