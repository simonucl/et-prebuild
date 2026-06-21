# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student’s solution is executed.
#
# This file deliberately checks **only** the resources that must already
# exist when the exercise starts.  It does **not** look for any of the
# files or directories that the student will later create
# (/home/user/cred_rotation/**), in accordance with the grading rules.

import os
import stat
import textwrap
import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

CSV_PATH = "/home/user/resources/credentials_2024Q2.csv"

# Exactly eight LF-terminated lines: one header + seven data rows.
EXPECTED_CSV_CONTENT = textwrap.dedent("""\
    user_id,access_key,created,expires
    u101,AKIA111111,2024-01-15,2024-06-10
    u102,AKIA222222,2024-02-10,2024-04-30
    u103,AKIA333333,2024-01-20,2024-05-15
    u104,AKIA444444,2024-03-01,2024-04-20
    u105,AKIA555555,2024-02-18,2024-07-01
    u106,AKIA666666,2024-02-25,2024-04-18
    u107,AKIA777777,2024-01-30,2024-04-25
""").replace("\n", "\n")  # keep LF endings exactly as typed

EXPECTED_NUM_LINES = 8           # header + 7 data rows
EXPECTED_FILE_MODE = 0o644       # rw-r--r--

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path):
    """Return the raw bytes and decoded text (utf-8) of a file."""
    with open(path, "rb") as fp:
        data = fp.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise AssertionError(
            f"{path} is not valid UTF-8 as required; decode error: {exc}"
        ) from None
    return data, text

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_csv_file_exists_and_is_regular():
    assert os.path.exists(
        CSV_PATH
    ), f"Required CSV file not found: {CSV_PATH}"
    assert os.path.isfile(
        CSV_PATH
    ), f"{CSV_PATH} exists but is not a regular file (maybe a dir or symlink?)"


def test_csv_permissions_are_world_readable():
    st: os.stat_result = os.stat(CSV_PATH)
    mode = stat.S_IMODE(st.st_mode)
    assert (
        mode == EXPECTED_FILE_MODE
    ), (
        f"{CSV_PATH} must have permissions 0o{EXPECTED_FILE_MODE:03o}; "
        f"found 0o{mode:03o}"
    )


def test_csv_content_matches_exactly():
    _raw, text = read_file(CSV_PATH)

    # Ensure the file ends with a single LF and no extra blank lines.
    assert text.endswith(
        "\n"
    ), f"{CSV_PATH} must be LF-terminated (end with a single '\\n')."
    lines = text.splitlines()
    assert (
        len(lines) == EXPECTED_NUM_LINES
    ), (
        f"{CSV_PATH} should contain exactly {EXPECTED_NUM_LINES} lines "
        f"(header + 7 data rows); found {len(lines)}."
    )

    expected_lines = EXPECTED_CSV_CONTENT.splitlines()
    assert (
        lines == expected_lines
    ), (
        f"Content of {CSV_PATH} does not match the expected initial data.\n"
        "Differences:\n"
        + "\n".join(
            f"  Expected: {e!r}\n  Found:    {f!r}"
            for e, f in zip(expected_lines, lines)
            if e != f
        )
    )