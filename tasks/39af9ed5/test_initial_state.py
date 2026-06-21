# test_initial_state.py
#
# This pytest suite verifies that the **initial** operating-system state
# provides every tool needed to complete the assignment *before* the
# student makes any changes.  It purposefully avoids looking for any of
# the artefacts the student will create (directory `/home/user/sysadmin_logs`
# and the two files inside it) in order to comply with the grading rules.

import os
import shutil
import stat
import subprocess

import pytest


HOME_DIR = "/home/user"
REQUIRED_COMMANDS = [
    "dpkg-query",   # used to obtain package versions
    "sha256sum",    # used to compute SHA-256 checksums
]


@pytest.mark.parametrize("command", REQUIRED_COMMANDS)
def test_required_command_in_path(command):
    """
    Ensure that every external command the instructions rely on is available
    in the current $PATH.
    """
    executable = shutil.which(command)
    assert executable is not None, (
        f"The command '{command}' must be installed and discoverable via $PATH "
        "for the exercise to be solvable, but it was not found."
    )
    assert os.access(executable, os.X_OK), (
        f"The resolved path '{executable}' for command '{command}' is not "
        "marked executable."
    )


@pytest.mark.parametrize("package", ["bash", "coreutils", "grep"])
def test_core_packages_are_installed(package):
    """
    Verify that the three core Debian packages required by the assignment
    are present in the local dpkg database and have non-empty version strings.
    """
    # dpkg-query exits with code 0 and prints the version if the package exists
    cmd = ["dpkg-query", "-W", "-f=${Version}", package]
    try:
        version = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"The package '{package}' does not appear to be installed or "
            f"querying it failed (exit code {exc.returncode}).  "
            "The assignment requires it to be present."
        )

    assert version, (
        f"The package '{package}' is installed but its version string could "
        "not be determined (empty response from dpkg-query)."
    )


def test_home_directory_exists_and_is_writable():
    """
    Confirm that the working directory '/home/user' exists and the current
    (non-root) user has write permissions there so they can create the required
    sub-directory and files.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory '{HOME_DIR}' to exist, but it was not "
        "found.  A writable home directory is necessary for the exercise."
    )

    # Check write permission for the current user
    can_write = os.access(HOME_DIR, os.W_OK)
    # As a safety net, also check sticky/permission bits that may interfere.
    st_mode = os.stat(HOME_DIR).st_mode
    is_read_only = bool(st_mode & (stat.S_ISVTX | stat.S_IRUSR == 0))

    assert can_write and not is_read_only, (
        f"The home directory '{HOME_DIR}' is not writable by the current user. "
        "The student must be able to create files and directories there."
    )