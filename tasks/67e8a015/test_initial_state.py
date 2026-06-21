# test_initial_state.py
#
# This test-suite verifies that the workspace is in the **initial** state
# expected **before** the student begins the exercise.  It checks only the
# pre-existing template file and its content, and deliberately avoids testing
# for any of the files or directories that the student is supposed to create
# (e.g. “fr_FR/”, “messages.po”, “update.log”).
#
# If any assertion fails, the error message will make it clear what is missing
# or incorrect so the template repository can be fixed.

from pathlib import Path
import pytest


TEMPLATES_DIR = Path("/home/user/localization/templates")
TEMPLATE_FILE = TEMPLATES_DIR / "messages.pot"

EXPECTED_POT_CONTENT = (
    'msgid ""\n'
    'msgstr ""\n'
    '"Project-Id-Version: 1.2\\n"\n'
    '"Report-Msgid-Bugs-To: you@example.com\\n"\n'
    '"POT-Creation-Date: 2023-06-30 09:00+0000\\n"\n'
    '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n'
    '"Language-Team: \\n"\n'
    '"MIME-Version: 1.0\\n"\n'
    '"Content-Type: text/plain; charset=UTF-8\\n"\n'
    '"Content-Transfer-Encoding: 8bit\\n"\n'
)


def test_templates_directory_exists():
    """
    The /home/user/localization/templates directory must exist.
    """
    assert TEMPLATES_DIR.is_dir(), (
        f"Expected directory {TEMPLATES_DIR} to exist, "
        "but it is missing."
    )


def test_messages_pot_exists():
    """
    The template file messages.pot must exist inside the templates directory.
    """
    assert TEMPLATE_FILE.is_file(), (
        f"Expected template file {TEMPLATE_FILE} to exist, "
        "but it is missing."
    )


def test_messages_pot_content_is_exact():
    """
    The messages.pot file must match the exact expected content.
    """
    actual = TEMPLATE_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_POT_CONTENT, (
        f"Content of {TEMPLATE_FILE} does not match the expected initial "
        "template.\n\n"
        "---- Expected ----\n"
        f"{EXPECTED_POT_CONTENT}\n"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_project_id_version_is_single_and_is_1_2():
    """
    Ensure exactly one Project-Id-Version header exists and that its value is 1.2.
    This guards against accidental manual edits that might introduce duplicates.
    """
    lines = TEMPLATE_FILE.read_text(encoding="utf-8").splitlines()
    piv_lines = [ln for ln in lines if "Project-Id-Version:" in ln]
    assert len(piv_lines) == 1, (
        "messages.pot should contain exactly one 'Project-Id-Version' header, "
        f"found {len(piv_lines)}."
    )
    assert 'Project-Id-Version: 1.2\\n' in piv_lines[0], (
        "The existing 'Project-Id-Version' header must have the value '1.2'. "
        f"Actual line: {piv_lines[0]!r}"
    )