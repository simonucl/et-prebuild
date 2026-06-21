# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student performs any actions.  Only standard–library
# modules plus pytest are used.

import os
import stat

import pytest

BIN_DIR = "/home/user/build/bin"

# Mapping: basename -> (expected_size, expected_contents)
EXPECTED_BINARIES = {
    "tool_alpha": (
        26,
        b"alpha build artifact v1.0\n",
    ),
    "tool_beta": (
        25,
        b"beta build artifact v1.0\n",
    ),
    "tool_gamma": (
        26,
        b"gamma build artifact v1.0\n",
    ),
}


def _full_path(name: str) -> str:
    """Return the absolute path to an expected binary."""
    return os.path.join(BIN_DIR, name)


def test_bin_directory_exists_and_is_directory():
    """Verify that /home/user/build/bin exists and is a directory."""
    assert os.path.isdir(
        BIN_DIR
    ), f"Required directory {BIN_DIR} is missing or is not a directory."


@pytest.mark.parametrize("binary", sorted(EXPECTED_BINARIES))
def test_each_binary_exists_with_correct_permissions(binary):
    """Each expected binary must exist and have 0644 permissions."""
    path = _full_path(binary)

    assert os.path.isfile(
        path
    ), f"Expected binary {path} is missing or is not a regular file."

    # Check POSIX permissions are exactly 0644 (rw-r--r--)
    mode = stat.S_IMODE(os.stat(path).st_mode)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"Permissions for {path} are {oct(mode)}, expected {oct(expected_mode)}."


@pytest.mark.parametrize("binary", sorted(EXPECTED_BINARIES))
def test_binary_size_and_contents_are_unchanged(binary):
    """Validate size in bytes and exact contents of each binary."""
    expected_size, expected_contents = EXPECTED_BINARIES[binary]
    path = _full_path(binary)

    # --- Size check ---------------------------------------------------------
    file_size = os.path.getsize(path)
    assert (
        file_size == expected_size
    ), f"Size mismatch for {path}: found {file_size} bytes, expected {expected_size}."

    # --- Content check ------------------------------------------------------
    with open(path, "rb") as fh:
        data = fh.read()

    assert (
        data == expected_contents
    ), f"Contents of {path} do not match the expected fixed build artifact."


def test_no_extra_binaries_present():
    """
    Ensure no unexpected files are present in /home/user/build/bin.
    (Only the three known tools should exist.)
    """
    present_files = sorted(
        f
        for f in os.listdir(BIN_DIR)
        if os.path.isfile(os.path.join(BIN_DIR, f))
    )
    expected_files = sorted(EXPECTED_BINARIES.keys())

    assert (
        present_files == expected_files
    ), f"Unexpected files found in {BIN_DIR}. Expected: {expected_files}, found: {present_files}"