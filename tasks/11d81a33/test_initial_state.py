# test_initial_state.py
"""
Pytest suite that validates the expected _initial_ operating-system state
_before_ the student carries out any actions for the “user-login micro-service”
exercise.

The exercise specifies that the directory /home/user/dev_data/ **must already
exist** and be writable by the current user.  All artefacts the student
creates will live inside this directory, so we verify only its presence and
basic accessibility.  We deliberately **do not** test for the presence or
absence of any future output files (e.g. the SQLite database or log file)
because those belong to the *post-task* state.
"""

import os
import errno
import pytest


DEV_DATA_DIR = "/home/user/dev_data"


def _is_writable(path: str) -> bool:
    """
    Return True if the current process can create a brand-new file inside
    the given directory.  This is a slightly stronger test than os.access()
    with os.W_OK because it catches sticky-bit situations.
    """
    test_file = os.path.join(path, ".pytest_write_probe")
    try:
        with open(test_file, "w", encoding="utf-8"):
            pass
        return True
    except OSError as exc:  # pragma: no cover
        if exc.errno in (errno.EACCES, errno.EROFS):
            return False
        # Any other error means the directory exists but something strange
        # happened; treat that as non-writable for our purposes.
        return False
    finally:
        # Clean up the probe file if it was created
        try:
            os.remove(test_file)
        except FileNotFoundError:
            pass


def test_dev_data_directory_exists_and_is_writable():
    """
    1. /home/user/dev_data/ must exist and be a directory.
    2. The current user must have write permissions inside it.
    """
    assert os.path.isdir(
        DEV_DATA_DIR
    ), (
        f"The directory '{DEV_DATA_DIR}' is missing.\n"
        "Create it with:\n\n"
        "    mkdir -p /home/user/dev_data\n"
    )

    assert _is_writable(
        DEV_DATA_DIR
    ), (
        f"The directory '{DEV_DATA_DIR}' exists but is not writable by the "
        "current user.\n"
        "Adjust its permissions (e.g. `chmod u+rwx /home/user/dev_data`) before "
        "continuing."
    )