# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any actions for the “app” localisation
# task.  These checks guarantee that only the expected prerequisites exist
# and nothing from the desired end-state has been created yet.
#
# Requirements validated:
#   • The French PO file exists.
#   • No locale directory / MO file / report file is present.
#   • .bashrc exists and does *not* already contain the export line.
#   • The msgfmt utility is available in $PATH.
#
# All paths are absolute as required.

import os
import re
import shutil
from pathlib import Path

HOME = Path("/home/user").resolve()
PROJECT_DIR = HOME / "project"
PO_FILE = PROJECT_DIR / "po" / "fr.po"

LOCALES_DIR = PROJECT_DIR / "locales"
LC_MESSAGES_DIR = LOCALES_DIR / "fr" / "LC_MESSAGES"
MO_FILE = LC_MESSAGES_DIR / "app.mo"
REPORT_FILE = LOCALES_DIR / "compile_report.txt"

BASHRC = HOME / ".bashrc"
EXPORT_LINE = 'export APP_LOCALE_PATH="/home/user/project/locales"'


def test_po_file_exists_and_is_non_empty():
    """Ensure the source PO file is in place and reasonably sized."""
    assert PO_FILE.is_file(), (
        f"Prerequisite missing: expected PO file at {PO_FILE}.\n"
        "It must be provided to the student before the task begins."
    )

    size = PO_FILE.stat().st_size
    # A valid PO is typically well over a few hundred bytes; require > 1 KiB.
    assert size >= 1024, (
        f"PO file {PO_FILE} is unexpectedly small ({size} bytes). "
        "Verify that the full translation file was supplied."
    )


def test_locales_directory_absent_initially():
    """No locale tree should exist before the student creates it."""
    assert not LOCALES_DIR.exists(), (
        f"Directory {LOCALES_DIR} already exists, "
        "but the student has not run their solution yet."
    )


def test_mo_file_absent_initially():
    """Compiled MO must not exist yet."""
    assert not MO_FILE.exists(), (
        f"File {MO_FILE} already exists before compilation—"
        "the initial state should be clean."
    )


def test_compile_report_absent_initially():
    """Report file must not be present before the student writes it."""
    assert not REPORT_FILE.exists(), (
        f"Compilation report {REPORT_FILE} found before task execution."
    )


def test_bashrc_exists_and_has_no_export_line():
    """Verify .bashrc exists, and the export line is *not* already present."""
    assert BASHRC.is_file(), (
        f"Expected interactive shell start-up file {BASHRC} to exist."
    )

    with BASHRC.open(encoding="utf-8") as fh:
        bashrc_content = fh.read()

    pattern = re.compile(rf"^{re.escape(EXPORT_LINE)}$", re.MULTILINE)
    assert not pattern.search(bashrc_content), (
        f"The line\n    {EXPORT_LINE}\n"
        "is already present in ~/.bashrc, but it should only be appended "
        "by the student’s solution."
    )


def test_msgfmt_is_available():
    """msgfmt (GNU gettext) must be on PATH for the student to use."""
    msgfmt_path = shutil.which("msgfmt")
    assert msgfmt_path, (
        "GNU gettext utility 'msgfmt' is not available in PATH. "
        "It must be installed so that the student can compile the PO file."
    )