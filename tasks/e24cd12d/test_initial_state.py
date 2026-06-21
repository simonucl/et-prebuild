# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the execution environment
before the student carries out the “Development-Environment Compliance Report”
task.

The checks make sure that all tools the student must query are available and
behave in an expected, parse-friendly way.  We intentionally do **not** touch
any of the artefacts the student is expected to create (e.g. the
`/home/user/compliance_audit` directory or its `report.json` file) so that the
assessment is purely about the pre-existing system state.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


# ---------- helper utilities -------------------------------------------------


def run_cmd(cmd: list[str]) -> str:
    """Run *cmd* and return the stripped stdout as a string.

    The function deliberately:
      • Captures *only* stdout (stderr is ignored).
      • Does not invoke the shell for safety.
      • Strips trailing newlines/whitespace for easy parsing.
    """
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def assert_executable_available(exe_name: str) -> Path:
    """Assert that *exe_name* is resolvable via $PATH and return its Path."""
    path = shutil.which(exe_name)
    assert path is not None, f"Expected executable '{exe_name}' to be in $PATH."
    return Path(path)


# ---------- tests ------------------------------------------------------------


def test_git_is_installed_and_reports_version():
    git_path = assert_executable_available("git")

    # Typical output: "git version 2.34.1"
    out = run_cmd([git_path, "--version"])
    prefix = "git version "
    assert out.startswith(
        prefix
    ), f"'git --version' should start with '{prefix}', got: {out!r}"

    version_part = out[len(prefix) :]
    assert (
        version_part
    ), "Could not parse a version number from 'git --version' output."
    # Basic sanity: version consists of digits and dots
    assert all(
        ch.isdigit() or ch == "." for ch in version_part
    ), f"Parsed git version looks suspicious: {version_part!r}"


def test_python3_is_installed_and_reports_version():
    py_path = assert_executable_available("python3")

    # Typical output: "Python 3.10.6"
    out = run_cmd([py_path, "--version"])
    prefix = "Python "
    assert out.startswith(
        prefix
    ), f"'python3 --version' should start with '{prefix}', got: {out!r}"

    version_part = out[len(prefix) :]
    assert version_part, "Could not parse a version number from python output."
    # Compare with sys.version_info for a rough sanity check
    current_major_minor = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert version_part.startswith(
        current_major_minor
    ), (
        "The interpreter used by pytest and the `python3` executable seem to "
        "differ; this may break the student's script. "
        f"pytest sees {current_major_minor}, but `python3` reports {version_part}."
    )


def test_gcc_is_installed_and_reports_version():
    gcc_path = assert_executable_available("gcc")

    # We only need the first line
    first_line = run_cmd([gcc_path, "--version"]).splitlines()[0]
    # Examples:
    #   "gcc (Debian 12.2.0-3) 12.2.0"
    #   "gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
    assert first_line.lower().startswith(
        "gcc"
    ), f"'gcc --version' first line should mention gcc, got: {first_line!r}"


def test_groups_command_is_available_and_works():
    """
    The student's script relies on `groups` producing a space-separated list of
    Unix groups for the current user (no colon, no header).
    """
    groups_path = shutil.which("groups")  # /usr/bin/groups on most distros
    # `groups` is sometimes a shell built-in; fall back to that if which fails
    cmd = [groups_path] if groups_path else ["groups"]

    out = run_cmd(cmd)
    # Typical output: "user adm cdrom sudo dip plugdev"
    assert out, "'groups' command returned no output."
    assert ":" not in out, (
        "Unexpected ':' found in `groups` output; the student is expected to "
        "strip the username prefix."
    )
    assert " " in out or out.isalpha(), (
        "`groups` output should list at least one group name."
    )