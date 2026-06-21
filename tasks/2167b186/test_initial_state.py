# test_initial_state.py
# PyTest suite that validates the expected **initial** filesystem state
# before the student begins the assignment for enabling French localisation.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constant canonical paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/home/user/project-localization")
LOCALES_DIR = PROJECT_ROOT / "locales"
DIST_DIR = PROJECT_ROOT / "dist"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.example"
ENV_FILE = PROJECT_ROOT / ".env"

EN_US_FILE = LOCALES_DIR / "en_US.json"
ES_ES_FILE = LOCALES_DIR / "es_ES.json"
FR_FR_FILE = LOCALES_DIR / "fr_FR.json"

BUILD_SCRIPT = SCRIPTS_DIR / "build_translations.sh"

DIST_FR_FILE = DIST_DIR / "fr_FR.po"

LOG_FILE = Path("/home/user/localization_update.log")

# ---------------------------------------------------------------------------
# Expected contents (must match byte-for-byte, including trailing newlines)
# ---------------------------------------------------------------------------
ENV_EXAMPLE_CONTENT = (
    "API_KEY=CHANGE_ME\n"
    "DEFAULT_LOCALE=en_US\n"
)

EN_US_JSON_CONTENT = (
    "{\n"
    "  \"greeting\": \"Hello\",\n"
    "  \"farewell\": \"Goodbye\",\n"
    "  \"inquiry\": \"How are you?\"\n"
    "}\n"
)

ES_ES_JSON_CONTENT = (
    "{\n"
    "  \"greeting\": \"Hola\",\n"
    "  \"farewell\": \"Adiós\",\n"
    "  \"inquiry\": \"¿Cómo estás?\"\n"
    "}\n"
)

BUILD_SCRIPT_CONTENT = (
    "#!/usr/bin/env bash\n"
    "set -e\n"
    "if [ -z \"$LOCALE\" ]; then\n"
    "  echo \"LOCALE env variable not set\" >&2\n"
    "  exit 1\n"
    "fi\n"
    "mkdir -p dist\n"
    "jq -r 'to_entries[] | \"\\(.key)=\\(.value)\"' \"locales/${LOCALE}.json\" > \"dist/${LOCALE}.po\"\n"
    "echo \"Built dist/${LOCALE}.po with $(wc -l < \"dist/${LOCALE}.po\") entries\"\n"
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _check_file_exact(path: Path, expected: str):
    assert path.exists(), f"Expected file not found: {path}"
    actual = path.read_text()
    assert actual == expected, (
        f"Contents of {path} do not match the expected template.\n"
        f"--- Expected ---\n{expected!r}\n--- Actual ---\n{actual!r}"
    )

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
def test_env_example_present_and_correct():
    """Verify .env.example exists with the correct default content."""
    _check_file_exact(ENV_EXAMPLE_FILE, ENV_EXAMPLE_CONTENT)


def test_env_file_should_not_exist_yet():
    """The student has not created .env yet; it must not exist."""
    assert not ENV_FILE.exists(), (
        f"File {ENV_FILE} should NOT exist before the task begins."
    )


def test_en_us_json_present_and_correct():
    """Verify the default English locale file is intact."""
    _check_file_exact(EN_US_FILE, EN_US_JSON_CONTENT)


def test_es_es_json_present_and_correct():
    """Verify the default Spanish locale file is intact."""
    _check_file_exact(ES_ES_FILE, ES_ES_JSON_CONTENT)


def test_fr_fr_json_should_not_exist_yet():
    """French locale must not exist before the student creates it."""
    assert not FR_FR_FILE.exists(), (
        f"French locale file {FR_FR_FILE} should NOT exist yet."
    )


def test_build_script_present_correct_and_executable():
    """Ensure the build script exists, is correct, and is executable."""
    _check_file_exact(BUILD_SCRIPT, BUILD_SCRIPT_CONTENT)
    # Check executable bit: at least owner executable.
    st_mode = BUILD_SCRIPT.stat().st_mode
    is_executable = bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Script {BUILD_SCRIPT} exists but is not executable."


def test_dist_directory_exists_and_is_directory():
    """The dist/ directory must already exist (may be empty)."""
    assert DIST_DIR.exists(), f"Directory {DIST_DIR} is missing."
    assert DIST_DIR.is_dir(), f"Expected {DIST_DIR} to be a directory."


def test_dist_fr_file_should_not_exist_yet():
    """No French artefact should have been built yet."""
    assert not DIST_FR_FILE.exists(), (
        f"File {DIST_FR_FILE} should NOT exist before running the build."
    )


def test_log_file_should_not_exist_yet():
    """Log file is produced only after the student completes the task."""
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist before the task begins."
    )