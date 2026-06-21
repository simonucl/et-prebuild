# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem/encoding state
# before the student performs any actions for the “encoding-conversion”
# exercise.
#
# Only the standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
HOME_DIR = Path("/home/user")
RAW_DIR = HOME_DIR / "data" / "raw"
RAW_FILE = RAW_DIR / "customers_win1252.csv"

# Expected decoded text (four lines, LF endings)
EXPECTED_LINES = [
    "id,name,city",
    "1,José,Montréal",
    "2,Léa,Berlin",
    "3,O'Connor,Dublin",
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def get_mode_bits(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) of a filesystem object."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_raw_directory_exists_and_permissions():
    assert RAW_DIR.exists(), (
        f"Required directory {RAW_DIR} is missing. "
        "Create it with permissions 755."
    )
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = get_mode_bits(RAW_DIR)
    assert actual_mode == expected_mode, (
        f"{RAW_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."
    )


def test_raw_file_exists_and_permissions():
    assert RAW_FILE.exists(), (
        f"Required source file {RAW_FILE} is missing."
    )
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."
    expected_mode = 0o644
    actual_mode = get_mode_bits(RAW_FILE)
    assert actual_mode == expected_mode, (
        f"{RAW_FILE} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."
    )


def test_raw_file_line_endings_are_lf_only():
    data = RAW_FILE.read_bytes()
    assert b"\r" not in data, (
        f"{RAW_FILE} contains CR (\\r) characters; line endings must be LF only."
    )


def test_raw_file_is_windows1252_and_decodes_to_expected_text():
    # 1. Confirm it cannot be decoded as UTF-8 (should raise)
    data = RAW_FILE.read_bytes()
    with pytest.raises(UnicodeDecodeError):
        data.decode("utf-8")

    # 2. Decode with Windows-1252 and compare textual content
    text_cp1252 = data.decode("cp1252")
    lines = text_cp1252.split("\n")
    # If the final newline is missing, split() will give 4 items; if present, the
    # last item will be "".  Strip any empty tail to be tolerant.
    if lines and lines[-1] == "":
        lines = lines[:-1]

    assert lines == EXPECTED_LINES, (
        "Decoded CSV content does not match the expected four lines.\n"
        f"Expected lines:\n{EXPECTED_LINES}\n\nActual lines:\n{lines}"
    )


def test_specific_byte_sequences_for_non_ascii_characters():
    """
    Verify that certain non-ASCII strings are encoded with the expected bytes in
    Windows-1252.  This guards against accidental re-encoding.
    """
    data = RAW_FILE.read_bytes()

    # Windows-1252 encodings:
    #   'José'      -> 4A 6F 73 E9
    #   'Montréal'  -> 4D 6F 6E 74 72 E9 61 6C
    jose_bytes = b"Jos\xe9"
    montreal_bytes = b"Montr\xe9al"

    assert jose_bytes in data, (
        "'José' is not encoded with bytes 4A 6F 73 E9 in the source file."
    )
    assert montreal_bytes in data, (
        "'Montréal' is not encoded with bytes 4D 6F 6E 74 72 E9 61 6C in the source file."
    )