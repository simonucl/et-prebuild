# test_initial_state.py
#
# This pytest suite validates that the **starting** filesystem state is
# correct *before* the student performs any actions described in the
# assignment.  It checks that the golden source tree exists exactly as
# expected and that the destination / log directories do **not** yet
# exist.  If any assertion fails, the corresponding message should make
# it immediately clear what is wrong with the environment.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
SOURCE_ENV = HOME / "source_env"
QA_REMOTE_ENV = HOME / "qa_remote_env"
SYNC_LOGS = HOME / "sync_logs"

# Expected relative paths inside /home/user/source_env
EXPECTED_TREE = {
    Path("app.py"): 'print("Hello QA")',
    Path("README.md"): "Example project for rsync test",
    Path("requirements.txt"): "flask==2.0.2\npytest==7.4.0",
    Path("data/sample.json"): '{ "value": 42 }',
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    """Read a text file, return its content with trailing newlines stripped."""
    return path.read_text().strip()


# ---------------------------------------------------------------------------
# Tests that verify the INITIAL state
# ---------------------------------------------------------------------------

def test_source_env_directory_exists():
    assert SOURCE_ENV.is_dir(), (
        f"Expected directory {SOURCE_ENV} to exist but it is missing."
    )


@pytest.mark.parametrize("relative_path, expected_content", EXPECTED_TREE.items())
def test_expected_files_exist_with_correct_content(relative_path, expected_content):
    """
    Ensure each expected file exists inside source_env with the correct
    (stripped) content.  New-lines at end of files are tolerated.
    """
    abs_path = SOURCE_ENV / relative_path
    assert abs_path.is_file(), f"Expected file {abs_path} is missing."

    actual_content = read_file(abs_path)
    assert (
        actual_content == expected_content
    ), f"Content of {abs_path} is incorrect.\nExpected:\n{expected_content!r}\nFound:\n{actual_content!r}"


def test_no_unexpected_items_in_source_env():
    """
    The project tree should contain ONLY the files listed in EXPECTED_TREE.
    Extra files would indicate a dirty starting snapshot.
    """
    found_paths = {
        p.relative_to(SOURCE_ENV) for p in SOURCE_ENV.rglob("*") if p.is_file()
    }
    expected_paths = set(EXPECTED_TREE.keys())
    unexpected = found_paths - expected_paths
    missing = expected_paths - found_paths

    assert not missing, (
        f"The following expected file(s) are missing in {SOURCE_ENV}: "
        + ", ".join(sorted(str(p) for p in missing))
    )
    assert not unexpected, (
        f"The following unexpected file(s) exist in {SOURCE_ENV}: "
        + ", ".join(sorted(str(p) for p in unexpected))
    )


def test_destination_directory_does_not_exist_yet():
    """
    Before the student runs rsync, /home/user/qa_remote_env must *not* exist.
    """
    assert not QA_REMOTE_ENV.exists(), (
        f"The directory {QA_REMOTE_ENV} already exists, "
        "but it should be created by the student's solution."
    )


def test_sync_logs_directory_does_not_exist_yet():
    """
    The /home/user/sync_logs directory and its expected output files should
    not exist before the student runs the required commands.
    """
    assert not SYNC_LOGS.exists(), (
        f"The directory {SYNC_LOGS} already exists, "
        "but it should be created by the student's solution."
    )