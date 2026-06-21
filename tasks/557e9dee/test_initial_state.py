# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# student/user performs any migration steps.  It checks for:
#
# 1. Presence of the expected directory tree.
# 2. Presence and exact-value correctness of
#    /home/user/projects/cloud_migration/configs/legacy_service.ini
# 3. Correct parse results from the INI file (two sections + key values).
# 4. Absence of the yet-to-be-created
#    /home/user/projects/cloud_migration/migration_summary.txt
#
# The tests are intentionally explicit; any failure message should tell the
# learner exactly what prerequisite element is missing or malformed.

import os
import configparser
import pytest

# --- Constants ----------------------------------------------------------------

ROOT_DIR = "/home/user/projects/cloud_migration"
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")
INI_PATH = os.path.join(CONFIG_DIR, "legacy_service.ini")
SUMMARY_PATH = os.path.join(ROOT_DIR, "migration_summary.txt")

EXPECTED_INI_CONTENT = (
    "[database]\n"
    "host = legacy-db.internal\n"
    "port = 5432\n"
    "user = legacy_user\n"
    "password = secret\n\n"
    "[api]\n"
    "endpoint = https://legacy-api.internal/v1\n"
    "timeout = 30\n"
)

# --- Helper --------------------------------------------------------------------

def _read_file(path):
    """Return file contents; fail with a helpful message if unreadable."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Expected to read {path!r} but got error: {exc}")

# --- Tests ---------------------------------------------------------------------

def test_directory_structure_exists():
    """Ensure the required directory hierarchy exists."""
    expected_dirs = [
        "/home",
        "/home/user",
        "/home/user/projects",
        ROOT_DIR,
        CONFIG_DIR,
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Missing required directory: {d}"

def test_legacy_ini_exists_and_is_correct():
    """Validate the legacy_service.ini file and its exact contents."""
    assert os.path.isfile(INI_PATH), (
        f"The required INI file was not found at {INI_PATH}"
    )

    # Verify full file contents match the spec exactly (including newlines).
    actual = _read_file(INI_PATH)
    assert actual == EXPECTED_INI_CONTENT, (
        "The contents of legacy_service.ini do not match the expected initial "
        "state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_INI_CONTENT}\n"
        "----   Got    ----\n"
        f"{actual}"
    )

def test_ini_parses_to_expected_values():
    """Parse the INI file and confirm the key/value pairs & section count."""
    parser = configparser.ConfigParser()
    parser.read(INI_PATH, encoding="utf-8")

    # Section count must be exactly two.
    sections = parser.sections()
    assert len(sections) == 2, (
        f"Expected exactly 2 sections in {INI_PATH}, found {len(sections)}: "
        f"{sections}"
    )

    # Database section keys.
    assert parser.get("database", "host") == "legacy-db.internal", (
        "Unexpected value for [database] host"
    )
    assert parser.get("database", "port") == "5432", (
        "Unexpected value for [database] port"
    )

    # API section keys.
    assert parser.get("api", "endpoint") == "https://legacy-api.internal/v1", (
        "Unexpected value for [api] endpoint"
    )
    assert parser.get("api", "timeout") == "30", (
        "Unexpected value for [api] timeout"
    )

def test_migration_summary_does_not_exist_yet():
    """Ensure the summary file is absent prior to the student's commands."""
    assert not os.path.exists(SUMMARY_PATH), (
        f"{SUMMARY_PATH} should NOT exist before the migration steps begin."
    )