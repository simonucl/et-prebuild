# test_initial_state.py
#
# This pytest suite verifies the initial state of the container **before**
# the student performs any actions.  It checks that the raw snapshot file
# required for the assignment is present *and* that its contents exactly
# match what the automated grader expects.
#
# IMPORTANT:  Per the meta-rules, we intentionally do NOT test for the
# presence (or absence) of any output directories/files such as
# /home/user/reports/*.  Only the pre-existing input data is validated.

import os
import textwrap
import pytest

SNAPSHOT_PATH = "/home/user/data/sys_snapshot.log"

# The snapshot file must contain these exact bytes (final '\n' included).
EXPECTED_SNAPSHOT_CONTENT = textwrap.dedent(
    """\
    PROC,102,0.3,1.2,bash
    PROC,205,25.6,10.1,python3
    PROC,309,50.8,5.0,java
    PROC,410,12.3,2.1,node
    MEM,TotalMemMB,7984
    MEM,FreeMemMB,1024
    CPU,CoreCount,4
    CPU,LoadAvg1min,3.12
    DISK,/dev/sda1,UsedPct,65
    """
)


def test_data_directory_exists():
    """Ensure /home/user/data exists and is a directory."""
    data_dir = os.path.dirname(SNAPSHOT_PATH)
    assert os.path.exists(
        data_dir
    ), f"Required directory {data_dir!r} is missing."
    assert os.path.isdir(
        data_dir
    ), f"Expected {data_dir!r} to be a directory, but it is not."


def test_snapshot_file_content_is_exact():
    """
    Verify that the snapshot file not only exists but also matches the
    byte-for-byte reference content expected by the grader.
    """
    assert os.path.exists(
        SNAPSHOT_PATH
    ), f"Snapshot file {SNAPSHOT_PATH!r} is missing."
    assert os.path.isfile(
        SNAPSHOT_PATH
    ), f"Path {SNAPSHOT_PATH!r} exists but is not a regular file."

    with open(SNAPSHOT_PATH, "r", encoding="utf-8", newline="") as fh:
        actual = fh.read()

    # Helpful diff message on failure
    assert (
        actual == EXPECTED_SNAPSHOT_CONTENT
    ), (
        "Snapshot file contents do not match the expected reference.\n"
        "----- Expected -----\n"
        f"{EXPECTED_SNAPSHOT_CONTENT!r}\n"
        "------ Actual ------\n"
        f"{actual!r}\n"
        "--------------------"
    )