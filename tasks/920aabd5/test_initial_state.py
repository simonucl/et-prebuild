# test_initial_state.py
#
# This test-suite validates the build environment *before* the student carries
# out any actions required by the task.  It deliberately avoids checking for
# the output artefacts (/home/user/translation_update/**) because they are
# supposed to be created by the student during the exercise.

import os
import shutil
import subprocess

import pytest


def test_home_directory_exists():
    """
    The workspace for this exercise lives under /home/user, so that directory
    must already be present on the machine.
    """
    home = "/home/user"
    assert os.path.isdir(home), f"Required base directory {home!r} is missing."


def test_uname_command_is_available_and_executable():
    """
    The task relies on the standard `uname` utility being present in PATH and
    executable.  This test confirms both conditions.
    """
    uname_path = shutil.which("uname")
    assert uname_path is not None, (
        "The `uname` command is not found in the system PATH; "
        "it is required to obtain the kernel release."
    )
    assert os.access(uname_path, os.X_OK), (
        f"The `uname` command exists at {uname_path!r} but is not executable."
    )


def test_kernel_release_can_be_retrieved():
    """
    Ensure that calling `uname -r` succeeds and returns a single, non-empty
    line (without embedded newlines).  This guarantees that the information
    the student must capture is available at runtime.
    """
    try:
        kernel_release = subprocess.check_output(
            ["uname", "-r"], text=True, stderr=subprocess.STDOUT
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        pytest.fail(f"Failed to execute `uname -r`: {exc}")

    # Strip a single trailing newline for validation purposes only
    stripped = kernel_release.rstrip("\n")

    assert stripped, "The `uname -r` command returned an empty string."
    assert "\n" not in stripped, (
        "The kernel release output from `uname -r` contains unexpected "
        "newline characters."
    )