# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating system
# BEFORE the student starts working on the assignment.
#
# It checks that the sample benchmark logs exist in
#     /home/user/samples
# and that each file contains the expected single-line content.
#
# NOTE:
#  • We intentionally do NOT test for any files or directories the student
#    is supposed to create (e.g. /home/user/profiling/reports), in order to
#    keep this suite focused solely on the pre-exercise filesystem state.
#  • All paths are absolute, in compliance with the spec.

import os
from pathlib import Path
import pytest

SAMPLES_DIR = Path("/home/user/samples")

EXPECTED_LOGS = {
    "webserver.log": "exec_time_ms=250\n",
    "cache.log": "exec_time_ms=75\n",
    "db.log": "exec_time_ms=184\n",
}


def _read_file(path: Path) -> str:
    """Helper that reads a small text file, returning its full contents."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_samples_directory_exists():
    assert SAMPLES_DIR.exists(), (
        f"Required directory {SAMPLES_DIR} is missing. "
        "It should already be present with the raw benchmark logs."
    )
    assert SAMPLES_DIR.is_dir(), f"{SAMPLES_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename,expected_content", EXPECTED_LOGS.items())
def test_each_sample_log_exists_with_correct_content(filename, expected_content):
    file_path = SAMPLES_DIR / filename
    assert file_path.exists(), (
        f"Expected log file {file_path} is missing. "
        "All three benchmark logs must be present before starting the task."
    )
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_content = _read_file(file_path)
    assert (
        actual_content == expected_content
    ), (
        f"Content mismatch in {file_path}.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )