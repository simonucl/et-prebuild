# test_initial_state.py
#
# Pytest suite that verifies the operating-system / file-system **before**
# the student performs any action.
#
# It checks that:
#   • Only the initial files/directories described in the task exist.
#   • Their contents match the specification (e.g. untranslated msgstr "").
#   • Output artefacts such as messages.mo or the final report do *not* exist.
#
# If any assertion fails, the error message pinpoints exactly what is wrong,
# helping the student understand what needs to be fixed.

import os
from pathlib import Path
import pytest

# --- Constants -------------------------------------------------------------

HOME = Path("/home/user").resolve()

PO_PATH = HOME / "projects/website/locale/fr/LC_MESSAGES/messages.po"
MO_PATH = HOME / "projects/website/locale/fr/LC_MESSAGES/messages.mo"
DNS_SEED_PATH = HOME / "resources/dns_seed.txt"
LOGS_DIR = HOME / "projects/website/logs"
REPORT_PATH = LOGS_DIR / "update_2023-10-31.log"

EXPECTED_DNS_LINES = [
    "staging.l10n.test 203.0.113.30",
    "api.l10n.test     203.0.113.31",
]

# Exact snippet that must *precede* any modification
PO_EXPECTED_SNIPPET = [
    '#: src/errors.c:45',
    'msgid "Server unreachable"',
    'msgstr ""',
]

# --- Helper functions ------------------------------------------------------


def read_text_lines(path: Path):
    """Return the list of lines in *path* stripped of trailing newlines."""
    with path.open("r", encoding="utf-8") as fp:
        return [ln.rstrip("\n") for ln in fp.readlines()]


# --- Tests -----------------------------------------------------------------


def test_po_file_exists_and_is_untranslated():
    assert PO_PATH.is_file(), (
        f"Expected PO file at {PO_PATH}, but it is missing."
    )

    lines = read_text_lines(PO_PATH)

    # Ensure the critical three-line untranslated snippet exists exactly once
    snippet_idx = None
    for i in range(len(lines) - len(PO_EXPECTED_SNIPPET) + 1):
        if lines[i : i + len(PO_EXPECTED_SNIPPET)] == PO_EXPECTED_SNIPPET:
            snippet_idx = i
            break

    assert snippet_idx is not None, (
        f"{PO_PATH} does not contain the expected untranslated block:\n"
        + "\n".join(PO_EXPECTED_SNIPPET)
    )

    # Sanity-check that the new French translation is NOT present yet
    french_translation_present = any(
        'msgstr "Serveur injoignable"' in ln for ln in lines
    )
    assert not french_translation_present, (
        f"{PO_PATH} already contains the French translation; "
        "the initial state should still be untranslated."
    )


def test_dns_seed_file_exists_and_has_expected_lines():
    assert DNS_SEED_PATH.is_file(), (
        f"DNS seed file {DNS_SEED_PATH} is missing."
    )

    lines = [ln for ln in read_text_lines(DNS_SEED_PATH) if ln.strip()]

    assert lines == EXPECTED_DNS_LINES, (
        f"{DNS_SEED_PATH} does not contain the expected lines.\n"
        f"Expected:\n{EXPECTED_DNS_LINES}\nFound:\n{lines}"
    )


def test_logs_directory_exists_and_is_empty():
    assert LOGS_DIR.is_dir(), f"Logs directory {LOGS_DIR} is missing."
    files = [p for p in LOGS_DIR.iterdir() if p.is_file()]
    assert not files, (
        f"Logs directory {LOGS_DIR} should be empty at start, "
        f"but found files: {[p.name for p in files]}"
    )


def test_report_file_does_not_exist_yet():
    assert not REPORT_PATH.exists(), (
        f"Report file {REPORT_PATH} should not exist before the student "
        "creates it."
    )


def test_mo_file_does_not_exist_yet():
    assert not MO_PATH.exists(), (
        f"Compiled MO file {MO_PATH} should not exist at the beginning."
    )