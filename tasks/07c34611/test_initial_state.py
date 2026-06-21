# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student runs any commands for the “automation-workflow” task.
#
# The checks make sure that:
#   • /home/user/workflows/input exists and contains exactly the three
#     stated JSON files (and nothing else).
#   • Each JSON file has the exact expected byte contents.
#   • No output artefacts (archive, restore directory, log file) are
#     present yet.

import os
from pathlib import Path

import pytest

WORKFLOWS_DIR = Path("/home/user/workflows")
INPUT_DIR = WORKFLOWS_DIR / "input"

EXPECTED_FILES = {
    "config1.json": b'{"name": "serviceA", "enabled": true}\n',
    "config2.json": b'{"name": "serviceB", "enabled": false}\n',
    "config3.json": b'{"name": "serviceC", "enabled": true}\n',
}

ARCHIVE_PATH = WORKFLOWS_DIR / "input_backup.tgz"
RESTORE_DIR = WORKFLOWS_DIR / "restore"
LOG_PATH = WORKFLOWS_DIR / "backup_report.log"


@pytest.fixture(scope="module")
def input_dir_contents():
    """Return a dict {relative_name: bytes} of files found in the input dir."""
    if not INPUT_DIR.exists():
        pytest.skip(f"{INPUT_DIR} is missing on this system; cannot run tests.")
    return {
        p.name: p.read_bytes()
        for p in INPUT_DIR.iterdir()
        if p.is_file()
    }


def test_input_directory_exists():
    assert INPUT_DIR.exists(), f"Required directory {INPUT_DIR} does not exist."
    assert INPUT_DIR.is_dir(), f"{INPUT_DIR} exists but is not a directory."


def test_input_contains_exact_three_json_files(input_dir_contents):
    found_names = set(input_dir_contents)
    expected_names = set(EXPECTED_FILES)
    missing = expected_names - found_names
    extra = found_names - expected_names
    assert not missing, (
        f"The following required files are missing from {INPUT_DIR}: "
        f"{', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected extra files present in {INPUT_DIR}: "
        f"{', '.join(sorted(extra))}"
    )
    # Ensure there are exactly three files (no sub-dirs counted)
    assert len(found_names) == 3, (
        f"{INPUT_DIR} should contain exactly 3 files, found {len(found_names)}."
    )


@pytest.mark.parametrize("filename,expected_bytes", EXPECTED_FILES.items())
def test_input_json_contents(filename, expected_bytes, input_dir_contents):
    assert filename in input_dir_contents, (
        f"{filename} is missing in {INPUT_DIR}."
    )
    actual = input_dir_contents[filename]
    assert actual == expected_bytes, (
        f"Contents of {filename} do not match expected bytes.\n"
        f"Expected: {expected_bytes!r}\nActual:   {actual!r}"
    )


def test_no_other_items_under_workflows():
    """There should be no sibling directories/files other than 'input'."""
    allowed = {"input"}
    extras = [
        p.name
        for p in WORKFLOWS_DIR.iterdir()
        if p.name not in allowed
    ]
    assert not extras, (
        f"Unexpected items exist in {WORKFLOWS_DIR}: {', '.join(sorted(extras))}"
    )


def test_output_artifacts_absent():
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} should not exist before the task is run."
    )
    assert not RESTORE_DIR.exists(), (
        f"Restore directory {RESTORE_DIR} should not exist before the task is run."
    )
    assert not LOG_PATH.exists(), (
        f"Log file {LOG_PATH} should not exist before the task is run."
    )