# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating‐system /
# filesystem **before** the student creates the summary report.  It makes sure
# that the required raw data file is present and well-formed so that subsequent
# tasks can rely on it.
#
# NOTE:  These tests intentionally do *not* check for the presence of the output
# directory or the summary file, because those are exactly what the student is
# supposed to create.

import pathlib
import re
import os

RAW_FILE = pathlib.Path("/home/user/perf/raw/fps_samples.log")


def test_raw_file_exists_and_is_regular_file():
    """
    The raw FPS capture file must exist at the exact expected path and must be a
    regular file.
    """
    assert RAW_FILE.exists(), (
        f"Required raw capture file is missing: {RAW_FILE}.\n"
        "Create this file before proceeding with the task."
    )
    assert RAW_FILE.is_file(), (
        f"Expected {RAW_FILE} to be a regular file, but it is not."
    )


def test_raw_file_has_at_least_one_line():
    """
    The file must contain at least one line of data.
    """
    with RAW_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert len(lines) > 0, (
        f"{RAW_FILE} is empty. It must contain one integer per line representing FPS samples."
    )


def test_each_line_is_positive_integer_with_no_spaces():
    """
    Every line in the raw file must be a positive integer with *no* leading or
    trailing whitespace other than the terminating newline.
    """
    int_pattern = re.compile(r"^\d+\n?$")

    with RAW_FILE.open("r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, start=1):
            # Strip only the trailing newline for validation purposes
            stripped = line.rstrip("\n")

            # Check that the line matches strictly digits
            assert int_pattern.fullmatch(line), (
                f"Line {idx} of {RAW_FILE} is malformed: {repr(line)}. "
                "Each line must contain only digits (0-9) and end with a single LF."
            )

            # Check that the integer is positive (>0)
            value = int(stripped)
            assert value > 0, (
                f"Line {idx} of {RAW_FILE} must be a positive integer, got {value}."
            )


def test_file_ends_with_single_newline():
    """
    The raw file should end with exactly one Unix newline character (LF).  This
    prevents tools that rely on POSIX text files from misbehaving.
    """
    with RAW_FILE.open("rb") as fh:
        fh.seek(0, os.SEEK_END)
        if fh.tell() == 0:
            pytest.skip("File is empty; newline check meaningless.")
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)

    assert last_byte == b"\n", (
        f"{RAW_FILE} must end with a single LF newline character."
    )