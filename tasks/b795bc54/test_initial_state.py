# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem / OS state
# before the student starts working on the “localization engineer” task.
#
# The tests assert that
#   • The required template and translation files exist and contain the
#     exact expected content.
#   • The diagnostics directory and all “output” artefacts are **absent**.
#   • No premature additions such as the “Goodbye.” msgid are present in fr.po.
#
# Only stdlib + pytest are used; all paths are absolute.

import re
from pathlib import Path

PROJECT_DIR = Path("/home/user/project_i18n")
DIAG_DIR = Path("/home/user/diagnostics")
POT_FILE = PROJECT_DIR / "messages.pot"
PO_FILE = PROJECT_DIR / "fr.po"
CSV_FILE = DIAG_DIR / "vmstat_log.csv"
REPORT_FILE = PROJECT_DIR / "update_report.json"


def test_required_directories_exist():
    """Ensure the base directories that must already be present exist."""
    assert Path("/home/user").is_dir(), "/home/user directory is missing"
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} directory is missing"


def test_diagnostics_directory_absent():
    """The diagnostics directory must NOT exist yet."""
    assert not DIAG_DIR.exists(), (
        f"{DIAG_DIR} should not exist before the task starts"
    )


def _normalize(text: str) -> str:
    """
    Return the text with a single trailing newline removed (if present).
    This makes strict string comparison immune to the final newline.
    """
    return text[:-1] if text.endswith("\n") else text


EXPECTED_MESSAGES_POT = _normalize(
    """msgid ""
msgstr ""
"Project-Id-Version: example 1.0\\n"
"Language: en\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

#: src/main.c:10
msgid "Hello, world!"
msgstr ""

#: src/main.c:20
msgid "Goodbye."
msgstr ""
"""
)

EXPECTED_FR_PO = _normalize(
    """msgid ""
msgstr ""
"Project-Id-Version: example 1.0\\n"
"Language: fr\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

#: src/main.c:10
msgid "Hello, world!"
msgstr "Bonjour le monde!"
"""
)


def test_messages_pot_content():
    """Verify that the template file exists and is exactly as expected."""
    assert POT_FILE.is_file(), f"{POT_FILE} is missing"
    actual = _normalize(POT_FILE.read_text(encoding="utf-8"))
    assert (
        actual == EXPECTED_MESSAGES_POT
    ), f"{POT_FILE} contents do not match the expected initial template"


def test_fr_po_content():
    """
    Verify that the French translation file exists, matches the expected
    initial content, and does NOT yet contain the 'Goodbye.' msgid.
    """
    assert PO_FILE.is_file(), f"{PO_FILE} is missing"
    actual = _normalize(PO_FILE.read_text(encoding="utf-8"))
    assert (
        actual == EXPECTED_FR_PO
    ), f"{PO_FILE} contents do not match the expected initial translation"
    assert (
        'msgid "Goodbye."' not in actual
    ), "'Goodbye.' entry should not be present in fr.po before the merge"


def test_no_output_artifacts_exist_yet():
    """Ensure that the artefacts which will be created by the student do not pre-exist."""
    assert not CSV_FILE.exists(), f"{CSV_FILE} should not exist before the task starts"
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} should not exist before the task starts"
    )