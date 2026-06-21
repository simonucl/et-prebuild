# test_initial_state.py
#
# This test-suite validates the repository state **before** the student starts
# working.  It intentionally does *not* look for any output artifacts that the
# assignment will eventually create.
#
# Checked prerequisites:
#   1. /home/user/mobile_pipelines  directory exists.
#   2. /home/user/mobile_pipelines/build_targets.txt file exists.
#   3. build_targets.txt contains exactly six lines, each matching the required
#      pattern and in the precise order specified in the task description.
#
# Any failure message should make it immediately clear what prerequisite is
# missing or malformed.

import pathlib
import re
import pytest

BASE_DIR = pathlib.Path("/home/user/mobile_pipelines")
TARGETS_FILE = BASE_DIR / "build_targets.txt"

EXPECTED_LINES = [
    "android-29",
    "android-30",
    "ios-13",
    "ios-14",
    "android-31",
    "ios-15",
]

LINE_PATTERN = re.compile(r"^(android|ios)-\d+$")


def test_mobile_pipelines_dir_exists():
    assert BASE_DIR.exists(), (
        f"Expected directory {BASE_DIR} to exist but it does not. "
        "Create it or adjust the path."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory. "
        "It must be a directory containing the pipeline resources."
    )


def test_build_targets_file_exists():
    assert TARGETS_FILE.exists(), (
        "Expected initial input file "
        f"{TARGETS_FILE} to exist but it does not."
    )
    assert TARGETS_FILE.is_file(), (
        f"{TARGETS_FILE} exists but is not a regular file."
    )


def test_build_targets_file_contents():
    raw_lines = TARGETS_FILE.read_text(encoding="utf-8").splitlines()
    # Fail fast if the wrong number of lines is present.
    assert len(raw_lines) == 6, (
        f"Expected build_targets.txt to contain exactly 6 lines but found "
        f"{len(raw_lines)}.\nActual lines:\n{raw_lines}"
    )

    # Validate each line pattern and collective uniqueness.
    for idx, line in enumerate(raw_lines, start=1):
        assert LINE_PATTERN.fullmatch(line), (
            f"Line {idx} in build_targets.txt is malformed: {line!r}. "
            "Each line must match 'android-<API_LEVEL>' "
            "or 'ios-<MAJOR_VERSION>' where the version is numeric."
        )

    # Ensure there are no duplicate entries.
    assert len(raw_lines) == len(set(raw_lines)), (
        "Duplicate entries detected in build_targets.txt: "
        f"{raw_lines}"
    )

    # Verify the order and exact content matches the specification.
    assert raw_lines == EXPECTED_LINES, (
        "The content of build_targets.txt does not match the expected list.\n"
        f"Expected (in order): {EXPECTED_LINES}\n"
        f"Found:               {raw_lines}"
    )