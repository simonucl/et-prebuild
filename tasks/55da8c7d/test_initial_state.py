# test_initial_state.py
"""
Pytest suite to validate the *initial* condition of the filesystem
before the student performs any action.

It asserts that:
1. The required source files and directories exist.
2. Their contents exactly match the expected two-line / three-line
   templates (with a single trailing LF).
3. No premature modifications have been made (e.g. “thanks” key or
   version bump).

Only stdlib + pytest are used.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_ROOT = HOME / "project"
LOCALES_DIR = PROJECT_ROOT / "locales"

EN_FILE = LOCALES_DIR / "en.yaml"
ES_FILE = LOCALES_DIR / "es.yaml"
SETTINGS_FILE = PROJECT_ROOT / "settings.toml"

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def en_content():
    return EN_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def es_content():
    return ES_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def settings_content():
    return SETTINGS_FILE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_structure():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project root directory {PROJECT_ROOT} to exist."
    )
    assert LOCALES_DIR.is_dir(), (
        f"Expected locales directory {LOCALES_DIR} to exist."
    )


@pytest.mark.parametrize(
    "file_path",
    [EN_FILE, ES_FILE],
    ids=["en.yaml", "es.yaml"],
)
def test_locale_files_exist(file_path):
    assert file_path.is_file(), f"Expected locale file {file_path} to exist."


def test_en_yaml_initial_content(en_content):
    expected = 'greeting: "Hello"\n' 'farewell: "Goodbye"\n'
    assert en_content == expected, (
        f"Unexpected content in {EN_FILE}.\n"
        f"Expected (exact, including newlines):\n{repr(expected)}\n"
        f"Got:\n{repr(en_content)}"
    )
    assert "thanks:" not in en_content, (
        f"The key 'thanks:' should NOT yet be present in {EN_FILE}."
    )


def test_es_yaml_initial_content(es_content):
    expected = 'greeting: "Hola"\n' 'farewell: "Adiós"\n'
    assert es_content == expected, (
        f"Unexpected content in {ES_FILE}.\n"
        f"Expected (exact, including newlines):\n{repr(expected)}\n"
        f"Got:\n{repr(es_content)}"
    )
    assert "thanks:" not in es_content, (
        f"The key 'thanks:' should NOT yet be present in {ES_FILE}."
    )


def test_settings_toml_initial_content(settings_content):
    expected = (
        "[build]\n"
        'version = "1.0.0"\n'
        'lang_support = ["en", "es"]\n'
    )
    assert settings_content == expected, (
        f"Unexpected content in {SETTINGS_FILE}.\n"
        f"Expected (exact, including newlines):\n{repr(expected)}\n"
        f"Got:\n{repr(settings_content)}"
    )
    assert 'version = "1.0.1"' not in settings_content, (
        f"The version should still be 1.0.0 in {SETTINGS_FILE}."
    )