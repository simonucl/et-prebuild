# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem *before*
# the student starts working on the localization-update task.
#
# It checks:
#   • Presence and writability of /home/user/project/translations
#   • Exact contents of the English master file (app_en.ini)
#   • Contents of the Spanish file (app_es.ini) and confirms which keys are
#     intentionally missing
#   • Absence of the yet-to-be-created /home/user/translation_update.log

import os
from pathlib import Path
import configparser
import pytest

BASE_DIR = Path("/home/user/project/translations")
EN_FILE = BASE_DIR / "app_en.ini"
ES_FILE = BASE_DIR / "app_es.ini"
LOG_FILE = Path("/home/user/translation_update.log")

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _read_file(path: Path) -> str:
    """Return file contents as a raw string."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def _parse_ini(path: Path) -> configparser.ConfigParser:
    """Parse INI file using configparser while keeping case sensitivity."""
    parser = configparser.ConfigParser()
    parser.optionxform = str  # keep keys case-sensitive
    with path.open("r", encoding="utf-8") as f:
        parser.read_file(f)
    return parser


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_translations_directory_exists_and_writable():
    assert BASE_DIR.exists(), (
        f"Required directory {BASE_DIR} is missing; create it before starting."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory."
    )
    assert os.access(BASE_DIR, os.W_OK), (
        f"Directory {BASE_DIR} is not writable by the current user."
    )


def test_app_en_ini_exact_contents():
    expected = (
        "[General]\n"
        "welcome=Welcome\n"
        "exit=Exit\n"
        "\n"
        "[Errors]\n"
        "file_not_found=File not found\n"
        "permission_denied=Permission denied\n"
    )
    assert EN_FILE.exists(), (
        f"Missing English source file: {EN_FILE}"
    )
    actual = _read_file(EN_FILE)
    # Strip a *single* trailing newline from both strings for robustness
    assert actual.rstrip("\n") == expected.rstrip("\n"), (
        "The contents of app_en.ini do not match the expected English master "
        "file. Ensure the file has exactly the specified keys and layout."
    )


def test_app_es_ini_initial_state_and_expected_missing_keys():
    assert ES_FILE.exists(), (
        f"Missing Spanish translation file: {ES_FILE}"
    )

    # 1) Validate the exact starter contents (including blank lines)
    expected_raw = (
        "[General]\n"
        "welcome=Bienvenido\n"
        "\n"
        "[Errors]\n"
        "file_not_found=Archivo no encontrado\n"
    )
    actual_raw = _read_file(ES_FILE)
    assert actual_raw.rstrip("\n") == expected_raw.rstrip("\n"), (
        "The initial Spanish file (app_es.ini) does not match the expected "
        "starting state. Do not modify this file before running the script."
    )

    # 2) Confirm which keys are currently missing vs. the English source
    en_cfg = _parse_ini(EN_FILE)
    es_cfg = _parse_ini(ES_FILE)

    # Helper: collect missing keys per section
    missing = {}
    for section in en_cfg.sections():
        en_keys = set(en_cfg[section].keys())
        es_keys = set(es_cfg[section].keys()) if es_cfg.has_section(section) else set()
        diff = en_keys - es_keys
        if diff:
            missing[section] = diff

    # The expected missing keys as per the problem statement
    expected_missing = {
        "General": {"exit"},
        "Errors": {"permission_denied"},
    }

    assert missing == expected_missing, (
        "Unexpected set of missing keys in app_es.ini.\n"
        f"Expected: {expected_missing}\n"
        f"Found:    {missing}\n"
        "Ensure the Spanish file has not been pre-filled with keys that are "
        "supposed to be added later."
    )


def test_translation_update_log_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the update script is run."
    )