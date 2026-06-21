# test_initial_state.py
#
# This test-suite verifies the operating-system state **before** the student
# executes any shell commands.  It purposefully checks only the resources that
# must already be present and *does not* look for any files or directories that
# will be created by the student later on.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
SAMPLE_DIR = HOME / "sample_data"

@pytest.mark.parametrize(
    "path, expected_content",
    [
        (SAMPLE_DIR / "file_alpha.txt", "alpha\n"),
        (SAMPLE_DIR / "file_beta.txt",  "beta\n"),
    ],
)
def test_sample_files_exist_with_correct_content(path: Path, expected_content: str):
    """
    Ensure that each required file exists, is a regular file, and contains the
    exact single line specified in the task description.
    """
    assert path.exists(), f"Required file missing: {path}"
    assert path.is_file(), f"Expected a regular file but found something else: {path}"

    # Read the file in text mode to validate its exact content (including newline).
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read()

    assert data == expected_content, (
        f"Content of {path} incorrect.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(data)}"
    )

def test_sample_directory_exists_and_is_directory():
    """
    Confirm that /home/user/sample_data exists and is a directory.
    """
    assert SAMPLE_DIR.exists(), f"Directory missing: {SAMPLE_DIR}"
    assert SAMPLE_DIR.is_dir(), f"Path exists but is not a directory: {SAMPLE_DIR}"