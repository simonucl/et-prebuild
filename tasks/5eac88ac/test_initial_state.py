# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# *before* the student performs any action for the “permission-frequency”
# exercise.  It checks that the directory /home/user/audit_dir and its
# contents exist exactly as expected and that every regular file has the
# correct permission string.  If anything is missing or incorrect, the
# tests will fail with a clear, descriptive message.

import os
import stat
import pytest

BASE_DIR = "/home/user/audit_dir"

# Expected regular files with their corresponding permission strings.
EXPECTED_FILES = {
    os.path.join(BASE_DIR, "config.cfg"): "-rw-r--r--",
    os.path.join(BASE_DIR, "run.sh"): "-rwxr-xr-x",
    os.path.join(BASE_DIR, "temp.log"): "-rw-rw-rw-",
    os.path.join(BASE_DIR, "public.txt"): "-rw-rw-rw-",
    os.path.join(BASE_DIR, "logs", "error.log"): "-rw-r--r--",
}

# Expected directories (no need to test permissions on directories, only
# their presence/type).
EXPECTED_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "logs"),
]


def _mode_to_permstring(mode: int) -> str:
    """
    Convert a st_mode integer (as returned by os.stat().st_mode) into the
    10-character permission string produced by `ls -l`.

    Example: 0o100644 --> '-rw-r--r--'
    """
    # File type character
    if stat.S_ISDIR(mode):
        lead = "d"
    elif stat.S_ISLNK(mode):
        lead = "l"
    elif stat.S_ISREG(mode):
        lead = "-"
    elif stat.S_ISCHR(mode):
        lead = "c"
    elif stat.S_ISBLK(mode):
        lead = "b"
    elif stat.S_ISFIFO(mode):
        lead = "p"
    elif stat.S_ISSOCK(mode):
        lead = "s"
    else:
        lead = "?"

    # Permission bits
    perms = []
    for who, shifts in (
        ("USR", (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR)),
        ("GRP", (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP)),
        ("OTH", (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH)),
    ):
        perms.append("r" if mode & shifts[0] else "-")
        perms.append("w" if mode & shifts[1] else "-")
        perms.append("x" if mode & shifts[2] else "-")
    return lead + "".join(perms)


@pytest.mark.parametrize("directory", EXPECTED_DIRS)
def test_directories_exist(directory):
    assert os.path.exists(directory), f"Expected directory '{directory}' does not exist."
    assert os.path.isdir(directory), f"'{directory}' exists but is not a directory."


@pytest.mark.parametrize("path, expected_perm", EXPECTED_FILES.items())
def test_files_exist_with_correct_permissions(path, expected_perm):
    assert os.path.exists(path), f"Expected file '{path}' does not exist."
    assert os.path.isfile(path), f"'{path}' exists but is not a regular file."

    actual_perm = _mode_to_permstring(os.stat(path).st_mode)
    assert (
        actual_perm == expected_perm
    ), f"File '{path}' has permissions '{actual_perm}', expected '{expected_perm}'."