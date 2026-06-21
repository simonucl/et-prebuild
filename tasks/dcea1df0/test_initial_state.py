# test_initial_state.py
#
# Pytest test-suite that validates the repository **before** the student starts
# working on the task.  It deliberately checks ONLY the resources that must be
# pre-populated by the exercise description and never touches any file or
# directory that the student is supposed to create later (venv, helper script,
# log file, …).
#
# The tests assert:
#   • mandatory directories exist
#   • mandatory files exist
#   • exact content expectations for the template .pot file
#   • exact absence/presence rules for the two *.po files
#
# Any failure message points directly to the missing/incorrect element so the
# student immediately knows what part of the initial sandbox is broken.
#
# Only stdlib + pytest are used.

from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
TEMPLATE_FILE = PROJECT_ROOT / "locale" / "templates" / "app.pot"
PO_EN_FILE = PROJECT_ROOT / "locale" / "en_US" / "LC_MESSAGES" / "app.po"
PO_FR_FILE = PROJECT_ROOT / "locale" / "fr_FR" / "LC_MESSAGES" / "app.po"


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        # Let the test itself raise the assertion; return empty to keep helpers simple
        return ""


def assert_contains(content: str, snippet: str, *, path: Path) -> None:
    assert (
        snippet in content
    ), f"File {path} is expected to contain the snippet:\n{snippet!r}\nBut it was not found."


def assert_not_contains(content: str, snippet: str, *, path: Path) -> None:
    assert (
        snippet not in content
    ), f"File {path} unexpectedly contains the snippet:\n{snippet!r}\nIt should NOT be there before the student runs anything."


# --------------------------------------------------------------------------- #
# Directory / file existence checks                                           #
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    expected_dirs = [
        PROJECT_ROOT / "locale",
        PROJECT_ROOT / "locale" / "templates",
        PROJECT_ROOT / "locale" / "en_US" / "LC_MESSAGES",
        PROJECT_ROOT / "locale" / "fr_FR" / "LC_MESSAGES",
    ]
    for d in expected_dirs:
        assert d.is_dir(), f"Required directory {d} is missing."


def test_required_files_exist():
    expected_files = [TEMPLATE_FILE, PO_EN_FILE, PO_FR_FILE]
    for f in expected_files:
        assert f.is_file(), f"Required file {f} is missing."


# --------------------------------------------------------------------------- #
# Content inspection                                                          #
# --------------------------------------------------------------------------- #
def test_template_file_has_expected_messages():
    """The template must already contain both HELLO_WORLD and MSG_NEW."""
    content = load_file(TEMPLATE_FILE)
    assert_contains(content, 'msgid "HELLO_WORLD"', path=TEMPLATE_FILE)
    assert_contains(content, 'msgid "MSG_NEW"', path=TEMPLATE_FILE)
    assert_contains(
        content, 'msgstr "A new message"', path=TEMPLATE_FILE
    ), "Template must include the default string for MSG_NEW."


def test_po_files_do_not_yet_contain_msg_new():
    """Before the student runs the merge, MSG_NEW must NOT appear in *.po files."""
    for po_path in (PO_EN_FILE, PO_FR_FILE):
        content = load_file(po_path)
        assert_not_contains(content, 'msgid "MSG_NEW"', path=po_path)


def test_po_files_contain_exactly_one_translation_entry_initially():
    """
    Each *.po must contain exactly one real translation entry (HELLO_WORLD)
    besides the header. We count occurrences of 'msgid "' lines excluding the
    header line which is an empty msgid.
    """
    for po_path in (PO_EN_FILE, PO_FR_FILE):
        lines = load_file(po_path).splitlines()
        # collect all msgid lines
        msgid_lines = [ln for ln in lines if ln.startswith("msgid ")]
        # The first msgid should be the empty header, the second is HELLO_WORLD
        assert (
            len(msgid_lines) == 2
        ), (
            f"File {po_path} is expected to contain exactly one translation entry "
            f"(HELLO_WORLD) plus the header, but {len(msgid_lines) - 1} entries were found."
        )
        assert msgid_lines[1] == 'msgid "HELLO_WORLD"', (
            f"Second msgid inside {po_path} should be HELLO_WORLD, "
            f"found: {msgid_lines[1]!r}"
        )