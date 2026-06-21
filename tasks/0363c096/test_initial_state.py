# test_initial_state.py
#
# This test-suite validates that the operating-system is in the
# expected *initial* state, i.e. **before** the student carries out
# the task of creating the inventory log.
#
# Key expectations BEFORE the student’s work starts:
#   • /home/user exists and is a directory.
#   • /home/user/etl/pip_packages.log must NOT exist yet.
#   • A usable “pip” installation is available and returns at least
#     two installed packages.
#
# Any failure here indicates that the execution environment is not
# clean or is missing critical tooling that the student’s solution
# relies on.

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HOME_DIR = Path("/home/user")
ETL_DIR = HOME_DIR / "etl"
LOG_FILE = ETL_DIR / "pip_packages.log"

PIP_CMD = [sys.executable, "-m", "pip", "list", "--format=columns", "--disable-pip-version-check"]

PACKAGE_LINE_RE = re.compile(r"^[A-Za-z0-9_.-]+\s+[0-9a-zA-Z+._-]+$")


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------
def _run_pip_list():
    """
    Run 'python -m pip list --format=columns' and return stdout as list of
    stripped lines. Pytest is allowed to capture stderr automatically.
    """
    proc = subprocess.run(
        PIP_CMD,
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0, (
        "Unable to execute pip. Expected to succeed with command:\n"
        f"    {' '.join(PIP_CMD)}\n"
        f"STDERR:\n{proc.stderr}"
    )

    return [line.rstrip("\n") for line in proc.stdout.splitlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_home_directory_exists():
    assert HOME_DIR.is_dir(), (
        f"Expected the home directory {HOME_DIR} to exist and be a directory."
    )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"The log file {LOG_FILE} already exists, but the student has not yet "
        "had a chance to create it. Please reset the environment."
    )


def test_etl_directory_absent_or_empty_of_log():
    """
    The /home/user/etl directory may or may not exist before the task starts.
    However, if it DOES exist, the specific output file must not be present.
    """
    if ETL_DIR.exists():
        assert ETL_DIR.is_dir(), (
            f"Expected {ETL_DIR} to be a directory if it exists."
        )
        assert not LOG_FILE.exists(), (
            f"{LOG_FILE} should not be present before the task is performed."
        )


def test_pip_available_and_lists_packages():
    lines = _run_pip_list()

    # pip list in "columns" format always starts with two header lines:
    # "Package   Version" followed by "-------   -------"
    assert len(lines) >= 3, (
        "pip list returned fewer lines than expected; cannot locate any "
        "installed packages."
    )

    header1, header2, *package_lines = lines

    # Basic sanity check on headers
    assert header1.lower().startswith("package"), (
        "Unexpected first header line from 'pip list'. "
        "Got: {!r}".format(header1)
    )
    assert set(header2) <= {" ", "-"}, (
        "Unexpected second header line from 'pip list'. "
        "Got: {!r}".format(header2)
    )

    # There should be at least two package entries to make the forthcoming
    # alphabetical-sort check in the **final** tests meaningful.
    assert len(package_lines) >= 2, (
        "Expected at least two installed packages, found only "
        f"{len(package_lines)}.\nFull output:\n" + "\n".join(lines)
    )

    # Ensure each package line matches the form "<name><spaces><version>"
    malformed = [
        line for line in package_lines if not PACKAGE_LINE_RE.match(line)
    ]
    assert not malformed, (
        "The following lines from 'pip list' were not recognised as valid "
        "package entries:\n" + "\n".join(malformed)
    )