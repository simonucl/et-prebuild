# test_initial_state.py
#
# This pytest file verifies the *initial* state of the operating-system
# environment before the student performs the conversion task.  It makes
# sure the profiling directory and the original UTF-16 file are present
# and contain the exact expected content.  It does *not* look for any
# result / output artefacts that the student is supposed to create
# later.

import os
import sys
import pathlib
import pytest

# ---------
# Constants
# ---------
HOME = pathlib.Path("/home/user")
PROFILING_DIR = HOME / "profiling"
UTF16_FILE = PROFILING_DIR / "output_utf16.txt"

# Expected textual content (decoded, i.e. Unicode string)
EXPECTED_TEXT = (
    "Profile Summary\n"
    "Function compute() took 12ms\n"
    "Function save_results() took 8ms\n"
)

@pytest.mark.describe("Initial filesystem state")
class TestInitialState:
    def test_profiling_directory_exists(self):
        """The /home/user/profiling directory must already exist."""
        assert PROFILING_DIR.is_dir(), (
            f"Required directory {PROFILING_DIR} is missing. "
            "The initial setup is incorrect."
        )

    def test_utf16_file_exists(self):
        """The UTF-16 summary file must already be present."""
        assert UTF16_FILE.is_file(), (
            f"Required file {UTF16_FILE} is missing. "
            "The student cannot proceed without it."
        )

    def test_utf16_file_starts_with_le_bom(self):
        """The file must start with the UTF-16 little-endian BOM 0xFF 0xFE."""
        with UTF16_FILE.open("rb") as fh:
            first_two = fh.read(2)
        assert first_two == b"\xFF\xFE", (
            f"{UTF16_FILE} does not start with the expected UTF-16 LE BOM "
            "(0xFF 0xFE).  Found bytes: {first_two!r}"
        )

    def test_utf16_file_decodes_correctly(self):
        """
        After decoding as UTF-16 (BOM aware), the textual content must match
        the reference string exactly.  We also verify that line endings are
        Unix LF.
        """
        with UTF16_FILE.open("rb") as fh:
            raw = fh.read()

        try:
            # Let Python detect endianness via BOM
            decoded = raw.decode("utf-16")
        except UnicodeDecodeError as exc:
            pytest.fail(
                f"File {UTF16_FILE} could not be decoded as UTF-16: {exc}"
            )

        # Ensure decoded string matches expected text exactly
        assert decoded == EXPECTED_TEXT, (
            "The decoded UTF-16 file contents do not match the expected "
            "profiling summary.\n"
            "Expected:\n"
            f"{EXPECTED_TEXT!r}\n"
            "Found:\n"
            f"{decoded!r}"
        )

    def test_no_crlf_line_endings_in_utf16_file(self):
        """
        Line endings inside the UTF-16 file must be Unix LF.
        CR characters (\\r) would decode as U+000D; ensure they are absent.
        """
        with UTF16_FILE.open("rb") as fh:
            raw = fh.read()

        decoded = raw.decode("utf-16")
        assert "\r" not in decoded, (
            f"{UTF16_FILE} contains CR characters. "
            "Only LF line endings are allowed."
        )