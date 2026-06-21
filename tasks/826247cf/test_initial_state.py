# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected **initial** state _before_ the student performs any
# task-related actions.  In this context, “expected” means that none of the
# artefacts the student is supposed to create (directory, file, file content)
# should exist yet.  If any of them already exist, the test will fail with a
# clear, descriptive message so that the learner (or the automated judge)
# knows what must be cleaned up or reset prior to starting the exercise.
#
# Rules enforced:
#   1. /home/user/network_reports                – must *not* exist.
#   2. /home/user/network_reports/dns_snapshot.log – must *not* exist.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import pytest

HOME_DIR = "/home/user"
TARGET_DIR = os.path.join(HOME_DIR, "network_reports")
TARGET_FILE = os.path.join(TARGET_DIR, "dns_snapshot.log")


def _readable_mode(path: str) -> str:
    """
    Helper that returns the octal permission bits (e.g., '0755')
    for diagnostics, or 'N/A' if the path does not exist.
    """
    try:
        mode = os.stat(path).st_mode
        return oct(stat.S_IMODE(mode)).zfill(4)
    except FileNotFoundError:
        return "N/A"


@pytest.mark.order(1)
def test_network_reports_directory_absent():
    """
    The directory /home/user/network_reports must NOT exist at the start
    of the exercise.  Its presence implies that the student (or a previous
    run) has already created artefacts and the environment is no longer
    pristine.
    """
    assert not os.path.exists(TARGET_DIR), (
        f"Unexpected directory present: {TARGET_DIR!r}\n"
        f"Current mode: {_readable_mode(TARGET_DIR)}\n"
        "Please remove or rename this directory so the exercise starts from a clean state."
    )


@pytest.mark.order(2)
def test_dns_snapshot_file_absent():
    """
    The file dns_snapshot.log (or even its parent directory) must NOT
    exist at the start of the exercise.
    """
    assert not os.path.exists(TARGET_FILE), (
        f"Unexpected file present: {TARGET_FILE!r}\n"
        f"Current mode: {_readable_mode(TARGET_FILE)}\n"
        "Delete this file (and its parent directory if needed) before beginning the task."
    )