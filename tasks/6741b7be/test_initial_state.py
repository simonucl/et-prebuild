# test_initial_state.py
#
# This pytest suite validates that the initial filesystem state of the
# localization exercise is exactly as expected *before* the student starts
# working.  It deliberately avoids checking for any of the artefacts that
# the student is supposed to create or modify later.

from pathlib import Path
import pytest
import re

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
TRANSLATIONS_DIR = PROJECT_DIR / "translations"
PATCHES_DIR = HOME / "patches"

EN_PO = TRANSLATIONS_DIR / "en.po"
ES_PO = TRANSLATIONS_DIR / "es.po"
PATCH_FILE = PATCHES_DIR / "new_strings.patch"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file missing: {path}")


# ---------------------------------------------------------------------------
# Directory / file presence
# ---------------------------------------------------------------------------

def test_directories_exist():
    """
    Make sure the directory structure that the exercise description relies on
    is present.
    """
    assert PROJECT_DIR.is_dir(), f"Missing project directory: {PROJECT_DIR}"
    assert TRANSLATIONS_DIR.is_dir(), f"Missing translations directory: {TRANSLATIONS_DIR}"
    assert PATCHES_DIR.is_dir(), f"Missing patches directory: {PATCHES_DIR}"


@pytest.mark.parametrize("po_path", [EN_PO, ES_PO])
def test_po_files_exist(po_path):
    """Both en.po and es.po must be present before any work begins."""
    assert po_path.is_file(), f"Expected PO file does not exist: {po_path}"


def test_patch_file_exists():
    assert PATCH_FILE.is_file(), f"Missing patch file: {PATCH_FILE}"


# ---------------------------------------------------------------------------
# Content of en.po (initial state)
# ---------------------------------------------------------------------------

def test_en_po_initial_state():
    content = read_file(EN_PO)

    # Correct header and revision date
    assert 'Project-Id-Version: ExampleProject 1.0' in content, "en.po header is incorrect or missing."
    assert 'PO-Revision-Date: 2023-10-01 10:00+0000' in content, "en.po has unexpected PO-Revision-Date."
    # No new string yet
    assert 'msgid "Goodbye"' not in content, 'en.po should NOT yet contain the "Goodbye" message.'
    # Existing string present once
    assert content.count('msgid "Hello"') == 1, 'en.po should contain exactly one "Hello" msgid.'


# ---------------------------------------------------------------------------
# Content of es.po (initial state)
# ---------------------------------------------------------------------------

def test_es_po_initial_state():
    content = read_file(ES_PO)

    assert 'Project-Id-Version: ExampleProject 1.0' in content, "es.po header is incorrect or missing."
    assert 'PO-Revision-Date: 2023-10-01 10:00+0000' in content, "es.po has unexpected PO-Revision-Date."
    # Spanish translation should be plain "Hola" (no accents/exclamations yet)
    pattern = r'msgid\s+"Hello"\s+msgstr\s+"Hola"'
    assert re.search(pattern, content, re.MULTILINE), (
        'es.po should translate "Hello" to "Hola" and not yet be revised.'
    )
    # The new "Goodbye" string should NOT be present yet
    assert 'msgid "Goodbye"' not in content, 'es.po should NOT yet contain the "Goodbye" message.'


# ---------------------------------------------------------------------------
# Content of the patch file
# ---------------------------------------------------------------------------

def test_patch_file_contents():
    """
    The patch must introduce:
      • a new "Goodbye" message in both en.po and es.po
      • a modification of the Spanish "Hello" translation
    """
    patch = read_file(PATCH_FILE)

    # Ensure it touches both PO files
    assert 'diff --git a/translations/en.po b/translations/en.po' in patch, \
        "Patch does not appear to modify en.po."
    assert 'diff --git a/translations/es.po b/translations/es.po' in patch, \
        "Patch does not appear to modify es.po."

    # Must add Goodbye block to both files
    assert '+msgid "Goodbye"' in patch, 'Patch is expected to add a "Goodbye" msgid.'
    # Spanish translation of Hello should be updated (from Hola to ¡Hola!)
    assert '-msgstr "Hola"' in patch and '+msgstr "¡Hola!"' in patch, \
        'Patch should update the Spanish translation of "Hello" from "Hola" to "¡Hola!".'