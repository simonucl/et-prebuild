# test_initial_state.py
#
# This test-suite validates that the host is ready **before** the student
# begins the exercise.  It deliberately avoids touching or even mentioning
# any of the files / directories that the student will be asked to create
# (per project rules).  The checks focus only on prerequisites that must
# already be in place.

import os
import shutil
import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "tool",
    ["make", "date"],
)
def test_required_cli_tools_exist(tool):
    """
    Ensure that essential CLI tools are available in the PATH.

    These tools are pre-requisites for the student’s Makefile solution:
      • `make` – used to drive the automation
      • `date` – used to generate ISO-8601 timestamps

    We do *not* attempt to inspect any yet-to-be-created directories or files.
    """
    full_path = shutil.which(tool)
    assert full_path is not None, (
        f"Required command '{tool}' is not available in PATH. "
        "The exercise cannot proceed without it."
    )


def test_date_supports_Iseconds():
    """
    Verify that the host `date` implementation supports the `-Iseconds` flag,
    which the forthcoming Makefile relies upon for timestamp generation.
    """
    try:
        completed = subprocess.run(
            ["date", "-Iseconds"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        pytest.fail(
            "Running `date -Iseconds` failed. "
            "The exercise requires a `date` command that supports this flag. "
            f"Underlying error: {exc}"
        )

    output = completed.stdout.strip()
    # ISO-8601 timestamps contain a 'T' separating date and time; quick sanity-check.
    assert "T" in output, (
        "The output from `date -Iseconds` does not look like an ISO-8601 "
        f"timestamp: {output!r}"
    )


def test_running_on_unix():
    """
    The exercise targets a Unix-like environment.
    """
    assert os.name == "posix", (
        "These tasks must be executed on a POSIX/Unix system. "
        f"Detected os.name={os.name!r}."
    )


def test_home_directory_exists():
    """
    Basic sanity check that the expected home directory is present.
    """
    home = "/home/user"
    assert os.path.isdir(home), (
        f"Expected home directory {home} is missing. "
        "The exercise presumes this location exists."
    )