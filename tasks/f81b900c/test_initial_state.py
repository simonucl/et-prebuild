# test_initial_state.py
#
# Pytest suite that validates the **initial** OS / filesystem state
# before the student begins the “un-translated strings” task.
#
# Rules verified:
# 1. The Russian PO file exists at the expected absolute path.
# 2. Exactly three occurrences of the header-style line   msgstr ""   are present
#    (which correspond to three currently untranslated strings).
# 3. No diagnostics directory (or log file) has been created yet.
#
# If any of these assertions fail, the accompanying message will make it
# clear what is missing or incorrect.

import os
from pathlib import Path

# Absolute paths used throughout the tests
LOCALE_DIR = Path("/home/user/project/locale")
RU_PO_FILE = LOCALE_DIR / "ru.po"

DIAG_DIR = Path("/home/user/project/diagnostics")
DIAG_FILE = DIAG_DIR / "untranslated_ru.log"


def test_locale_directory_exists():
    """The /home/user/project/locale directory must exist."""
    assert LOCALE_DIR.exists() and LOCALE_DIR.is_dir(), (
        f"Expected directory {LOCALE_DIR} to exist, but it is missing."
    )


def test_ru_po_file_exists():
    """The Russian PO file must exist at the expected full path."""
    assert RU_PO_FILE.exists() and RU_PO_FILE.is_file(), (
        f"Expected file {RU_PO_FILE} to exist, but it is missing."
    )


def test_ru_po_has_exactly_three_untranslated_strings():
    """
    Count how many lines are literally   msgstr ""   (after stripping whitespace).
    According to the initial-state specification, there must be exactly three.
    """
    with RU_PO_FILE.open(encoding="utf-8") as f:
        untranslated_count = sum(1 for line in f if line.strip() == 'msgstr ""')

    assert untranslated_count == 3, (
        f"Expected exactly 3 untranslated msgstr entries in {RU_PO_FILE}, "
        f"but found {untranslated_count}."
    )


def test_diagnostics_directory_not_yet_created():
    """
    The diagnostics directory (and log file) should not exist *before*
    the student runs their solution.
    """
    assert not DIAG_DIR.exists(), (
        f"Diagnostics directory {DIAG_DIR} should not exist yet, "
        "but it is already present."
    )
    assert not DIAG_FILE.exists(), (
        f"Diagnostics log file {DIAG_FILE} should not exist yet, "
        "but it is already present."
    )