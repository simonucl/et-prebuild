# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem **before**
# the student runs the required shell command.
#
# It asserts that:
#   • Required directories already exist.
#   • The “old” and “new” .po files exist at the correct absolute paths
#     and contain the expected (different) contents.
#   • No log file has been created yet.
#
# No third-party libraries are used; only the Python stdlib + pytest.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user").resolve()

# Absolute paths that the assignment talks about
PROJECT_LOCALE_DIR = HOME / "project" / "locale" / "fr" / "LC_MESSAGES"
UPDATES_DIR = HOME / "updates"
UPDATE_LOGS_DIR = HOME / "update_logs"

OLD_MESSAGES_PO = PROJECT_LOCALE_DIR / "messages.po"
NEW_FR_PO = UPDATES_DIR / "fr.po"
EXPECTED_LOG_FILE = UPDATE_LOGS_DIR / "2024-translation-update.log"


OLD_MESSAGES_PO_CONTENT = """# French translations – OLD
msgid "Hello"
msgstr "Bonjour (old)"
msgid "Bye"
msgstr "Au revoir (old)"
"""

NEW_FR_PO_CONTENT = """# French translations – NEW
msgid "Hello"
msgstr "Bonjour"
msgid "Bye"
msgstr "Au revoir"
"""


@pytest.mark.parametrize(
    "path",
    [
        PROJECT_LOCALE_DIR,
        UPDATES_DIR,
        UPDATE_LOGS_DIR,
    ],
)
def test_required_directories_exist(path: Path):
    assert path.is_dir(), (
        f"Required directory {path} is missing. "
        "Make sure the project skeleton is in place before running the command."
    )


@pytest.mark.parametrize(
    "po_file, expected_content",
    [
        (OLD_MESSAGES_PO, OLD_MESSAGES_PO_CONTENT),
        (NEW_FR_PO, NEW_FR_PO_CONTENT),
    ],
)
def test_po_files_exist_with_expected_content(po_file: Path, expected_content: str):
    assert po_file.is_file(), f"Expected PO file {po_file} is missing."
    content = po_file.read_text(encoding="utf-8")
    # Normalize line endings to LF for comparison robustness
    assert content.replace("\r\n", "\n") == expected_content, (
        f"File {po_file} does not contain the expected initial content."
    )


def test_old_and_new_po_files_are_different():
    """Sanity check: the 'old' and 'new' translation files must differ before the task."""
    old_bytes = OLD_MESSAGES_PO.read_bytes()
    new_bytes = NEW_FR_PO.read_bytes()
    assert old_bytes != new_bytes, (
        "The old and new PO files are already identical; "
        "there would be nothing to overwrite."
    )


def test_log_file_does_not_exist_yet():
    assert not EXPECTED_LOG_FILE.exists(), (
        f"Log file {EXPECTED_LOG_FILE} should not exist before the command runs."
    )


def test_update_logs_directory_is_empty():
    """There should be no files inside /home/user/update_logs/ initially."""
    entries = [p for p in UPDATE_LOGS_DIR.iterdir() if p.is_file()]
    assert entries == [], (
        f"Directory {UPDATE_LOGS_DIR} is expected to be empty but contains: "
        f"{', '.join(str(p) for p in entries)}"
    )