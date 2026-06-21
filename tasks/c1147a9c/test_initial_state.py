# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student carries out any actions.  It asserts that the
# pre-staged front-end project exists exactly as described and that
# its files have the expected byte sizes.
#
# IMPORTANT:  Do **not** add tests for any archive files or for
# /home/user/backups/, because those are *output* artefacts that
# are expected **after** the student completes the task.

from pathlib import Path
import os
import pytest

# Base directory that must already exist
WEB_PROJECT_ROOT = Path("/home/user/web_project")

@pytest.fixture(scope="module")
def project_root():
    assert WEB_PROJECT_ROOT.is_dir(), (
        f"Expected directory {WEB_PROJECT_ROOT} to exist, "
        "but it is missing or not a directory."
    )
    return WEB_PROJECT_ROOT


def test_expected_subdirectories_exist(project_root):
    """
    Ensure css/, js/ and images/ directories exist inside the project.
    """
    for subdir in ("css", "js", "images"):
        p = project_root / subdir
        assert p.is_dir(), f"Missing expected directory: {p}"


@pytest.mark.parametrize(
    "relative_path,expected_size",
    [
        ("index.html", 100),
        ("css/style.css", 41),
        ("js/app.js", 28),
        ("images/logo.png", 22),
    ],
)
def test_expected_files_exist_with_correct_size(project_root, relative_path, expected_size):
    """
    Verify that each required file exists and has the exact byte size
    specified in the task description.
    """
    file_path = project_root / relative_path
    # Confirm the file exists
    assert file_path.is_file(), f"Missing expected file: {file_path}"
    # Confirm byte size
    actual_size = os.stat(file_path).st_size
    assert actual_size == expected_size, (
        f"File {file_path} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )