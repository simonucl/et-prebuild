# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the student’s remediation script runs.  If any of these tests fail,
# the grading environment itself is broken or the student has already
# (incorrectly) modified the files.

import os
import stat
import pytest

HOME = "/home/user"
CONFIG_DIR = os.path.join(HOME, "policy", "configs")
REPORTS_DIR = os.path.join(HOME, "policy", "reports")

APP1_PATH = os.path.join(CONFIG_DIR, "app1.ini")
APP2_PATH = os.path.join(CONFIG_DIR, "app2.ini")

APP1_EXPECTED = """[security]
enforce_tls=false

[logging]
level=DEBUG
"""

APP2_EXPECTED = """[security]
enforce_tls=true

[logging]
level=INFO
"""


def _read_file(path):
    """Return file content with UNIX newlines."""
    with open(path, encoding="utf-8") as fh:
        return fh.read().replace("\r\n", "\n")


def test_configs_directory_exists():
    assert os.path.isdir(CONFIG_DIR), (
        f"Expected directory {CONFIG_DIR!r} to exist."
    )

    mode = stat.S_IMODE(os.stat(CONFIG_DIR).st_mode)
    assert mode & stat.S_IWUSR, (
        f"Directory {CONFIG_DIR!r} must be writable by the user."
    )


def test_reports_directory_exists_and_empty():
    assert os.path.isdir(REPORTS_DIR), (
        f"Expected directory {REPORTS_DIR!r} to exist."
    )

    # Directory must be empty prior to remediation.
    children = os.listdir(REPORTS_DIR)
    assert children == [], (
        f"Expected {REPORTS_DIR} to be empty before remediation; "
        f"found: {children}"
    )


@pytest.mark.parametrize(
    "path,expected_content",
    [
        (APP1_PATH, APP1_EXPECTED),
        (APP2_PATH, APP2_EXPECTED),
    ],
)
def test_ini_files_exist_with_correct_content(path, expected_content):
    assert os.path.isfile(path), f"Missing required INI file: {path}"

    # Check file permissions (0644).
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == 0o644, (
        f"File {path} should have mode 0644; found {oct(mode)}"
    )

    content = _read_file(path)
    # We ignore a single trailing newline difference.
    assert content.rstrip("\n") == expected_content.rstrip("\n"), (
        f"Content mismatch in {path}. "
        "The file does not match the expected initial state."
    )


def test_exactly_two_ini_files_present():
    # There should be exactly the two expected INI files in CONFIG_DIR
    ini_files = sorted(
        f for f in os.listdir(CONFIG_DIR) if f.lower().endswith(".ini")
    )
    expected = sorted([os.path.basename(APP1_PATH), os.path.basename(APP2_PATH)])
    assert ini_files == expected, (
        f"Expected exactly these INI files {expected} in {CONFIG_DIR}, "
        f"but found {ini_files}"
    )


def test_no_backup_files_exist_yet():
    # No *.bak files should exist before remediation.
    bak_files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".bak")]
    assert (
        bak_files == []
    ), f"Backup files {bak_files} found in {CONFIG_DIR} before remediation."