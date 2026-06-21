# test_initial_state.py
#
# Pytest suite to verify the **initial** state of the operating system
# before the student performs any actions for the “first-pass connectivity
# report” exercise.
#
# Expectations for the pristine state:
#   1. The directory /home/user/network_diagnostics MUST NOT exist.
#   2. Consequently, the file /home/user/network_diagnostics/diagnostics.csv
#      must also not exist.
#
# If either the directory or the file already exists, the test suite will
# fail with a clear, descriptive message.

import os
from pathlib import Path

NETWORK_DIR = Path("/home/user/network_diagnostics")
CSV_FILE = NETWORK_DIR / "diagnostics.csv"


def test_home_directory_exists():
    """
    Sanity-check that the base home directory exists so the rest of the
    assertions make sense.
    """
    home = Path("/home/user")
    assert home.is_dir(), (
        f"Expected the base home directory '{home}' to exist and be "
        "a directory, but it is missing."
    )


def test_network_diagnostics_directory_absent():
    """
    The /home/user/network_diagnostics directory must NOT be present
    before the student starts the task.
    """
    assert not NETWORK_DIR.exists(), (
        f"The directory '{NETWORK_DIR}' should NOT exist before starting "
        "the task, but it already does."
    )


def test_diagnostics_csv_absent():
    """
    The diagnostics.csv file must not exist before the student starts
    the task.  If the parent directory does not exist, this assertion
    trivially passes; otherwise we still explicitly check for the file.
    """
    assert not CSV_FILE.exists(), (
        f"The file '{CSV_FILE}' should NOT exist before starting "
        "the task, but it already does."
    )