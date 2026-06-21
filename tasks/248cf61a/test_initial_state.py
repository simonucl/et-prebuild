# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem for the
# “messages_de.properties” re-encoding exercise.  These tests must pass
# *before* the student starts working; therefore we explicitly check that the
# products of the assignment (UTF-8 copy and populated log) are NOT yet
# present, while the legacy ISO-8859-1 source file *is* present and correct.
#
# Only Python’s standard library plus pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project")
TRANSLATIONS_DIR = os.path.join(PROJECT_DIR, "translations")
SOURCE_FILE = os.path.join(TRANSLATIONS_DIR, "messages_de.properties")
TARGET_FILE = os.path.join(TRANSLATIONS_DIR, "messages_de_utf8.properties")
CONVERSION_LOG = os.path.join(PROJECT_DIR, "conversion.log")


def _read_binary(path):
    with open(path, "rb") as fh:
        return fh.read()


def test_translations_directory_exists_and_permissions():
    assert os.path.isdir(
        TRANSLATIONS_DIR
    ), f"Required directory {TRANSLATIONS_DIR!r} is missing."
    mode = stat.S_IMODE(os.stat(TRANSLATIONS_DIR).st_mode)
    assert (
        mode == 0o755
    ), f"Directory {TRANSLATIONS_DIR!r} must have permissions 0755, found {oct(mode)}."


def test_source_file_exists_and_permissions():
    assert os.path.isfile(
        SOURCE_FILE
    ), f"Source file {SOURCE_FILE!r} is missing."
    mode = stat.S_IMODE(os.stat(SOURCE_FILE).st_mode)
    assert (
        mode == 0o644
    ), f"Source file {SOURCE_FILE!r} must have permissions 0644, found {oct(mode)}."


def test_source_file_content_and_encoding():
    raw = _read_binary(SOURCE_FILE)

    # 1) File must not be empty
    assert raw, f"Source file {SOURCE_FILE!r} is unexpectedly empty."

    # 2) Must end with a single LF
    assert raw.endswith(
        b"\n"
    ), f"Source file {SOURCE_FILE!r} must end with a newline (LF)."

    # 3) There must be exactly three data lines
    lines = raw.split(b"\n")
    # The last split element will be b'' because the file ends with \n
    assert (
        len(lines) == 4
    ), f"Expected exactly three lines plus trailing LF in {SOURCE_FILE!r}, got {len(lines)-1} lines."

    expected_lines_latin1 = [
        "greeting=Grüß Gott",
        "farewell=Auf Wiedersehen",
        "thanks=Vielen Dank",
    ]
    decoded = raw.decode("latin-1").split("\n")[:-1]  # drop empty element
    assert (
        decoded == expected_lines_latin1
    ), f"Content of {SOURCE_FILE!r} does not match expected key-value pairs."

    # 4) The bytes for 'ü' (0xFC) and 'ß' (0xDF) must appear (ISO-8859-1)
    assert b"\xFC" in raw, "Byte 0xFC ('ü' in ISO-8859-1) not found in source file."
    assert b"\xDF" in raw, "Byte 0xDF ('ß' in ISO-8859-1) not found in source file."

    # 5) The file must NOT be valid UTF-8
    with pytest.raises(
        UnicodeDecodeError, match="invalid start byte|cannot decode byte"
    ):
        raw.decode("utf-8")


def test_target_file_does_not_exist_yet():
    assert not os.path.exists(
        TARGET_FILE
    ), (
        f"Target file {TARGET_FILE!r} should NOT exist before conversion. "
        "It looks like the task may have been performed already."
    )


def test_conversion_log_absent_or_empty():
    """
    The conversion log either should not exist or be an empty regular file.
    Any non-empty existing file would indicate that the student has already
    started modifying it, which is outside the 'initial state'.
    """
    if not os.path.exists(CONVERSION_LOG):
        pytest.skip(f"{CONVERSION_LOG!r} does not exist yet — this is acceptable.")
    else:
        assert os.path.isfile(
            CONVERSION_LOG
        ), f"{CONVERSION_LOG!r} exists but is not a regular file."
        size = os.path.getsize(CONVERSION_LOG)
        assert (
            size == 0
        ), f"{CONVERSION_LOG!r} should be empty at the initial state, found {size} bytes."