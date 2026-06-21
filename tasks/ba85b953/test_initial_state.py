# test_initial_state.py
#
# This pytest suite verifies the initial state of the filesystem *before*
# the student runs the required command.  It checks that the expected
# /home/user/scripts directory and its contents (three shell scripts) exist
# exactly as described in the task statement.  No tests are performed on the
# output file (/home/user/security_scan.log) because it must not exist yet.

import os
from pathlib import Path
import pytest

SCRIPTS_DIR = Path("/home/user/scripts")

EXPECTED_FILES = {
    "backup.sh": [
        "#!/bin/bash",
        "# Daily backup script",
        'password="letmein"',
        "tar -czf /tmp/backup.tgz /var/data",
    ],
    "deploy.sh": [
        "#!/bin/bash",
        "# Deployment helper",
        'export DB_password="P@ssw0rd!"',
        'echo "Deployment complete"',
    ],
    "clean.sh": [
        "#!/bin/bash",
        "# Cleanup utility",
        "# (no secrets here)",
    ],
}


def read_lines(path: Path):
    """
    Return the file's contents as a list of lines WITHOUT trailing newlines.
    This makes equality comparisons straightforward and insensitive to
    platform‐specific newline characters.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def test_scripts_directory_exists_and_is_directory():
    assert SCRIPTS_DIR.exists(), (
        f"Expected directory {SCRIPTS_DIR} to exist, "
        "but it does not."
    )
    assert SCRIPTS_DIR.is_dir(), (
        f"Expected {SCRIPTS_DIR} to be a directory, "
        "but it is not."
    )


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_expected_script_files_exist(filename):
    file_path = SCRIPTS_DIR / filename
    assert file_path.exists(), (
        f"Expected file {file_path} to exist, "
        "but it does not."
    )
    assert file_path.is_file(), (
        f"Expected {file_path} to be a regular file, "
        "but it is not."
    )


@pytest.mark.parametrize("filename, expected_lines", EXPECTED_FILES.items())
def test_script_contents(filename, expected_lines):
    """
    Verify that each script file's contents exactly match the lines specified
    in the initial state description.
    """
    file_path = SCRIPTS_DIR / filename
    actual_lines = read_lines(file_path)

    # Helpful error message shows a unified diff if the assertion fails.
    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected initial state.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(f"  {i+1}: {line}" for i, line in enumerate(expected_lines))
        + "\nActual ({len(actual_lines)} lines):\n"
        + "\n".join(f"  {i+1}: {line}" for i, line in enumerate(actual_lines))
    )