# test_initial_state.py
#
# Pytest suite to verify that the operating-system / filesystem is in the
# expected *initial* state, i.e. **before** the student carries out the task.
#
# The checks performed are:
#   1. The input file /home/user/network_snapshot.txt exists, is a regular,
#      non-empty, readable file, and already contains at least one line that
#      flags a high-risk finding (either “(VULNERABLE)” or “Heartbleed”).
#   2. None of the artefacts the student is supposed to create are present yet:
#        • /home/user/pen_test/perf_optimized/
#        • /home/user/pen_test/perf_optimized/fast_extract.sh
#        • /home/user/pen_test/perf_optimized/fast_vulns.txt
#        • /home/user/pen_test/perf_optimized/operation.log
#
# All failures emit clear, prescriptive error messages so that any deviation
# from the expected pristine environment is obvious.

import os
import stat
import pytest

INPUT_FILE = "/home/user/network_snapshot.txt"
OUTPUT_DIR = "/home/user/pen_test/perf_optimized"
SCRIPT_PATH = os.path.join(OUTPUT_DIR, "fast_extract.sh")
VULNS_PATH = os.path.join(OUTPUT_DIR, "fast_vulns.txt")
LOG_PATH = os.path.join(OUTPUT_DIR, "operation.log")


def test_input_file_exists_and_readable():
    """Ensure the source network enumeration file exists and is readable."""
    assert os.path.exists(INPUT_FILE), (
        f"The required input file {INPUT_FILE} does not exist. "
        "It must be provided before the exercise begins."
    )
    assert os.path.isfile(INPUT_FILE), (
        f"{INPUT_FILE} exists but is not a regular file."
    )
    # Check readability
    assert os.access(INPUT_FILE, os.R_OK), (
        f"The current user cannot read {INPUT_FILE}. "
        "Please adjust permissions to make it world-readable."
    )


def test_input_file_non_empty_and_contains_risk_indicators():
    """Verify the input file is non-empty and actually includes high-risk markers."""
    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as fh:
        contents = fh.read()

    assert contents.strip(), (
        f"{INPUT_FILE} appears to be empty; it should contain network data."
    )

    has_vulnerable = "(VULNERABLE)" in contents
    has_heartbleed = "Heartbleed" in contents

    assert has_vulnerable or has_heartbleed, (
        f"{INPUT_FILE} does not contain any lines with '(VULNERABLE)' or "
        "'Heartbleed'. At least one such line must be present so the "
        "student can demonstrate filtering."
    )


@pytest.mark.parametrize(
    "path,what",
    [
        (OUTPUT_DIR, "output directory"),
        (SCRIPT_PATH, "extraction script"),
        (VULNS_PATH, "filtered vulnerabilities file"),
        (LOG_PATH, "operation log"),
    ],
)
def test_no_student_outputs_exist_yet(path, what):
    """
    Confirm that none of the artefacts the student is expected to create
    are present *before* the task is attempted.
    """
    assert not os.path.exists(path), (
        f"The {what} {path} already exists, but it should not be present "
        "prior to the student beginning the exercise. "
        "Please start from a clean environment."
    )