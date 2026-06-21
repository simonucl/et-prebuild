# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
before the student performs any actions.

What we verify:
1. /home/user/data exists and is a directory.
2. /home/user/data/artifactory_ops.log exists, is a file, and contains exactly
   the 11 lines specified by the task description—byte-for-byte including the
   Unix LF line endings.

We explicitly do NOT test for the presence (or absence) of anything under
/home/user/reports because those are the artefacts the student must create.
"""

import os
from pathlib import Path
import pytest

DATA_DIR = Path("/home/user/data")
LOG_FILE = DATA_DIR / "artifactory_ops.log"

EXPECTED_LINES = [
    "2023-11-15T10:01:12Z repo-alpha /libs/commons-lang3-3.12.0.jar UPLOAD OK",
    "2023-11-15T10:02:48Z repo-beta /apps/myapp-1.3.1.war DOWNLOAD OK",
    "2023-11-15T10:03:10Z repo-alpha /libs/commons-io-2.11.0.jar UPLOAD FAIL",
    "2023-11-15T10:04:47Z repo-gamma /docker/core-image.tar DELETE OK",
    "2023-11-15T10:05:19Z repo-beta /apps/oldapp-0.9.8.war DELETE FAIL",
    "2023-11-15T10:06:03Z repo-alpha /libs/guava-31.1-jre.jar UPLOAD OK",
    "2023-11-15T10:07:55Z repo-beta /apps/newapp-1.4.0.war DOWNLOAD FAIL",
    "2023-11-15T10:09:12Z repo-gamma /docker/legacy-image.tar UPLOAD OK",
    "2023-11-15T10:10:27Z repo-alpha /libs/log4j-2.17.2.jar DELETE FAIL",
    "2023-11-15T10:11:41Z repo-delta /nuget/packageX.1.0.0.nupkg UPLOAD OK",
    "2023-11-15T10:13:03Z repo-beta /apps/myapp-1.3.2.war DOWNLOAD OK",
]

@pytest.fixture(scope="module")
def log_lines():
    """Return the list of lines (without trailing newlines) from the log file."""
    assert DATA_DIR.is_dir(), f"Required directory missing: {DATA_DIR}"
    assert LOG_FILE.is_file(), (
        f"Required log file missing: {LOG_FILE}\n"
        "The test harness expects this file to pre-exist with specific content."
    )
    # Read preserving line endings, then strip the trailing '\n' so comparison
    # is purely textual.
    with LOG_FILE.open("r", encoding="utf-8") as f:
        contents = f.read()
    # Splitlines(keepends=False) removes the trailing LF so we compare to EXPECTED_LINES.
    return contents.splitlines()

def test_log_file_line_count(log_lines):
    """The log file must contain exactly 11 lines."""
    assert len(log_lines) == 11, (
        f"Expected 11 lines in {LOG_FILE}, found {len(log_lines)}.\n"
        "Ensure the log file is untouched and has not been truncated or modified."
    )

def test_log_file_contents(log_lines):
    """Verify the log file contents match the expected baseline exactly."""
    # We compare lists for a strict, ordered, whole-file check.
    assert log_lines == EXPECTED_LINES, (
        f"The contents of {LOG_FILE} do not match the expected baseline.\n"
        "This file must remain unmodified before the student's solution runs."
    )