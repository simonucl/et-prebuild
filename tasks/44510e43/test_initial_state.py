# test_initial_state.py
#
# This pytest suite verifies that the initial filesystem state is correct
# *before* the student starts working.  It checks only for the presence and
# exact contents of the pre-existing raw CSV files that the task statement
# guarantees.  It does NOT look for (or against) any of the output artefacts
# the student will eventually create.

import os
import textwrap
import pytest

RAW_DIR = "/home/user/datasets/raw"
A_PATH = os.path.join(RAW_DIR, "experiment_A.csv")
B_PATH = os.path.join(RAW_DIR, "experiment_B.csv")

EXPECTED_A_CONTENT = textwrap.dedent(
    """\
    ID,Value
    A1,10
    A2,15
    A3,N/A
    A4,20
    """
)

EXPECTED_B_CONTENT = textwrap.dedent(
    """\
    ID,Value
    B1,5
    B2,8
    B3,11
    B4,N/A
    B5,12
    """
)


def test_raw_directory_exists():
    assert os.path.isdir(RAW_DIR), (
        f"Expected directory {RAW_DIR!r} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize(
    "path, expected_contents",
    [
        (A_PATH, EXPECTED_A_CONTENT),
        (B_PATH, EXPECTED_B_CONTENT),
    ],
    ids=["experiment_A.csv", "experiment_B.csv"],
)
def test_csv_files_exist_with_correct_content(path, expected_contents):
    assert os.path.isfile(path), (
        f"Expected file {path!r} to exist, but it is missing."
    )

    with open(path, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # The expected strings above include a final newline; check full equality.
    assert actual == expected_contents, (
        f"Contents of {path!r} do not match the required initial state.\n"
        "Expected:\n"
        f"{expected_contents!r}\n"
        "Actual:\n"
        f"{actual!r}"
    )