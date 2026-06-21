# test_initial_state.py
#
# This pytest suite verifies the pristine state of the filesystem
# before the learner attempts the exercise.  We **expect** that the
# artefact files do NOT yet exist.  If any of them are present, the
# test will fail with a clear, descriptive message.

import os
import stat
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = os.path.join(HOME_DIR, "db_firewall_setup.sh")
LOG_PATH = os.path.join(HOME_DIR, "db_firewall_setup.log")


@pytest.fixture(scope="module")
def home_dir_exists():
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory {HOME_DIR!r} to exist, "
        "but it was not found."
    )
    return HOME_DIR


def _file_status(path):
    """
    Helper that returns a tuple (exists, is_file, mode) for the
    supplied path.  If the path does not exist, the latter two values
    are None.
    """
    if not os.path.exists(path):
        return (False, None, None)

    st = os.stat(path)
    return (True, stat.S_ISREG(st.st_mode), st.st_mode & 0o777)


@pytest.mark.parametrize("file_path", [SCRIPT_PATH, LOG_PATH])
def test_artefacts_should_not_exist_yet(home_dir_exists, file_path):
    """
    The student has not yet created any artefact files.  Ensure that
    neither the shell script nor its companion log file is present.
    """
    exists, is_file, mode = _file_status(file_path)

    assert not exists, (
        f"Found unexpected file at {file_path!r} with mode "
        f"{oct(mode) if mode is not None else 'N/A'}.  The filesystem "
        "should be clean before the exercise begins."
    )