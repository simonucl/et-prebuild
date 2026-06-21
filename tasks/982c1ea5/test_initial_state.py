# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state
# required by the “credential rotation” exercise is present
# **before** the student performs any action.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
REMOTE_SERVER_DIR = HOME / "remote_server"
REMOTE_ETC_DIR = REMOTE_SERVER_DIR / "etc"
REMOTE_CREDS_FILE = REMOTE_ETC_DIR / "credentials.txt"

NEW_CREDS_DIR = HOME / "new_creds"
NEW_CREDS_FILE = NEW_CREDS_DIR / "credentials.txt"


def _read_lines(path: pathlib.Path):
    """
    Read a text file and return a list of its lines *without* trailing
    newline characters.  Using splitlines() makes the comparison
    agnostic to the exact newline representation (`\n` vs `\r\n`) and
    to whether the final line is newline-terminated.
    """
    return path.read_text(encoding="utf-8").splitlines()


def test_required_directories_exist():
    """Ensure that the mandatory directory structure is present."""
    assert REMOTE_SERVER_DIR.is_dir(), (
        f"Missing directory: {REMOTE_SERVER_DIR}"
    )
    assert REMOTE_ETC_DIR.is_dir(), (
        f"Missing directory: {REMOTE_ETC_DIR}"
    )
    assert NEW_CREDS_DIR.is_dir(), (
        f"Missing directory: {NEW_CREDS_DIR}"
    )


@pytest.mark.parametrize(
    "file_path, expected_lines",
    [
        (
            REMOTE_CREDS_FILE,
            ["username: admin", "password: OldP@ssw0rd!"],
        ),
        (
            NEW_CREDS_FILE,
            ["username: admin", "password: N3wSecur3P@ss!"],
        ),
    ],
)
def test_required_files_exist_and_have_expected_content(file_path, expected_lines):
    """Verify that the mandatory credential files exist and contain the expected data."""
    assert file_path.is_file(), f"Required file not found: {file_path}"

    lines = _read_lines(file_path)
    assert (
        lines == expected_lines
    ), (
        f"Unexpected contents in {file_path}. "
        f"Expected lines: {expected_lines!r}; Found lines: {lines!r}"
    )