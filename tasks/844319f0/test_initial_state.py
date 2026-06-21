# test_initial_state.py
#
# This test-suite validates the *initial* state of the file-system
# before the learner runs any command.  It checks that the nightly-build
# manifest is present and has the exact, known contents that the task
# description relies on.

import os
import textwrap
import pytest

HOME_DIR = "/home/user"
BUILDS_DIR = os.path.join(HOME_DIR, "builds")
MANIFEST_PATH = os.path.join(BUILDS_DIR, "artifact_manifest.csv")

# The canonical contents of /home/user/builds/artifact_manifest.csv
EXPECTED_MANIFEST = textwrap.dedent(
    """\
    build_id,artifact_name,version,checksum
    101,core-lib,1.0.0,2873acb
    102,ui-assets,1.0.1,9fbc211
    103,service-bin,2.0.0,17ab899
    """
)


def test_builds_directory_exists():
    """/home/user/builds must be an existing directory."""
    assert os.path.isdir(
        BUILDS_DIR
    ), f"Expected directory {BUILDS_DIR!r} to exist, but it does not."


def test_manifest_file_exists():
    """The artifact manifest CSV must exist at the exact path."""
    assert os.path.isfile(
        MANIFEST_PATH
    ), f"Expected file {MANIFEST_PATH!r} to exist, but it does not."


def test_manifest_contents_are_exact():
    """
    The CSV must have the exact, known contents (including the
    trailing newline).  Any deviation indicates the starting state
    is wrong.
    """
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # Use == rather than startswith to catch extra/missing lines.
    assert (
        actual == EXPECTED_MANIFEST
    ), (
        f"Contents of {MANIFEST_PATH!r} do not match the expected template.\n\n"
        f"--- Expected ---\n{EXPECTED_MANIFEST!r}\n"
        f"--- Actual   ---\n{actual!r}\n"
    )


def test_manifest_has_exact_four_columns():
    """
    Sanity-check that every non-header row possesses exactly four
    comma-separated fields, in the prescribed order.
    """
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    header = lines[0]
    expected_header = "build_id,artifact_name,version,checksum"
    assert (
        header == expected_header
    ), f"Header row should be {expected_header!r}, found {header!r}"

    for idx, row in enumerate(lines[1:], start=2):  # 1-based line numbers
        columns = row.split(",")
        assert len(columns) == 4, (
            f"Line {idx} in {MANIFEST_PATH!r} does not contain exactly "
            f"4 comma-separated fields: {row!r}"
        )