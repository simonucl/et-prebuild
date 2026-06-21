# test_initial_state.py
"""
PyTest suite that verifies the clean-slate state of the filesystem
*before* the student starts working on the “server_reports” exercise.

We make sure that none of the required artefacts already exist.  
If any of them are present the student would start from an incorrect
state and the assessment would be invalid.

Only the *directory* `/home/user/server_reports` is allowed to exist
(it may or may not be present), but the five specific files that the
grader will later look for must be absent.
"""

from pathlib import Path
import pytest

# Absolute paths that **must not** exist yet
FILES_THAT_MUST_BE_ABSENT = [
    Path("/home/user/server_reports/server-status-2024-05-14.json"),
    Path("/home/user/server_reports/server-status.schema.json"),
    Path("/home/user/server_reports/critical-servers-2024-05-14.json"),
    Path("/home/user/server_reports/summary-2024-05-14.txt"),
    Path("/home/user/server_reports/validation.log"),
]


def test_no_final_output_files_exist():
    """
    Ensure that none of the target artefact files are present before
    the student begins.  A pre-existing file would invalidate the task.
    """
    for path in FILES_THAT_MUST_BE_ABSENT:
        assert not path.exists(), (
            f"The file {path} already exists. "
            "The environment must start without any of the final artefacts."
        )


def test_server_reports_directory_state():
    """
    The parent directory may or may not exist at this point.  If it is
    already present it must be a directory (not a file).
    """
    dir_path = Path("/home/user/server_reports")
    if dir_path.exists():
        assert dir_path.is_dir(), (
            f"{dir_path} exists but is not a directory. "
            "Either remove it or make sure it is a directory before starting."
        )