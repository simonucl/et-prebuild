# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating system
# before the student performs any actions for the “Localhost Vulnerability
# Scan” task.  At this point in time **no results file should yet exist**,
# because creating it is exactly what the student is asked to do.
#
# The checks below purposely assert the *absence* of the target file so that
# we can detect polluted environments (e.g. from a prior, failed or cached
# run).  If the file is already present, the tests will fail with clear
# guidance, ensuring the student starts from a clean slate.

import pathlib
import pytest

RESULTS_PATH = pathlib.Path("/home/user/scan_results/localhost_scan.txt")


def test_scan_results_file_does_not_exist():
    """
    The scan-results file must NOT exist before the student runs their
    solution.  Its presence would indicate that the environment is not in the
    expected pristine state.
    """
    assert not RESULTS_PATH.exists(), (
        f"Pre-flight check failed: the file {RESULTS_PATH} already exists.\n"
        "The initial environment must not contain this file; please remove it "
        "so the student can generate it as part of their solution."
    )