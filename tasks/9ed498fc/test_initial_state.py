# test_initial_state.py
#
# This test-suite validates that the playground is ready *before* the student
# starts creating the required directory structure / permission snapshot.
#
# IMPORTANT:  We intentionally do *not* reference any of the paths that the
# assignment will ask the student to create (e.g. “/home/user/my_site”, the
# “public” sub-directory, or the snapshot log file) because such artefacts do
# not exist yet and must not be touched here.  The purpose of this file is
# solely to confirm that the baseline environment is sane and writable.

import os
import stat
import tempfile
import pytest


HOME_DIR = "/home/user"


def test_home_directory_exists_and_is_dir():
    """
    The home directory `/home/user` must exist and be a directory so that the
    student has a predictable starting point for all subsequent commands.
    """
    assert os.path.exists(
        HOME_DIR
    ), f"Expected the directory {HOME_DIR!r} to exist, but it does not."
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected {HOME_DIR!r} to be a directory, but it is not."


def test_home_directory_is_writable_by_current_user():
    """
    The student must be able to create files / directories underneath `/home/user`.
    We therefore try to create and delete a temporary file inside that directory.
    """
    # The parent must be writable *and* searchable/executable.
    st = os.stat(HOME_DIR)
    mode = stat.S_IMODE(st.st_mode)

    # Check write & execute bits for the owner.  (We don’t assume group/world.)
    owner_write = bool(mode & stat.S_IWUSR)
    owner_exec = bool(mode & stat.S_IXUSR)

    assert owner_write and owner_exec, (
        f"The directory {HOME_DIR!r} should be writable and searchable by its "
        "owner so the student can work inside it, but the current permission "
        f"mode is {oct(mode)}."
    )

    # Additionally, perform a practical check by creating an actual file.
    try:
        with tempfile.NamedTemporaryFile(dir=HOME_DIR, delete=True) as tmp:
            tmp.write(b"probe")
            tmp.flush()
    except PermissionError as exc:
        pytest.fail(
            f"Failed to create a temporary file inside {HOME_DIR!r}: {exc}"
        )