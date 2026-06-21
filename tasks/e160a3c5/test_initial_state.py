# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in a pristine state *before* the student performs any actions for
# the “netdiag” task.  Nothing related to the expected artefacts must
# exist yet.  If something is already present, the environment is
# considered contaminated and the test must fail with an explanatory
# message.

import os
import stat
import pytest


NETDIAG_DIR = "/home/user/netdiag"
PING_LOG = "/home/user/netdiag/localhost_ping.log"


def _path_type(path):
    """
    Helper: return a human-readable string describing what `path` is,
    or None if it does not exist.
    """
    if not os.path.exists(path):
        return None
    st = os.lstat(path)
    if stat.S_ISDIR(st.st_mode):
        return "directory"
    if stat.S_ISREG(st.st_mode):
        return "regular file"
    if stat.S_ISLNK(st.st_mode):
        return "symlink"
    return "special file"


def test_netdiag_directory_absent():
    """
    The directory /home/user/netdiag should NOT exist yet.
    Students will create it as part of the exercise.
    """
    ptype = _path_type(NETDIAG_DIR)
    assert ptype is None, (
        f"The path {NETDIAG_DIR!r} already exists "
        f"as a {ptype}. The environment must be clean before the task begins."
    )


def test_ping_log_absent():
    """
    The file /home/user/netdiag/localhost_ping.log should NOT exist yet.
    It will be created by the student's script.
    """
    ptype = _path_type(PING_LOG)
    assert ptype is None, (
        f"The path {PING_LOG!r} already exists "
        f"as a {ptype}. The environment must be clean before the task begins."
    )