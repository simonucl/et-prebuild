# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “cleaned-datasets backup” exercise.  These tests **must** pass *before*
# the student begins their work.  They deliberately avoid looking for any
# output/target files or directories (e.g. nothing under /home/user/archives/).

import os
from pathlib import Path

import pytest


DATA_DIR = Path("/home/user/datasets/cleaned").resolve()

# Mapping of expected file names to their exact, byte-for-byte contents
EXPECTED_FILES = {
    "iris_cleaned.csv": (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "5.1,3.5,1.4,0.2,setosa\n"
        "5.9,3.0,5.1,1.8,virginica\n"
    ),
    "titanic_cleaned.csv": (
        "survived,pclass,sex,age,fare\n"
        "1,1,female,38,71.2833\n"
        "0,3,male,34.5,7.8292\n"
    ),
    "mnist_cleaned.csv": (
        "pixel1,pixel2,pixel3,label\n"
        "0,0,0,7\n"
        "0,0,0,2\n"
    ),
}


@pytest.fixture(scope="module")
def data_dir():
    return DATA_DIR


def test_cleaned_directory_exists_and_is_readable(data_dir):
    assert data_dir.exists(), f"Required directory {data_dir} is missing."
    assert data_dir.is_dir(), f"{data_dir} exists but is not a directory."
    # Check readability by listing; raises if permission denied
    try:
        list(data_dir.iterdir())
    except PermissionError:
        pytest.fail(f"Directory {data_dir} is not readable by the current user.")


def test_directory_contains_exactly_three_expected_files(data_dir):
    present_files = sorted(p.name for p in data_dir.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    assert (
        present_files == expected_files
    ), (
        "Directory /home/user/datasets/cleaned/ must contain exactly the three CSV "
        "files specified in the task description.\n"
        f"Expected: {expected_files}\n"
        f"Found   : {present_files}"
    )


@pytest.mark.parametrize("filename,expected_contents", EXPECTED_FILES.items())
def test_each_file_exists_and_has_exact_contents(data_dir, filename, expected_contents):
    file_path = data_dir / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Read as text with universal newlines so we can compare exact string
    with file_path.open("r", newline="") as f:
        actual_contents = f.read()

    assert (
        actual_contents == expected_contents
    ), (
        f"Contents of {file_path} do not match the expected reference data.\n"
        "---- Expected (repr) ----\n"
        f"{repr(expected_contents)}\n"
        "---- Actual (repr) ----\n"
        f"{repr(actual_contents)}"
    )


def test_no_extra_subdirectories_in_cleaned_directory(data_dir):
    subdirs = [p for p in data_dir.iterdir() if p.is_dir()]
    assert (
        not subdirs
    ), (
        f"Directory {data_dir} should not contain subdirectories. "
        f"Found: {[d.name for d in subdirs]}"
    )