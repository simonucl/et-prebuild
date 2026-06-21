# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# *before* the student carries out the ticket “#2023-441 – Checksum verification for deployment binary”.
#
# Expected initial conditions (ground-truth):
#   • Directory /home/user/it_assets       – permissions 755
#   • File      /home/user/it_assets/installer_v3.2.bin
#       ‣ permissions 644
#       ‣ size 3 bytes
#       ‣ exact contents b'abc' (ASCII, no newline)
#   • File      /home/user/it_assets/installer_v3.2.bin.sha256  MUST **NOT** exist yet
#
# The tests below enforce these facts so that any deviation is reported with
# clear, actionable failure messages.

import os
import stat
import pytest

DIR_PATH = "/home/user/it_assets"
BIN_PATH = "/home/user/it_assets/installer_v3.2.bin"
SHA_PATH = "/home/user/it_assets/installer_v3.2.bin.sha256"

# ---------------------------------------------------------------------------


def _mode(path: str) -> int:
    """
    Return the filesystem permission bits for *path* (lowest octal 3 digits).
    E.g. 0o755, 0o644, etc.
    """
    return os.stat(path).st_mode & 0o777


# ---------------------------------------------------------------------------
# Directory checks
# ---------------------------------------------------------------------------

def test_it_assets_directory_exists():
    assert os.path.exists(DIR_PATH), (
        f"Required directory {DIR_PATH!r} is missing."
    )
    assert os.path.isdir(DIR_PATH), (
        f"{DIR_PATH!r} exists but is not a directory."
    )


def test_it_assets_directory_permissions():
    expected_mode = 0o755
    actual_mode = _mode(DIR_PATH)
    assert actual_mode == expected_mode, (
        f"Directory {DIR_PATH!r} should have permissions "
        f"{oct(expected_mode)}, found {oct(actual_mode)}."
    )


# ---------------------------------------------------------------------------
# Binary file checks
# ---------------------------------------------------------------------------

def test_installer_binary_exists():
    assert os.path.exists(BIN_PATH), (
        f"Required binary file {BIN_PATH!r} is missing."
    )
    assert os.path.isfile(BIN_PATH), (
        f"{BIN_PATH!r} exists but is not a regular file."
    )


def test_installer_binary_permissions():
    expected_mode = 0o644
    actual_mode = _mode(BIN_PATH)
    assert actual_mode == expected_mode, (
        f"Binary {BIN_PATH!r} should have permissions "
        f"{oct(expected_mode)}, found {oct(actual_mode)}."
    )


def test_installer_binary_size_and_contents():
    expected_contents = b"abc"  # exactly 3 bytes, no newline
    with open(BIN_PATH, "rb") as f:
        data = f.read()

    assert len(data) == len(expected_contents), (
        f"{BIN_PATH!r} should be {len(expected_contents)} bytes, "
        f"found {len(data)} bytes."
    )
    assert data == expected_contents, (
        f"{BIN_PATH!r} does not contain the expected data "
        f"(expected {expected_contents!r}, found {data!r})."
    )


# ---------------------------------------------------------------------------
# Checksum file *must not* be present yet
# ---------------------------------------------------------------------------

def test_checksum_file_absent_initially():
    assert not os.path.exists(SHA_PATH), (
        f"Checksum file {SHA_PATH!r} already exists, but it should be created "
        f"by the student as part of the task. Remove it and start over."
    )