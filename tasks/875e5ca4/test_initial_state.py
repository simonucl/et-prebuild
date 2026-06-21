# test_initial_state.py
#
# Pytest suite to validate the *initial* operating-system / filesystem state
# before the student performs any action for the “missing French translations”
# task.
#
# What we check:
#   • The working directory /home/user/localization exists and is a directory.
#   • The directory has permission bits 0o755 (rwxr-xr-x) **or more restrictive**.
#   • The file /home/user/localization/translations.csv exists, is a regular file,
#     is UTF-8 decodable, has permission bits 0o644 (rw-r--r--) **or more
#     restrictive**, and its *exact* byte contents match the specification.
#
# Per the instructions we deliberately do *not* test for any of the expected
# output artifacts (e.g. /home/user/localization/missing_fr.txt) because those
# belong to the post-exercise state.

import os
import stat
import pytest

LOC_DIR = "/home/user/localization"
CSV_PATH = os.path.join(LOC_DIR, "translations.csv")

EXPECTED_CSV_BYTES = (
    b"key,en_US,fr_FR,de_DE\n"
    b"welcome,Welcome,,Willkommen\n"
    b"bye,Goodbye,Au revoir,Auf Wiedersehen\n"
    b"thanks,Thank you,,Danke\n"
    b"hello,Hello,Bonjour,Hallo\n"
    b"morning,Good morning,,Guten Morgen\n"
)


def _is_mode_at_most(path: str, expected_mode: int) -> bool:
    """
    Return True iff every permission bit set in 'path' is also present in
    'expected_mode'.  In other words, the file/dir is *not less restrictive*
    than expected_mode.
    """
    actual_mode = stat.S_IMODE(os.stat(path).st_mode)
    # A file is "more restrictive" if it *clears* some of the bits allowed in
    # expected_mode.  Therefore:
    return (actual_mode | expected_mode) == expected_mode


@pytest.mark.parametrize("path", [LOC_DIR])
def test_localization_directory_exists_and_has_correct_mode(path):
    assert os.path.exists(path), f"Required directory {path!r} does not exist."
    assert os.path.isdir(path), f"{path!r} exists but is not a directory."

    expected_mode = 0o755
    assert _is_mode_at_most(path, expected_mode), (
        f"Directory {path} has permission mode "
        f"{oct(stat.S_IMODE(os.stat(path).st_mode))}; expected {oct(expected_mode)} "
        f"or more restrictive."
    )


def test_translations_csv_exists_and_is_regular_file():
    assert os.path.exists(CSV_PATH), (
        f"Required CSV file {CSV_PATH!r} is missing."
    )
    assert os.path.isfile(CSV_PATH), (
        f"{CSV_PATH!r} exists but is not a regular file."
    )


def test_translations_csv_permissions_are_correct():
    expected_mode = 0o644
    actual_mode = stat.S_IMODE(os.stat(CSV_PATH).st_mode)
    assert _is_mode_at_most(CSV_PATH, expected_mode), (
        f"File {CSV_PATH} has permission mode {oct(actual_mode)}; expected "
        f"{oct(expected_mode)} or more restrictive."
    )


def test_translations_csv_contents_are_exact():
    with open(CSV_PATH, "rb") as f:
        contents = f.read()

    assert contents == EXPECTED_CSV_BYTES, (
        f"Contents of {CSV_PATH} do not match the expected specification.\n"
        f"--- Expected ({len(EXPECTED_CSV_BYTES)} bytes) ---\n"
        f"{EXPECTED_CSV_BYTES!r}\n"
        f"--- Found ({len(contents)} bytes) ---\n"
        f"{contents!r}"
    )

    # Additionally verify the file decodes cleanly as UTF-8 to catch encoding
    # regressions.
    try:
        contents.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{CSV_PATH} is not valid UTF-8: {exc}")