# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating system
# *before* the student performs any action.  It deliberately avoids
# checking for the presence (or absence) of any *output* artefacts
# such as /home/user/processed or files inside that directory.

import os
import pytest

RAW_PATH = "/home/user/datasets/raw_reviews.tsv"

# The exact, line-by-line contents that must already be present.
EXPECTED_LINES = [
    "#id\ttext\tlabel\textra\n",
    "1\tHello World\tPOSITIVE\tmeta1\n",
    "2\tThis is great\tPOSITIVE\tmeta2\n",
    "#3\tbad data\tNEGATIVE\n",
    "3\tAwful\tNEGATIVE\tmeta3\n",
    "4\tLovely Day\tPOSITIVE\tmeta4\n",
    "\n",
    "5\tterrible\tNEGATIVE\tmeta5\n",
]


def test_raw_file_exists_and_is_regular():
    """Verify that the raw TSV file exists and is a regular file."""
    assert os.path.exists(
        RAW_PATH
    ), f"Required file missing: {RAW_PATH}"
    assert os.path.isfile(
        RAW_PATH
    ), f"Expected {RAW_PATH} to be a regular file, but it's not."


def test_raw_file_contents_exact_match():
    """Verify that the raw TSV file contains the expected 8 lines, exactly."""
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    # Check number of lines first for a clearer error message.
    assert len(actual_lines) == len(
        EXPECTED_LINES
    ), (
        f"{RAW_PATH} should contain {len(EXPECTED_LINES)} lines, "
        f"but actually contains {len(actual_lines)}."
    )

    # Compare each line verbatim so that any mismatch is reported precisely.
    for idx, (exp, got) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert (
            got == exp
        ), (
            f"Line {idx} of {RAW_PATH} differs from expected.\n"
            f"Expected: {repr(exp)}\n"
            f"Got     : {repr(got)}"
        )