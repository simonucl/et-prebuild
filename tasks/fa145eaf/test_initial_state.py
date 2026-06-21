# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# filesystem *before* the student creates any artefacts for the “DNS /
# hostname resolution” mini-dataset task.
#
# The tests confirm that neither the directory
#   /home/user/ml_data/dns_test
# nor the CSV file
#   /home/user/ml_data/dns_test/localhost_ip.csv
# exist yet.  If any of them are present at this point, it means the
# environment has already been altered and the student will not see a
# clean slate.
#
# Only Python’s stdlib and pytest are used.

import os
import stat
from pathlib import Path

DIR_PATH = Path("/home/user/ml_data/dns_test")
FILE_PATH = DIR_PATH / "localhost_ip.csv"


def _describe_path(path: Path) -> str:
    """
    Return a human-readable description of what *actually* exists at ``path``,
    or 'nothing' if the path does not exist.  Helps produce clear assert
    messages.
    """
    if not path.exists():
        return "nothing"

    try:
        st = path.lstat()
    except FileNotFoundError:
        return "nothing (race condition)"
    mode = st.st_mode
    if stat.S_ISDIR(mode):
        return "a directory"
    if stat.S_ISREG(mode):
        return "a regular file"
    if stat.S_ISLNK(mode):
        return "a symlink"
    return f"an object of unknown type (mode: {oct(mode)})"


def test_dns_test_directory_absent():
    """
    The directory /home/user/ml_data/dns_test MUST NOT exist at the start of the
    exercise.  Its presence would indicate that the environment has already
    been modified or the student’s task has been pre-executed.
    """
    assert not DIR_PATH.exists(), (
        f"Expected {DIR_PATH} to be absent, but found {_describe_path(DIR_PATH)}. "
        "The initial environment must be pristine."
    )


def test_dns_csv_file_absent():
    """
    The CSV file /home/user/ml_data/dns_test/localhost_ip.csv MUST NOT exist at
    the beginning.  If it is already present, the student cannot demonstrate
    the required creation steps.
    """
    assert not FILE_PATH.exists(), (
        f"Expected {FILE_PATH} to be absent, but found {_describe_path(FILE_PATH)}. "
        "Remove the file (or start from a clean VM/sandbox) so the student can "
        "perform the task."
    )