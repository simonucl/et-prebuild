# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the container
# before the student begins the task for installing `sqlparse`.
#
# What we check (and ONLY what we check):
# 1. Directory /home/user/prebuilt_wheels exists and is readable.
# 2. The directory contains exactly one wheel file named
#       sqlparse-0.4.4-py3-none-any.whl
#    and that file itself is readable.
#
# We purposefully do NOT look for any of the “output” artefacts
# (formatted_query.sql, sqlparse_install.log, user-site packages, etc.),
# as those must be created *after* the student completes the task.
#
# Only stdlib + pytest are used.

import os
import stat
import pytest

PREBUILT_DIR = "/home/user/prebuilt_wheels"
EXPECTED_WHEEL = "sqlparse-0.4.4-py3-none-any.whl"
EXPECTED_WHEEL_PATH = os.path.join(PREBUILT_DIR, EXPECTED_WHEEL)


def test_prebuilt_wheels_dir_exists_and_readable():
    """Ensure the prebuilt_wheels directory is present and readable."""
    assert os.path.isdir(PREBUILT_DIR), (
        f"Required directory {PREBUILT_DIR} is missing. "
        "The sqlparse wheel must be supplied here."
    )

    # Check for read & execute permissions on the directory
    mode = os.stat(PREBUILT_DIR).st_mode
    assert mode & stat.S_IRUSR, f"Directory {PREBUILT_DIR} is not readable."
    assert mode & stat.S_IXUSR, f"Directory {PREBUILT_DIR} is not accessible (no execute/search bit)."


def test_exact_wheel_file_present_and_readable():
    """Verify that exactly one correct wheel file is present and readable."""
    # Gather all *.whl files inside the directory
    try:
        wheel_files = [f for f in os.listdir(PREBUILT_DIR) if f.endswith(".whl")]
    except FileNotFoundError:
        pytest.fail(f"Directory {PREBUILT_DIR} does not exist.")

    assert wheel_files, (
        f"No .whl files found in {PREBUILT_DIR}. "
        "Expected sqlparse wheel 'sqlparse-0.4.4-py3-none-any.whl'."
    )

    # Must contain exactly the expected wheel and nothing else
    assert wheel_files == [EXPECTED_WHEEL], (
        f"Unexpected wheel files in {PREBUILT_DIR}: {wheel_files}. "
        f"Expecting only '{EXPECTED_WHEEL}'."
    )

    # Now ensure the wheel file itself exists and is readable
    assert os.path.isfile(EXPECTED_WHEEL_PATH), (
        f"Expected wheel file {EXPECTED_WHEEL_PATH} is missing."
    )
    assert os.access(EXPECTED_WHEEL_PATH, os.R_OK), (
        f"Expected wheel file {EXPECTED_WHEEL_PATH} is not readable."
    )