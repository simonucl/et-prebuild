# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# _before_ the student carries out any actions for the “network diagnostics”
# task.  Nothing related to the final artefact should exist yet.
#
# What we verify:
#   • /home/user/network_diagnostics **must not** contain the final log file
#     /home/user/network_diagnostics/diag.log.
#   • If /home/user/network_diagnostics already exists, it must be a directory
#     (not a regular file, symlink, etc.).  Having the directory pre-created is
#     acceptable, but the log file must still be absent.
#
# These checks ensure the working environment is in a clean, predictable state
# prior to the student’s work.
#
# Only stdlib + pytest are used, per the specification.

import os
import stat
import pytest

HOME = "/home/user"
DIAG_DIR = os.path.join(HOME, "network_diagnostics")
DIAG_LOG = os.path.join(DIAG_DIR, "diag.log")


def test_diag_log_does_not_exist():
    """
    The final artefact 'diag.log' must NOT exist at the start.
    Its presence would indicate that the baseline snapshot is contaminated
    and that the student cannot demonstrate creation of the file.
    """
    assert not os.path.exists(
        DIAG_LOG
    ), (
        f"Precondition failure: {DIAG_LOG!r} already exists.\n"
        "The log file must NOT be present before the student begins; "
        "please remove it so the exercise starts from a clean slate."
    )


def test_diag_dir_is_absent_or_directory():
    """
    The parent directory may or may not exist at the outset.  If it does exist,
    it must be a directory (not a file, FIFO, symlink, etc.).
    """
    if not os.path.exists(DIAG_DIR):
        pytest.skip(f"{DIAG_DIR!r} does not exist yet—this is acceptable.")
    # Path exists: ensure it is *strictly* a directory.
    st = os.lstat(DIAG_DIR)
    assert stat.S_ISDIR(
        st.st_mode
    ), (
        f"Precondition failure: {DIAG_DIR!r} exists but is not a directory "
        f"(mode {oct(st.st_mode)}).  Remove or rename it so that the student "
        "can create the required directory."
    )