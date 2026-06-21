# test_initial_state.py
#
# This pytest suite validates the INITIAL state of the operating system
# before the student attempts the task.  The task instructions state that
# the student must end up with:
#
#   Directory: /home/user/.iot
#   File     : /home/user/.iot/config.ini
#
# Therefore, prior to the student’s work **neither** the directory nor the
# file should exist.  If any part of the target path already exists, the
# environment is not clean and the tests must fail so the student is not
# credited for work they did not perform.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
IOT_DIR = HOME / ".iot"
CONFIG_FILE = IOT_DIR / "config.ini"


def _describe_path(p: Path) -> str:
    """
    Return a human-readable description of what exists at *p*, or a message
    indicating that nothing exists there.
    """
    if not p.exists() and not p.is_symlink():
        return f"nothing exists at {p}"
    try:
        st = p.lstat()
    except FileNotFoundError:
        return f"nothing exists at {p}"

    mode = stat.S_IFMT(st.st_mode)
    if stat.S_ISDIR(mode):
        typ = "directory"
    elif stat.S_ISLNK(mode):
        typ = "symlink"
    elif stat.S_ISREG(mode):
        typ = "regular file"
    else:
        typ = "special file"
    return f"{typ} exists at {p}"


def test_iot_directory_absent():
    """
    The directory /home/user/.iot must NOT exist yet.
    """
    assert not IOT_DIR.exists() and not IOT_DIR.is_symlink(), (
        f"Expected /home/user/.iot to be absent before the task starts, "
        f"but {_describe_path(IOT_DIR)}."
    )


def test_config_file_absent():
    """
    The file /home/user/.iot/config.ini must NOT exist yet.
    """
    assert not CONFIG_FILE.exists() and not CONFIG_FILE.is_symlink(), (
        f"Expected /home/user/.iot/config.ini to be absent before the task starts, "
        f"but {_describe_path(CONFIG_FILE)}."
    )