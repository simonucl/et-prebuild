# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
*before* the student starts working on the task “prepare rsync firewall rules”.

What must *NOT* exist yet (clean slate):
    • Directory /home/user/fw_backup
    • File      /home/user/fw_backup/backup_fw_rules.sh
    • File      /home/user/fw_backup/backup_fw_rules.sha256
"""

import os
import stat
import pytest


FW_BACKUP_DIR = "/home/user/fw_backup"
SCRIPT_FILE   = os.path.join(FW_BACKUP_DIR, "backup_fw_rules.sh")
SHA_FILE      = os.path.join(FW_BACKUP_DIR, "backup_fw_rules.sha256")


def _human_mode(mode: int) -> str:
    """
    Render a human-readable string such as “0o755” from an st_mode integer.
    Helps to present clearer assertion messages.
    """
    return oct(mode & 0o777)


@pytest.mark.parametrize(
    "path, kind",
    [
        (FW_BACKUP_DIR, "directory"),
        (SCRIPT_FILE,   "file"),
        (SHA_FILE,      "file"),
    ],
)
def test_paths_do_not_exist(path: str, kind: str):
    """
    The dedicated working directory and both expected artefacts
    must be absent before the student starts working.
    """
    assert not os.path.exists(path), (
        f"Unexpected {kind} “{path}” already exists. "
        f"Start with a clean environment as described in the task instructions."
    )


def test_script_is_not_executable_yet():
    """
    If, against expectations, the script file already exists,
    ensure it is *not* executable; the executable bit will be set by the student.
    """
    if not os.path.isfile(SCRIPT_FILE):
        pytest.skip(f"{SCRIPT_FILE} is not present (as expected).")
    mode = os.stat(SCRIPT_FILE).st_mode
    is_exec = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert not is_exec, (
        f"{SCRIPT_FILE} should not be executable yet "
        f"(found permissions {_human_mode(mode)})."
    )