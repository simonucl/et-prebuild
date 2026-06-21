# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the filesystem
# before the student performs any action.  It checks only the prerequisites
# (input directory / file, their exact contents and encoding) and **does not**
# test for any output artefacts that the student is expected to create later.

import os
import stat
import pytest

INPUT_DIR = "/home/user/support/input"
INPUT_FILE = "/home/user/support/input/legacy_notes.txt"

# Byte-for-byte contents that must be present in the legacy file
EXPECTED_BYTES = bytes.fromhex(
    "43 61 66 E9 20 4D FC 6E 73 74 65 72 20 2D 20 "
    "72 E9 75 6E 69 6F 6E 20 E0 20 31 34 68 2E 0A"
)

EXPECTED_TEXT_ISO_8859_1 = "Café Münster - réunion à 14h.\n"


def test_input_directory_exists():
    assert os.path.isdir(INPUT_DIR), (
        f"Required directory {INPUT_DIR} is missing. "
        "The initial state must contain the input/ directory."
    )

    # Basic permission sanity: readable + executable (so it can be traversed)
    mode = os.stat(INPUT_DIR).st_mode
    assert mode & stat.S_IRUSR, f"{INPUT_DIR} should be readable by the owner."
    assert mode & stat.S_IXUSR, f"{INPUT_DIR} should be traversable by the owner."


def test_legacy_file_exists():
    assert os.path.isfile(INPUT_FILE), (
        f"Required file {INPUT_FILE} is missing. "
        "The task must start with the legacy ISO-8859-1 file in place."
    )

    mode = os.stat(INPUT_FILE).st_mode
    assert mode & stat.S_IRUSR, f"{INPUT_FILE} should be readable by the owner."
    assert mode & stat.S_IWUSR, f"{INPUT_FILE} should be writable by the owner."


def test_legacy_file_exact_content_and_encoding():
    """
    Verify three things:
    1. The file's bytes are EXACTLY as specified by the task.
    2. Those bytes decode correctly with ISO-8859-1 to the expected text.
    3. Attempting to decode as UTF-8 must raise UnicodeDecodeError,
       proving the file is indeed legacy single-byte encoded.
    """
    with open(INPUT_FILE, "rb") as fp:
        data = fp.read()

    # 1. Exact byte-for-byte match
    assert data == EXPECTED_BYTES, (
        "The contents of legacy_notes.txt do not match the expected "
        "byte sequence for the initial state."
    )

    # 2. ISO-8859-1 decoding gives the intended visible text
    decoded_iso = data.decode("iso-8859-1")
    assert decoded_iso == EXPECTED_TEXT_ISO_8859_1, (
        "When decoded with ISO-8859-1, the file must read exactly:\n"
        f"{EXPECTED_TEXT_ISO_8859_1!r}\n"
        "But it decoded to:\n"
        f"{decoded_iso!r}"
    )

    # 3. UTF-8 decoding must fail (there are invalid UTF-8 byte sequences)
    with pytest.raises(UnicodeDecodeError):
        _ = data.decode("utf-8")


def test_legacy_file_newline_and_no_bom():
    """
    Additional sanity:
       • No UTF-8 BOM at the start (0xEFBBBF).
       • File ends with a single Unix LF (0x0A).
       • Total length is exactly 30 bytes.
    """
    with open(INPUT_FILE, "rb") as fp:
        data = fp.read()

    # No BOM
    assert not data.startswith(b"\xEF\xBB\xBF"), (
        f"{INPUT_FILE} should not start with a UTF-8 BOM in the initial state."
    )

    # Ends with exactly one LF
    assert data.endswith(b"\x0A"), (
        f"{INPUT_FILE} must end with exactly one Unix LF (\\n, 0x0A)."
    )
    assert not data.endswith(b"\x0A\x0A"), (
        f"{INPUT_FILE} must not have multiple trailing newlines."
    )

    # Length
    assert len(data) == 30, (
        f"{INPUT_FILE} is expected to be exactly 30 bytes long in "
        "the initial state."
    )