# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# conditions for the “Grafana dashboard batch-operations” exercise.
#
# These tests assert the following pre-conditions (before the student runs
# any commands):
#
# 1. The source directory /home/user/dashboards/ exists and is a directory.
# 2. Exactly three JSON files are present there:
#       - app_error.json
#       - latency_overview.json
#       - system_health.json
#    No other files (of any type) are allowed inside that directory tree.
# 3. Each JSON file contains the single, trailing-newline-terminated line
#    specified in the task description.
# 4. The target directory /home/user/archive/ must *not* exist yet.
#
# If any assertion fails, the error message explains precisely what is wrong,
# guiding the student to fix their environment before running their solution.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user").expanduser()
DASH_DIR = HOME / "dashboards"
ARCHIVE_DIR = HOME / "archive"

# Expected files and their exact one-line contents (including trailing '\n').
EXPECTED_FILES = {
    "app_error.json": '{"dashboard":"app_error"}\n',
    "latency_overview.json": '{"dashboard":"latency_overview"}\n',
    "system_health.json": '{"dashboard":"system_health"}\n',
}

###############################################################################
# Helper utilities
###############################################################################

def iter_all_files(root: Path):
    """
    Yield every file (not directory) under *root*, recursively.
    """
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            yield Path(dirpath) / name


###############################################################################
# Tests
###############################################################################

def test_dashboards_directory_exists_and_is_dir():
    assert DASH_DIR.exists(), f"Required directory {DASH_DIR} is missing."
    assert DASH_DIR.is_dir(), f"{DASH_DIR} exists but is not a directory."


def test_no_archive_directory_yet():
    assert not ARCHIVE_DIR.exists(), (
        f"{ARCHIVE_DIR} should NOT exist before the student runs their solution."
    )


@pytest.mark.parametrize("fname", list(EXPECTED_FILES))
def test_expected_json_files_exist_with_correct_content(fname):
    fpath = DASH_DIR / fname
    assert fpath.exists(), f"Expected file {fpath} is missing."
    assert fpath.is_file(), f"{fpath} exists but is not a regular file."

    with fpath.open("r", encoding="utf-8") as fp:
        content = fp.read()
    expected = EXPECTED_FILES[fname]
    assert content == expected, (
        f"Contents of {fpath} do not match expected.\n"
        f"Expected exactly:\n{expected!r}\nGot:\n{content!r}"
    )


def test_no_extra_files_in_dashboards_tree():
    all_files = list(iter_all_files(DASH_DIR))
    expected_full_paths = {DASH_DIR / name for name in EXPECTED_FILES}

    extra_files = [str(p) for p in all_files if p not in expected_full_paths]
    missing_files = [str(p) for p in expected_full_paths if p not in all_files]

    assert not missing_files, (
        "The following expected JSON files are missing:\n" + "\n".join(missing_files)
    )
    assert not extra_files, (
        "Only the three specified JSON files should exist under "
        f"{DASH_DIR}, but extra files were found:\n" + "\n".join(extra_files)
    )