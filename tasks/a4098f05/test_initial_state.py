# test_initial_state.py
#
# This pytest module validates the *initial* state of the project workspace
# before the student performs any actions.  It checks that the expected
# source log file already exists with the exact, prescribed contents and that
# the surrounding directory hierarchy is in place.
#
# NOTE:  We intentionally do NOT look for (or forbid) the presence of any
#        yet-to-be-produced artefacts, in keeping with the task requirements.

from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_ROOT = HOME / "project"
LOG_DIR = PROJECT_ROOT / "logs"
SOURCE_LOG = LOG_DIR / "update_2023-04-01.log"


EXPECTED_SOURCE_CONTENT = (
    "[INFO]  I1000: Assets scanned: 42\n"
    "[ERROR] E2300: Missing translation for locale 'fr' key 'home.title'\n"
    "[ERROR] E2300: Missing translation for locale 'de' key 'settings.label'\n"
    "[ERROR] E2300: Missing translation for locale 'es' key 'about.header'\n"
    "[WARN]  W3400: Placeholder count mismatch in 'de' for key 'login.button'\n"
    "[WARN]  W3400: Placeholder count mismatch in 'fr' for key 'profile.subtitle'\n"
    "[INFO]  I1001: Catalog compiled\n"
    "[ERROR] E2300: Missing translation for locale 'fr' key 'logout.confirm'\n"
    "[WARN]  W3400: Placeholder count mismatch in 'it' for key 'cart.total'\n"
    "[INFO]  I1002: Build complete\n"
    "[ERROR] E2300: Missing translation for locale 'de' key 'contact.phone'\n"
    "[WARN]  W3400: Placeholder count mismatch in 'de' for key 'order.summary'\n"
    "[ERROR] E2300: Missing translation for locale 'fr' key 'checkout.button'\n"
    "[ERROR] E2300: Missing translation for locale 'de' key 'error.404'\n"
    "[INFO]  Summary: 6 missing translations, 4 warnings, 2 infos\n"
)

# ---------- Tests ------------------------------------------------------------


def test_project_directory_structure():
    """Ensure /home/user/project/logs structure exists."""
    assert PROJECT_ROOT.is_dir(), (
        f"Expected directory {PROJECT_ROOT} is missing."
    )
    assert LOG_DIR.is_dir(), (
        f"Expected directory {LOG_DIR} is missing."
    )


def test_source_log_exists():
    """Verify the source log file exists before any student action."""
    assert SOURCE_LOG.is_file(), (
        f"Required source log file {SOURCE_LOG} is missing."
    )


def test_source_log_content_exact_match():
    """
    The source log file must match the exact lines provided in the task
    description, including ordering and trailing newline.
    """
    content = SOURCE_LOG.read_text(encoding="utf-8")
    # Helpful diff if something is wrong
    assert content == EXPECTED_SOURCE_CONTENT, (
        "Contents of the source log do not match the expected initial state.\n"
        "------ Expected (snippet) ------\n"
        f"{EXPECTED_SOURCE_CONTENT[:300]}...\n"
        "------ Got (snippet) ------\n"
        f"{content[:300]}..."
    )