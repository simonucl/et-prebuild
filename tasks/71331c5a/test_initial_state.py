# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student runs their localisation-compilation script.
#
# What we verify:
#   • The template POT file exists, is non-empty and looks like a POT file.
#   • The three source PO files (en, fr, es) exist, are non-empty and
#     contain the correct “Language: <lang>” header.
#   • The writable logs directory exists and is empty.
#
# What we deliberately do **NOT** test:
#   • Presence (or absence) of any output artefacts such as compiled MO
#     files, process_log.txt or summary.txt – those are deliverables and are
#     outside the scope of the *initial* state checks.
#
# Only standard library modules plus pytest are used, as required.

import pathlib
import textwrap

import pytest

# --------------------------------------------------------------------------- #
# Constants for paths                                                         #
# --------------------------------------------------------------------------- #
HOME = pathlib.Path("/home/user")
BASE_DIR = HOME / "localization"

TEMPLATE_FILE = BASE_DIR / "source" / "messages.pot"

PO_DIR = BASE_DIR / "project" / "po"
PO_FILES = {
    "en": PO_DIR / "en.po",
    "fr": PO_DIR / "fr.po",
    "es": PO_DIR / "es.po",
}

LOGS_DIR = BASE_DIR / "logs"


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def read_file(path: pathlib.Path) -> str:
    """Return the full text content of *path* as UTF-8, stripping no newlines."""
    return path.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_template_pot_exists_and_non_empty():
    """The updated template POT file must already exist and be usable."""
    assert TEMPLATE_FILE.is_file(), (
        f"Template file {TEMPLATE_FILE} is missing. "
        "It should be provided to the student."
    )

    size = TEMPLATE_FILE.stat().st_size
    assert size > 0, f"Template file {TEMPLATE_FILE} is empty (size={size})."

    text = read_file(TEMPLATE_FILE)
    expected_snippet = textwrap.dedent(
        """
        msgid ""
        msgstr ""
        """
    ).strip()
    assert expected_snippet in text, (
        f"Template file {TEMPLATE_FILE} does not appear to contain a valid "
        'gettext header (could not find \'msgid ""\\nmsgstr ""\').'
    )


@pytest.mark.parametrize("lang", ["en", "fr", "es"])
def test_po_files_exist_and_have_language_header(lang):
    """Each existing PO file must be present, non-empty and self-identify."""
    po_path = PO_FILES[lang]

    assert po_path.is_file(), (
        f"PO file for language '{lang}' expected at {po_path} but was not found."
    )

    size = po_path.stat().st_size
    assert size > 0, f"PO file {po_path} is empty (size={size})."

    text = read_file(po_path)

    expected_header = f'Language: {lang}\\n'
    assert expected_header in text, (
        f"PO file {po_path} does not contain the required "
        f"Language header line '{expected_header.strip()}'."
    )


def test_logs_directory_exists_and_is_empty():
    """An empty, writable logs directory should already be in place."""
    assert LOGS_DIR.is_dir(), (
        f"Logs directory {LOGS_DIR} is missing. "
        "It should be created for the student beforehand."
    )

    leftover_items = [p for p in LOGS_DIR.iterdir() if p.name not in (".", "..")]
    assert not leftover_items, (
        f"Logs directory {LOGS_DIR} is expected to be empty initially, "
        f"but found: {', '.join(str(p) for p in leftover_items)}"
    )