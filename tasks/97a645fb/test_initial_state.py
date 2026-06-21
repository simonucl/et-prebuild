# test_initial_state.py
#
# This test-suite validates ONLY the *initial* filesystem state that must be
# provided **before** the student starts working.
#
# According to the task description the machine SHOULD contain *exactly*:
#   1. A directory  : /home/user/scripts                (mode 0755)
#   2. A script file: /home/user/scripts/backup.sh      (mode 0755)
#
# Nothing else (such as /home/user/bin, the symbolic link, or the log file)
# is validated here because those items are expected to be *created later*
# by the student.  Per the rubric, we must **not** test for the presence or
# absence of any of the output resources.
#
# The tests below therefore confirm that:
#   • /home/user/scripts exists and is a directory.
#   • /home/user/scripts/backup.sh exists, is a regular file, is executable
#     by the owner, and still contains the original 4-line placeholder
#     content supplied in the specification.
#
# Any failure message should make it very clear what part of the expected
# initial state is missing or incorrect.

import os
import stat
from pathlib import Path

SCRIPTS_DIR = Path("/home/user/scripts")
BACKUP_SH   = SCRIPTS_DIR / "backup.sh"

EXPECTED_BACKUP_SH_LINES = [
    "#!/bin/bash\n",
    "# Simple backup placeholder\n",
    'echo "Backup running..."\n',
    "exit 0\n",
]


def test_scripts_directory_exists_and_is_dir():
    """
    /home/user/scripts must exist and be a directory.
    """
    assert SCRIPTS_DIR.exists(), (
        f"Expected directory '{SCRIPTS_DIR}' is missing. "
        "The initial environment must provide this directory."
    )
    assert SCRIPTS_DIR.is_dir(), (
        f"'{SCRIPTS_DIR}' exists but is not a directory. "
        "The initial environment is malformed."
    )


def test_backup_script_exists_and_is_file():
    """
    /home/user/scripts/backup.sh must exist and be a regular file.
    It must also be executable by the owner (mode 0755 or similar).
    """
    assert BACKUP_SH.exists(), (
        f"Expected script '{BACKUP_SH}' is missing from the initial environment."
    )
    assert BACKUP_SH.is_file(), (
        f"'{BACKUP_SH}' exists but is not a regular file in the initial environment."
    )

    st_mode = BACKUP_SH.stat().st_mode
    is_owner_executable = bool(st_mode & stat.S_IXUSR)
    assert is_owner_executable, (
        f"Script '{BACKUP_SH}' is not marked as executable by the owner "
        "(expected mode 0755 or similar)."
    )


def test_backup_script_contents_are_unchanged():
    """
    The script's placeholder contents should be exactly the 4 lines specified
    in the task description.  This guards against unintended pre-modification.
    """
    with BACKUP_SH.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Give a detailed diff-style message if the contents differ.
    assert lines == EXPECTED_BACKUP_SH_LINES, (
        "Contents of '/home/user/scripts/backup.sh' do not match the expected "
        "4-line placeholder provided in the specification.\n"
        "Expected:\n"
        + "".join(EXPECTED_BACKUP_SH_LINES)
        + "\nFound:\n"
        + "".join(lines)
    )