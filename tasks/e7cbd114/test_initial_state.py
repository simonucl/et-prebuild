# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state
# before the student performs any actions for the migration task.
#
# It intentionally checks ONLY the legacy items that must already
# be present.  It does **not** test for any of the artefacts the
# student is expected to create later (e.g., /home/user/current_release,
# /home/user/migration_logs, or the symlinks/log file).
#
# If any of these tests fail, it means the starting environment is
# not as advertised and the exercise itself would be invalid.

import os
from pathlib import Path

# Base paths used throughout the assertions
SERVICES_DIR = Path("/home/user/services")
API_DIR = SERVICES_DIR / "api"
WEB_DIR = SERVICES_DIR / "web"


def _assert_dir_exists(path: Path):
    """
    Helper: assert that ``path`` exists and is a *real* directory
    (not a symlink).
    """
    assert path.exists(), f"Expected directory '{path}' is missing."
    assert path.is_dir(), f"'{path}' exists but is not a directory."
    assert not path.is_symlink(), f"'{path}' should be a real directory, not a symlink."


def _assert_file_contents(path: Path, expected: str):
    """
    Helper: assert that ``path`` exists, is a regular file,
    and its contents match ``expected`` exactly.
    """
    assert path.exists(), f"Expected file '{path}' is missing."
    assert path.is_file(), f"'{path}' exists but is not a regular file."
    with path.open("r", encoding="utf-8") as fh:
        content = fh.read()
    assert content == expected, (
        f"Contents of '{path}' do not match the expected text.\n"
        f"Expected:\n{expected!r}\nGot:\n{content!r}"
    )


def test_services_directory_structure():
    """
    Ensure the legacy services directory and its sub-directories exist
    as real directories (not symlinks).
    """
    _assert_dir_exists(SERVICES_DIR)
    _assert_dir_exists(API_DIR)
    _assert_dir_exists(WEB_DIR)


def test_api_readme_file():
    """
    Confirm the placeholder README in the API directory exists
    and contains the expected text.
    """
    readme_path = API_DIR / "README.txt"
    expected_text = "API service code lives here\n"
    _assert_file_contents(readme_path, expected_text)


def test_web_readme_file():
    """
    Confirm the placeholder README in the Web directory exists
    and contains the expected text.
    """
    readme_path = WEB_DIR / "README.txt"
    expected_text = "Web frontend code lives here\n"
    _assert_file_contents(readme_path, expected_text)