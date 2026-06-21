# test_initial_state.py
#
# These tests assert that the base operating-system environment is ready
# for the student to carry out the assignment, **before** the student has
# created any of the required output files or directories.  They ensure
# that fundamental prerequisites (shell, firewall binary, home directory)
# are present so the exercise can be completed, while deliberately
# avoiding any check for the files/directories the student will create.

import os
import shutil
import stat
import pytest

HOME = "/home/user"
BASH_PATH = "/bin/bash"
IPTABLES_COMMON_PATHS = ("/usr/sbin/iptables", "/sbin/iptables")


def _is_executable(path: str) -> bool:
    """Return True if `path` exists and has any execute bit set."""
    try:
        mode = os.stat(path).st_mode
    except FileNotFoundError:
        return False
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def test_home_directory_exists_and_is_directory():
    """
    The baseline image must contain the expected user home directory so that
    the student can create `/home/user/scripts` beneath it.
    """
    assert os.path.exists(HOME), (
        f"Expected base home directory {HOME!r} to exist but it is missing."
    )
    assert os.path.isdir(HOME), (
        f"Path {HOME!r} exists but is not a directory; "
        "a writable home directory is required."
    )


def test_bash_exists_and_is_executable():
    """
    The assignment requires the shebang `#!/bin/bash`; therefore `/bin/bash`
    must exist and be executable in the initial environment.
    """
    assert os.path.exists(BASH_PATH), (
        f"{BASH_PATH} is missing.  The system must have /bin/bash installed."
    )
    assert _is_executable(BASH_PATH), (
        f"{BASH_PATH} exists but is not executable; "
        "ensure bash is correctly installed with execute permissions."
    )


def test_iptables_available_in_path_or_common_locations():
    """
    The helper script will invoke `iptables`, so the binary must be available.
    We accept any of:
      • Found in the user's PATH (via shutil.which)
      • Located at /usr/sbin/iptables
      • Located at /sbin/iptables
    """
    iptables_in_path = shutil.which("iptables")

    iptables_present = (
        iptables_in_path is not None
        or any(os.path.exists(p) for p in IPTABLES_COMMON_PATHS)
    )

    tested_paths = [iptables_in_path] if iptables_in_path else []
    tested_paths.extend(p for p in IPTABLES_COMMON_PATHS if os.path.exists(p))

    assert iptables_present, (
        "The `iptables` binary could not be located in $PATH nor at any of the "
        "common system locations:\n"
        f"  Searched PATH result : {iptables_in_path}\n"
        f"  Checked explicit paths: {', '.join(IPTABLES_COMMON_PATHS)}\n"
        "Install iptables or adjust the environment before the assignment begins."
    )

    # Additionally, whichever binary we found must be executable
    for path in tested_paths:
        assert _is_executable(path), (
            f"`iptables` was found at {path!r} but is not executable.  "
            "Please correct its permissions."
        )