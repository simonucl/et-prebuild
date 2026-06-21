# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the student
# starts working on the “backup / restore verification” exercise.
#
# The checks assert that:
#   1. /home/user/data exists and is a directory.
#   2. Exactly three regular files exist directly inside it:
#        file1.txt, file2.txt, file3.txt
#   3. Each of the three files has the exact expected content (including
#      trailing new-line characters).
#   4. Neither /home/user/backup_logs nor /home/user/restored_data exists yet.
#
# Any failure message should immediately tell the student what is wrong with
# the initial environment.
#
# NOTE:  This file must be executed *before* the student performs any action.
#        It purposely does NOT test for any of the artefacts that the student
#        is supposed to create.

import os
import stat
import pytest

DATA_DIR = "/home/user/data"
BACKUP_LOGS_DIR = "/home/user/backup_logs"
RESTORED_DIR = "/home/user/restored_data"

EXPECTED_FILES = {
    "file1.txt": "Alpha backup test file.\n",
    "file2.txt": "Bravo second file line 1.\nBravo line 2.\n",
    "file3.txt": "Charlie 3rd file\nlineB\n",
}


def _read_file(path):
    """Read file exactly as bytes then decode as UTF-8 without alteration."""
    with open(path, "rb") as fh:
        data = fh.read()
    return data.decode("utf-8")


def test_data_directory_exists_and_is_directory():
    assert os.path.exists(DATA_DIR), f"Directory {DATA_DIR} is missing."
    assert os.path.isdir(DATA_DIR), f"{DATA_DIR} exists but is not a directory."

    # Ensure directory has user-writable permissions (mode 0o755 expected)
    mode = stat.S_IMODE(os.stat(DATA_DIR).st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"{DATA_DIR} should have mode {oct(expected_mode)} "
        f"but has {oct(mode)} instead."
    )


def test_expected_files_present_and_no_extras():
    present = sorted(
        [
            entry
            for entry in os.listdir(DATA_DIR)
            if os.path.isfile(os.path.join(DATA_DIR, entry))
        ]
    )
    expected = sorted(EXPECTED_FILES.keys())
    assert present == expected, (
        f"{DATA_DIR} must contain exactly the files "
        f"{expected}, but currently contains {present}."
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_FILES.items())
def test_file_contents_are_exact(filename, expected_content):
    path = os.path.join(DATA_DIR, filename)
    assert os.path.isfile(path), f"Expected regular file {path} is missing."

    content = _read_file(path)
    assert (
        content == expected_content
    ), f"Content mismatch for {path!r}.\nExpected:\n{expected_content!r}\nGot:\n{content!r}"


def test_no_preexisting_output_directories():
    assert not os.path.exists(
        BACKUP_LOGS_DIR
    ), f"{BACKUP_LOGS_DIR} should NOT exist before the task starts."
    assert not os.path.exists(
        RESTORED_DIR
    ), f"{RESTORED_DIR} should NOT exist before the task starts."