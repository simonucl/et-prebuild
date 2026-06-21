# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# *before* the student performs any actions.  It checks only the
# initial prerequisites (input files / directories) and deliberately
# ignores anything that will be created later (backups, converted
# files, logs, etc.).

import pathlib
import pytest

# ----------------------------------------------------------------------
# Constants describing the required starting state
# ----------------------------------------------------------------------

CONF_DIR = pathlib.Path("/home/user/conf")
CONF_FILE = CONF_DIR / "settings.conf"

# The exact original UTF-8 bytes that must be present in settings.conf.
EXPECTED_BYTES = (
    b"nombre=Jos\xc3\xa9\n"
    b"ciudad=M\xc3\xa1laga\n"
    b"clave=pa\xc3\x9fw\xc3\xb6rd\n"
)

# The textual form of the UTF-8 content for additional verification.
EXPECTED_TEXT = "nombre=José\nciudad=Málaga\nclave=paßwörd\n"

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_conf_directory_exists():
    """
    /home/user/conf must exist and be a directory.
    """
    assert CONF_DIR.exists(), f"Required directory {CONF_DIR} is missing."
    assert CONF_DIR.is_dir(), f"{CONF_DIR} exists but is not a directory."


def test_settings_conf_file_exists_and_is_correct():
    """
    /home/user/conf/settings.conf must exist, be a regular file,
    contain the exact expected UTF-8 bytes, and decode cleanly to the
    expected Unicode string.
    """
    assert CONF_FILE.exists(), f"Required file {CONF_FILE} is missing."
    assert CONF_FILE.is_file(), f"{CONF_FILE} exists but is not a regular file."

    data = CONF_FILE.read_bytes()

    # Byte-for-byte comparison.
    assert data == EXPECTED_BYTES, (
        f"{CONF_FILE} contents do not match the expected initial UTF-8 bytes."
    )

    # Validate that the file is valid UTF-8 and matches the expected text.
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{CONF_FILE} is not valid UTF-8: {exc}")

    assert text == EXPECTED_TEXT, (
        f"{CONF_FILE} decoded text does not match expected lines.\n"
        f"Expected:\n{EXPECTED_TEXT!r}\nGot:\n{text!r}"
    )


def test_settings_conf_file_size():
    """
    The file size must be exactly 44 bytes.
    """
    size = CONF_FILE.stat().st_size
    expected_size = len(EXPECTED_BYTES)
    assert size == expected_size, (
        f"{CONF_FILE} size is {size} bytes; expected {expected_size} bytes."
    )