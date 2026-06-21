# test_initial_state.py
#
# This pytest suite verifies that the execution environment contains the
# *baseline* tools a student will need **before** attempting the exercise
# described in the project statement.  These checks purposefully avoid
# touching any of the output artefacts mentioned in the specification
# (directories / files that the student is supposed to create later).

import os
import shutil
import subprocess

import pytest


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _is_executable_in_path(cmd_name: str) -> bool:
    """
    Return True iff an executable called *cmd_name* can be found via $PATH.
    shutil.which is preferred over `command -v` or similar because it is
    cross-platform and part of the Python standard library.
    """
    return shutil.which(cmd_name) is not None


# ---------------------------------------------------------------------------
# Tests – ordered from most fundamental to most specific
# ---------------------------------------------------------------------------

def test_user_home_directory_exists():
    """
    Sanity check: the canonical user home directory must be present.
    """
    home_dir = "/home/user"
    assert os.path.isdir(home_dir), (
        f"Expected user home directory '{home_dir}' to exist, "
        "but it was not found."
    )


@pytest.mark.parametrize(
    "cmd_name,package_hint",
    [
        ("nc", "netcat"),
        ("timeout", "coreutils (usually provided by the system)"),
        ("bash", "bash (usually provided by the system)"),
    ],
)
def test_required_cli_tools_are_available(cmd_name: str, package_hint: str):
    """
    Verify that the command-line tools referenced in the assignment
    ('nc', 'timeout', 'bash') are available in the current PATH.

    We do NOT attempt to check versions or behaviour here—only presence.
    """
    assert _is_executable_in_path(cmd_name), (
        f"The executable '{cmd_name}' was not found in $PATH. "
        f"Install the tool (e.g. via the '{package_hint}' package) "
        "before attempting the exercise."
    )


def test_shell_can_spawn_subprocesses():
    """
    Ensure that the Python interpreter is able to spawn a trivial subprocess
    via the system shell.  This is a defensive test; if it fails, *none* of
    the student's future commands (`nc`, `timeout`, job-control, etc.) will
    work, so we surface the issue early.
    """
    try:
        completed = subprocess.run(
            ["bash", "-c", "echo hello"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except FileNotFoundError:
        pytest.fail(
            "The 'bash' shell could not be found or executed. "
            "It is required for the assignment."
        )
    except subprocess.TimeoutExpired:
        pytest.fail(
            "Spawning a trivial subprocess via 'bash' exceeded the 5-second "
            "timeout.  Something is wrong with process creation on this "
            "system."
        )

    assert completed.stdout.strip() == "hello", (
        "Unexpected output from the test subprocess. "
        "This indicates that basic shell execution may be unreliable."
    )