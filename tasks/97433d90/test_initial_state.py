# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state **before**
# the student starts solving the exercise.  It must pass unchanged on
# the grading server.  Any failure pin-points a deviation from the
# required starting conditions.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
SUPPORT_DIR = HOME / "support"
INCOMING_DIR = SUPPORT_DIR / "incoming"
RESOLVED_DIR = SUPPORT_DIR / "resolved"
LOG_FILE = SUPPORT_DIR / "encoding_report.log"

# Filenames that must be present in /incoming/
EXPECTED_TXT_FILES = [
    "clients_es.txt",
    "résumé_fr.txt",
    "daten_de.txt",
]


def _read_bytes(path: pathlib.Path) -> bytes:
    """Return raw bytes from *path*; raise if file is missing."""
    if not path.is_file():
        pytest.fail(f"Required file missing: {path}")
    return path.read_bytes()


def test_incoming_directory_exists():
    assert INCOMING_DIR.is_dir(), (
        f"Directory {INCOMING_DIR} must exist before the task starts."
    )


def test_expected_files_exist_and_are_regular():
    missing = [name for name in EXPECTED_TXT_FILES
               if not (INCOMING_DIR / name).is_file()]
    assert not missing, (
        "The following required file(s) are missing in "
        f"{INCOMING_DIR}: {', '.join(missing)}"
    )

    # Ensure no unexpected *.txt files are present
    present_txt = {p.name for p in INCOMING_DIR.glob("*.txt")}
    unexpected = present_txt - set(EXPECTED_TXT_FILES)
    assert not unexpected, (
        f"Unexpected *.txt file(s) found in {INCOMING_DIR}: "
        f"{', '.join(sorted(unexpected))}"
    )


@pytest.mark.parametrize("file_name", EXPECTED_TXT_FILES)
def test_files_are_latin1_and_not_utf8(file_name):
    """
    Each supplied file must be encoded in ISO-8859-1 (Latin-1) and
    *not* already valid UTF-8.
    """
    path = INCOMING_DIR / file_name
    raw = _read_bytes(path)

    # 1) Must decode losslessly with Latin-1
    try:
        text_latin1 = raw.decode("latin-1")
    except UnicodeDecodeError as e:
        pytest.fail(
            f"{path} is expected to be ISO-8859-1 but failed to decode: {e}"
        )

    # 2) Ensure text_latin1 contains at least one non-ASCII character;
    #    otherwise the test below would be inconclusive.
    assert any(ord(ch) > 0x7F for ch in text_latin1), (
        f"{path} should contain non-ASCII bytes when decoded as Latin-1."
    )

    # 3) Must *not* be decodable as UTF-8 (presence of 0xE9 etc.)
    with pytest.raises(UnicodeDecodeError):
        raw.decode("utf-8")


def test_resolved_directory_absent_initially():
    assert not RESOLVED_DIR.exists(), (
        f"{RESOLVED_DIR} should NOT exist before the student runs the solution."
    )


def test_log_file_absent_initially():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the student runs the solution."
    )