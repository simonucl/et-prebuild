# test_initial_state.py
"""
Initial-state verification for the “bash-package.log” exercise.

These tests run **before** the student performs any work.  They make sure that
the operating system already provides everything that the upcoming task
depends on—most importantly a working `dpkg` command and an installed `bash`
package.

Nothing about the yet-to-be-created output directory or files is checked here;
the rubric explicitly forbids looking for them in the initial-state suite.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize("candidate", ["/usr/bin/dpkg", "/bin/dpkg"])
def test_dpkg_binary_exists(candidate):
    """
    The Debian/Ubuntu package manager (`dpkg`) must be present as a regular,
    executable file.  We check the two canonical locations in order and accept
    the first one that satisfies the expectation.
    """
    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        # Success – no assertion failure for this candidate
        return

    # If this specific candidate is missing, defer the assertion until we have
    # tried all parametrised paths.  Pytest will report failure only if every
    # parametrised case fails.
    assert (
        False
    ), f"`dpkg` not found or not executable at expected location: {candidate!r}"


def test_dpkg_responds_to_version_request():
    """
    A basic sanity check that `dpkg` is runnable; we expect it to exit with
    status 0 when asked for its version information.
    """
    dpkg = shutil.which("dpkg")
    assert dpkg, "The `dpkg` command is not available in PATH."

    try:
        completed = subprocess.run(
            [dpkg, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"`dpkg --version` exited with non-zero status {exc.returncode}; "
            f"stderr was: {exc.stderr.strip()}"
        )

    assert (
        "Debian" in completed.stdout or "Ubuntu" in completed.stdout
    ), "`dpkg --version` output did not look like a Debian-family tool."


def test_bash_package_is_installed():
    """
    Validate that the `bash` package is reported as *installed* (`ii`) by
    `dpkg -l`.  This guarantees that the student will actually find the line
    they need to capture later.
    """
    dpkg = shutil.which("dpkg")
    assert dpkg, "The `dpkg` command is not available in PATH."

    try:
        # Use `--no-pager` to avoid any interactive paging behaviour if the
        # environment happens to inject `less`.  The option is safe even if the
        # system has no pager configured.
        output = subprocess.check_output(
            [dpkg, "-l", "bash"], text=True, stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Running `dpkg -l bash` failed with exit code {exc.returncode}.\n"
            f"Command output was:\n{exc.output}"
        )

    lines = output.splitlines()

    # Skip possible header lines (they start with `||/` or `Desired=` etc.).
    pkg_lines = [
        line
        for line in lines
        if line.startswith(("ii", "hi", "rc", "un", "pn", "ic", "iF"))
    ]

    assert (
        pkg_lines
    ), "No package-status lines were found in `dpkg -l bash` output; unexpected format."

    # Look for the exact installed marker “ii  bash ”
    installed_line = next(
        (line for line in pkg_lines if line.startswith("ii") and " bash " in line), None
    )

    assert (
        installed_line is not None
    ), "The `bash` package is not marked as installed ('ii') in `dpkg` output."


def test_bash_binary_exists_and_is_executable():
    """
    Finally, confirm that the runnable shell binary itself is present.  While
    technically independent from the `dpkg` listing, it is a sensible
    prerequisite for the assignment.
    """
    bash_path = Path("/bin/bash")
    assert bash_path.is_file(), "Expected `/bin/bash` to exist as a file."
    assert os.access(bash_path, os.X_OK), "`/bin/bash` is not executable."