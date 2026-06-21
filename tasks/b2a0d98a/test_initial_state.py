# test_initial_state.py
#
# This pytest suite validates that the Linux VM is in the expected
# “fresh-from-the-factory” state *before* the student creates
# /home/user/finops/ and the required artefacts.
#
# We purposefully DO NOT look for /home/user/finops/ or any files that
# will later be produced there; instead, we verify that the underlying
# operating-system prerequisites (commands, files, connectivity) are in
# place so the student can complete the assignment successfully.

import os
import shutil
import subprocess

import pytest

HOME_DIR = "/home/user"

# Commands that must exist in $PATH and execute successfully.
COMMANDS_IN_ORDER = [
    "hostname",
    "ip addr show",
    "ip route show",
    "cat /etc/resolv.conf",
    "ss -tunlp",
    "ping -c 1 127.0.0.1",
]


def _base_executable(command: str) -> str:
    """
    Return the first word of a command line—
    the actual executable to look up with shutil.which().
    """
    return command.split()[0]


def _run(cmd: str, timeout: int = 5) -> subprocess.CompletedProcess:
    """Run *cmd* in the shell and return the CompletedProcess object."""
    return subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Directory / environment sanity checks
# ---------------------------------------------------------------------------


def test_home_directory_exists():
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected home directory {HOME_DIR!r} to exist and be a directory."


# ---------------------------------------------------------------------------
# Executable availability
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", COMMANDS_IN_ORDER)
def test_required_executables_present(command):
    exe = _base_executable(command)
    path = shutil.which(exe)
    assert (
        path is not None
    ), f"Required executable {exe!r} not found in $PATH; needed to run '{command}'."


# ---------------------------------------------------------------------------
# Command exit statuses
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", COMMANDS_IN_ORDER)
def test_required_commands_exit_zero(command):
    """
    Each diagnostic command that the student must later record should already
    execute successfully on the fresh VM.
    """
    cp = _run(command)
    assert cp.returncode == 0, (
        f"Command '{command}' exited with non-zero status {cp.returncode}.\n"
        f"stdout:\n{cp.stdout}\n\nstderr:\n{cp.stderr}"
    )


# ---------------------------------------------------------------------------
# File prerequisites
# ---------------------------------------------------------------------------


def test_resolv_conf_exists():
    resolv_conf = "/etc/resolv.conf"
    assert os.path.isfile(
        resolv_conf
    ), f"{resolv_conf!r} is missing; DNS resolution would fail."