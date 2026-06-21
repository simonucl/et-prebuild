# test_initial_state.py
#
# This pytest suite validates that the operating-system environment is
# ready *before* the student starts the assignment.  It purposefully
# avoids mentioning (or checking) any of the output files/directories
# the student is expected to create, in accordance with the grading
# specification.
#
# The checks focus on:
#   • Availability of essential command-line tools.
#   • Existence of the expected home directory.
#   • Basic writability of a temporary location.
#
# Only the Python standard library and pytest are used.

import os
import shutil
import stat
import tempfile

import pytest


@pytest.mark.parametrize(
    "executable",
    [
        "ssh-keygen",
        "mkdir",
        "chmod",
        "cat",
        "echo",
    ],
)
def test_required_executables_present(executable):
    """
    Verify that every command listed in the assignment's hint section is
    available in the current PATH.  If any are missing, the student will
    not be able to complete the task.
    """
    path = shutil.which(executable)
    assert path is not None, f"Required executable '{executable}' not found in PATH."
    assert os.access(path, os.X_OK), f"'{executable}' exists but is not executable: {path}"


def test_home_directory_exists_and_is_directory():
    """
    Ensure that the /home/user directory—where all task artefacts will
    eventually reside—already exists and is a directory.
    """
    home_dir = "/home/user"
    assert os.path.exists(home_dir), f"Expected home directory '{home_dir}' is missing."
    assert os.path.isdir(home_dir), f"'{home_dir}' exists but is not a directory."


def test_temp_directory_is_writable():
    """
    Basic sanity check that a temporary directory can be created and
    written to.  This guarantees that the filesystem is writable for the
    upcoming operations without touching any of the paths the student is
    supposed to create.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "probe.txt")
        try:
            with open(test_file, "w") as fh:
                fh.write("probe")
        except OSError as exc:
            pytest.fail(f"Cannot write to temporary directory '{tmpdir}': {exc}")
        assert os.path.exists(test_file), "Failed to create a file in the temporary directory."


def test_home_directory_permissions():
    """
    The home directory should *not* be world-writable; this prevents
    permission issues later when the student sets restrictive modes on
    newly created paths.
    """
    st = os.stat("/home/user")
    mode = stat.S_IMODE(st.st_mode)
    assert (mode & stat.S_IWOTH) == 0, (
        "/home/user is world-writable, which would interfere with setting "
        "secure permissions during the assignment."
    )