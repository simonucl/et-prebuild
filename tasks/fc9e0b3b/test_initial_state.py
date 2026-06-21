# test_initial_state.py
#
# This pytest suite validates that the operating-system state is ready
# for the “backup reference moment” exercise *before* the student
# performs any action.  It checks only the prerequisites and **does not**
# examine the files or directories that the student is expected to
# create or modify.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")


def test_home_directory_exists_and_is_directory():
    """
    The home directory `/home/user` must be present and must be a directory
    so that the student has somewhere to create `backup_logs/` later.
    """
    assert HOME.exists(), "Expected '/home/user' to exist, but it is missing."
    assert HOME.is_dir(), (
        f"Expected '/home/user' to be a directory, "
        f"but found a different file type ({HOME.stat().st_mode:o})."
    )


def test_home_directory_is_writable():
    """
    The student will need write permissions to create the backup_logs
    directory and the log file.  Verify that the current process can
    write to /home/user.
    """
    assert os.access(HOME, os.W_OK), (
        "The directory '/home/user' is not writable—cannot create "
        "'backup_logs' or any files inside."
    )


def _is_executable(path: Path) -> bool:
    """Return True if *path* exists and has at least one executable bit set."""
    try:
        mode = path.stat().st_mode
    except FileNotFoundError:
        return False
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def test_shell_utilities_available():
    """
    The student is expected to use a shell built-in like `echo` or the
    external `printf`.  Make sure standard locations for these utilities
    exist and are executable.  We do *not* mandate which one the student
    must use; we just ensure that at least one viable option is present.
    """
    echo_paths = [Path("/bin/echo"), Path("/usr/bin/echo")]
    printf_paths = [Path("/bin/printf"), Path("/usr/bin/printf")]

    echo_available = any(_is_executable(p) for p in echo_paths)
    printf_available = any(_is_executable(p) for p in printf_paths)

    assert echo_available or printf_available, (
        "Neither 'echo' nor 'printf' was found in standard locations "
        "(/bin or /usr/bin).  At least one of them must be present and "
        "executable so the student can write to the log file."
    )