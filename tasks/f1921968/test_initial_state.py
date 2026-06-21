# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating-system /
# file-system *before* the student starts working on the “database backup”
# exercise.  It deliberately checks that only the resources which are supposed
# to be present up-front actually exist, and that nothing from the target
# solution is already around.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
SCRIPT = os.path.join(HOME, "backup.sh")

SERVICE_DIR = os.path.join(HOME, ".config", "systemd", "user")
SERVICE_FILE = os.path.join(SERVICE_DIR, "db-backup.service")
TIMER_FILE = os.path.join(SERVICE_DIR, "db-backup.timer")

CRON_FILE = os.path.join(HOME, "backup_cron_entry.txt")
LOG_FILE = os.path.join(HOME, "backup_task.log")


# --------------------------------------------------------------------------- #
# 1. The helper script must exist (it is provided by the exercise scaffolding)
# --------------------------------------------------------------------------- #
def test_backup_script_exists_with_correct_contents():
    msg = (
        "The helper script '{0}' must exist *before* the student starts the "
        "task.  The file is missing.".format(SCRIPT)
    )
    assert os.path.isfile(SCRIPT), msg

    expected = textwrap.dedent(
        """\
        #!/bin/bash
        echo "backup executed"
        """
    )
    with open(SCRIPT, "r", encoding="utf-8") as fh:
        contents = fh.read()

    # The file must match the expected bytes exactly (including the final \n)
    assert contents == expected, (
        f"'{SCRIPT}' does not have the expected initial contents.  It should "
        "consist of exactly two lines:\n"
        "  1. #!/bin/bash\n"
        '  2. echo "backup executed"\\n'
    )


def test_backup_script_is_NOT_executable_yet():
    """
    The exercise requires the student to make backup.sh executable.
    Therefore, at the beginning it must *not* have the executable bit set.
    """
    st_mode = os.stat(SCRIPT).st_mode
    is_executable = bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert not is_executable, (
        f"'{SCRIPT}' is already executable, but it should *not* be.  "
        "The student is supposed to add the executable bit."
    )


# --------------------------------------------------------------------------- #
# 2. No systemd artefacts should be in place yet
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path, desc",
    [
        (SERVICE_FILE, "systemd service file"),
        (TIMER_FILE, "systemd timer file"),
    ],
)
def test_no_systemd_files_present(path, desc):
    assert not os.path.exists(path), (
        f"The initial state must **not** contain the {desc} '{path}'.  "
        "It appears to exist already, which would defeat the purpose of the "
        "exercise."
    )


def test_user_systemd_directory_may_exist_but_is_not_required():
    """
    The directory ~/.config/systemd/user is allowed to be absent.
    If it already exists (for unrelated reasons), that is fine as well.
    We merely document the expectation.
    """
    # This is a sanity check; no assertion required.


# --------------------------------------------------------------------------- #
# 3. No cron artefact should exist yet
# --------------------------------------------------------------------------- #
def test_no_cron_file_present():
    assert not os.path.exists(CRON_FILE), (
        f"The cron specification '{CRON_FILE}' must not exist in the initial "
        "state.  The student is tasked with creating it."
    )


# --------------------------------------------------------------------------- #
# 4. The verification log must not exist yet
# --------------------------------------------------------------------------- #
def test_no_log_file_present():
    assert not os.path.exists(LOG_FILE), (
        f"The verification log '{LOG_FILE}' should be absent at the start.  "
        "The student will create it and append 'TASK FINISHED' once done."
    )