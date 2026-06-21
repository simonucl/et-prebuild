# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating‐system /
# filesystem before the student performs any action for the “add French
# translation” task.  These tests **must** all pass *before* the student starts
# working; if any of them fail, that means the environment the student received
# is already wrong.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
I18N_DIR = HOME / "i18n"
SOURCE_DIR = I18N_DIR / "source"
ES_DIR = I18N_DIR / "es"
FR_DIR = I18N_DIR / "fr"              # Must NOT exist yet
POT_FILE = SOURCE_DIR / "messages.pot"
ES_PO_FILE = ES_DIR / "messages.po"
FR_PO_FILE = FR_DIR / "messages.po"   # Must NOT exist yet
LOG_FILE = HOME / "update_translation.log"  # Must NOT exist yet


@pytest.fixture(scope="module")
def pot_content():
    """Return the bytes content of the .pot file for reuse."""
    return POT_FILE.read_bytes()


def test_required_directories_and_files_exist():
    """Verify that the Spanish directory and the source directory exist,
    and that the French directory does *not* exist yet."""
    assert I18N_DIR.is_dir(), f"Directory {I18N_DIR} is missing."
    assert SOURCE_DIR.is_dir(), f"Directory {SOURCE_DIR} is missing."
    assert ES_DIR.is_dir(), f"Directory {ES_DIR} is missing."
    assert not FR_DIR.exists(), (
        f"{FR_DIR} should NOT exist before the student creates it."
    )


def test_required_files_exist_and_permissions():
    """Verify the presence and permissions of the provided files."""
    # Spanish .po file (content not important, only existence)
    assert ES_PO_FILE.is_file(), f"Spanish PO file {ES_PO_FILE} is missing."
    # Template .pot file
    assert POT_FILE.is_file(), f"Template POT file {POT_FILE} is missing."

    # Permissions: 0o644 for files
    for file_path in (POT_FILE, ES_PO_FILE):
        mode = stat.S_IMODE(os.stat(file_path).st_mode)
        assert mode == 0o644, (
            f"{file_path} should have permissions 644, found {oct(mode)}."
        )

    # Verify that the French .po and the log file do not exist yet
    assert not FR_PO_FILE.exists(), (
        f"{FR_PO_FILE} should NOT exist before the student copies the template."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the student writes the log."
    )


def test_pot_file_exact_expected_content(pot_content):
    """The .pot file must match the exact 11-line reference provided in
    the task description."""
    expected_lines = [
        'msgid ""\n',
        'msgstr ""\n',
        '"Project-Id-Version: PACKAGE VERSION\\n"\n',
        '"POT-Creation-Date: 2023-01-01 12:00+0000\\n"\n',
        '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n',
        '"Report-Msgid-Bugs-To: \\n"\n',
        '"Language-Team: \\n"\n',
        '"Language: \\n"\n',
        '"MIME-Version: 1.0\\n"\n',
        '"Content-Type: text/plain; charset=UTF-8\\n"\n',
        '"Content-Transfer-Encoding: 8bit\\n"\n',
    ]

    actual_text = pot_content.decode("utf-8", errors="strict")
    actual_lines = actual_text.splitlines(keepends=True)

    assert actual_lines == expected_lines, (
        f"{POT_FILE} contents differ from the expected template.\n"
        "Expected lines:\n"
        + "".join(expected_lines)
        + "\nActual lines:\n"
        + "".join(actual_lines)
    )


def test_pot_file_has_trailing_newline(pot_content):
    """Ensure the .pot file ends with exactly one trailing newline."""
    assert pot_content.endswith(b"\n"), (
        f"{POT_FILE} must end with a single newline character."
    )