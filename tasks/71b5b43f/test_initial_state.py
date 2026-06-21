# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem before
# any conversion work is carried out by the student.  It purposefully
# avoids looking for the output artefacts that the assignment requires
# the student to create.

from pathlib import Path
import pytest

FORENSICS_DIR = Path("/home/user/forensics")
LATIN1_FILE = FORENSICS_DIR / "incident_note_latin1.txt"

# The text we expect after decoding the Latin-1 file.
EXPECTED_CONTENT = (
    "Incident Note - 2023-05-15\n"
    "Affected user: José Álvarez\n"
    "Issue: Crème brûlée recipe overwritten with mojibake\n"
    "Details: ½ cup sugar became ÃÂ½ cup sugar\n"
    "Resolution: Convert file encoding from ISO-8859-1 to UTF-8.\n"
)


def test_forensics_directory_exists():
    """The evidence directory must already exist."""
    assert FORENSICS_DIR.exists(), (
        f"Required directory {FORENSICS_DIR} is missing."
    )
    assert FORENSICS_DIR.is_dir(), (
        f"{FORENSICS_DIR} exists but is not a directory."
    )


def test_latin1_file_exists():
    """The original Latin-1 evidence file must be present."""
    assert LATIN1_FILE.exists(), (
        f"Required file {LATIN1_FILE} is missing."
    )
    assert LATIN1_FILE.is_file(), (
        f"{LATIN1_FILE} exists but is not a regular file."
    )


def test_latin1_file_content_and_encoding():
    """
    The evidence file must:
    1. Decode cleanly with ISO-8859-1 (Latin-1).
    2. Contain the exact expected text.
    3. Fail to decode with UTF-8, proving it has not already been converted.
    """
    raw_bytes = LATIN1_FILE.read_bytes()

    # 1 & 2: Decode with Latin-1 and compare to the canonical text.
    decoded_latin1 = raw_bytes.decode("latin-1")
    assert decoded_latin1 == EXPECTED_CONTENT, (
        f"{LATIN1_FILE} content does not match the expected Latin-1 text."
    )

    # 3: Ensure the file is not already UTF-8.
    with pytest.raises(UnicodeDecodeError):
        raw_bytes.decode("utf-8")