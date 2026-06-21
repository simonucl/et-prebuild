# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student performs any actions described in the “Localization Engineer”
# exercise.  These tests assert that the repository clone is in its pristine
# starting condition so that subsequent grading (of the student’s solution)
# is meaningful.
#
# Only Python’s standard library and pytest are used, as required.

import json
from pathlib import Path
import pytest

# Root directory that the exercise works in.
PROJECT_ROOT = Path("/home/user/project")

LOCALES_DIR = PROJECT_ROOT / "locales"
LOGS_DIR = PROJECT_ROOT / "logs"
API_TEST_LOG = LOGS_DIR / "api_test.log"

EN_LOCALE_FILE = LOCALES_DIR / "en.json"
FR_LOCALE_FILE = LOCALES_DIR / "fr.json"


def _read_text(path: Path) -> str:
    """
    Helper that returns a file’s text with surrounding whitespace stripped.
    Fails with a clear message when the file is missing.
    """
    if not path.exists():
        pytest.fail(f"Expected file at {path} is missing.")
    if not path.is_file():
        pytest.fail(f"Expected {path} to be a file, but it is not.")
    return path.read_text(encoding="utf-8").strip()


# --------------------------------------------------------------------------- #
# 1. Basic repository layout                                                   #
# --------------------------------------------------------------------------- #
def test_project_layout():
    """Validate that /home/user/project/ and its ‘locales’ sub-directory exist."""
    assert PROJECT_ROOT.exists() and PROJECT_ROOT.is_dir(), (
        f"Directory {PROJECT_ROOT} is missing."
    )
    assert LOCALES_DIR.exists() and LOCALES_DIR.is_dir(), (
        f"Directory {LOCALES_DIR} is missing."
    )


# --------------------------------------------------------------------------- #
# 2. English locale must be untouched                                          #
# --------------------------------------------------------------------------- #
def test_en_json_exists_with_expected_content():
    """
    The English locale file must exist and contain exactly the untouched
    starting JSON from the specification.
    """
    expected = '{"hello":"Hello","bye":"Goodbye"}'
    actual = _read_text(EN_LOCALE_FILE)
    assert actual == expected, (
        f"Content of {EN_LOCALE_FILE} is incorrect.\n"
        f"Expected: {expected}\n"
        f"Actual:   {actual}"
    )

    # Additionally confirm it parses as valid JSON with the right keys.
    try:
        data = json.loads(actual)
    except json.JSONDecodeError as e:
        pytest.fail(f"{EN_LOCALE_FILE} is not valid JSON: {e}")

    assert set(data) == {"hello", "bye"}, (
        f"{EN_LOCALE_FILE} should only contain keys 'hello' and 'bye', "
        f"found: {list(data.keys())}"
    )


# --------------------------------------------------------------------------- #
# 3. French locale must reflect the *initial* (pre-change) state               #
# --------------------------------------------------------------------------- #
def test_fr_json_pre_change_state():
    """
    The French locale file must exist and reflect the state *before* the
    student applies any of the requested modifications.
    """
    expected = '{"hello":"Bonjour","bye":"Au revoir","obsolete":"obsolète"}'
    actual = _read_text(FR_LOCALE_FILE)
    assert actual == expected, (
        f"Content of {FR_LOCALE_FILE} does not match the expected initial state.\n"
        f"Expected: {expected}\n"
        f"Actual:   {actual}"
    )

    # Validate JSON parses and keys are exactly as expected
    try:
        data = json.loads(actual)
    except json.JSONDecodeError as e:
        pytest.fail(f"{FR_LOCALE_FILE} is not valid JSON: {e}")

    assert list(data.keys()) == ["hello", "bye", "obsolete"], (
        f"{FR_LOCALE_FILE} must contain keys in order "
        f"['hello', 'bye', 'obsolete']; found {list(data.keys())}"
    )


# --------------------------------------------------------------------------- #
# 4. No API test log should be present yet                                     #
# --------------------------------------------------------------------------- #
def test_api_test_log_absent_initially():
    """
    The transcript log (/logs/api_test.log) should not exist before the
    student performs any curl calls.  Its presence would indicate that the
    final-state artefacts have been produced prematurely.
    """
    assert not API_TEST_LOG.exists(), (
        f"{API_TEST_LOG} should NOT exist before the task is started."
    )


# --------------------------------------------------------------------------- #
# 5. Logs directory should either be absent or empty                           #
# --------------------------------------------------------------------------- #
def test_logs_directory_state():
    """
    If /logs exists at this point, it should be empty.  This prevents false
    positives from prior runs leaking into the environment.
    """
    if LOGS_DIR.exists():
        assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
        contents = list(LOGS_DIR.iterdir())
        assert not contents, (
            f"{LOGS_DIR} is expected to be empty before the student begins, "
            f"but it already contains: {[p.name for p in contents]}"
        )