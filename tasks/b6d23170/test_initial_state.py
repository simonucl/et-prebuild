# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating‐system /
# file-system **before** the student writes any solution code.
#
# The checks below guarantee that:
#   • All expected directories and INI files already exist (and only those).
#   • The content of each INI file matches the scenario description so that the
#     student will later detect the exact three mis-configurations required.
#   • The incident-logs directory as well as the final output file are **absent**
#     at this point.
#
# Only Python’s stdlib + pytest are used, and every failure message explains
# exactly what is missing or incorrect.

import os
from pathlib import Path
import configparser
import pytest

HOME = Path("/home/user")
SYSTEM_CONFIGS_DIR = HOME / "system_configs"
INCIDENT_LOGS_DIR = HOME / "incident_logs"
EXPECTED_INI_FILES = {
    SYSTEM_CONFIGS_DIR / "webapp.ini",
    SYSTEM_CONFIGS_DIR / "db.ini",
    SYSTEM_CONFIGS_DIR / "cache.ini",
}


# ---------------------------------------------------------------------------
# Basic presence / absence checks
# ---------------------------------------------------------------------------

def test_system_configs_dir_exists():
    assert SYSTEM_CONFIGS_DIR.exists(), f"Expected directory {SYSTEM_CONFIGS_DIR} does not exist."
    assert SYSTEM_CONFIGS_DIR.is_dir(), f"{SYSTEM_CONFIGS_DIR} exists but is not a directory."


def test_expected_ini_files_exist():
    """Each required INI file must exist and be a regular file."""
    for ini_path in EXPECTED_INI_FILES:
        assert ini_path.exists(), f"Required INI file {ini_path} is missing."
        assert ini_path.is_file(), f"{ini_path} exists but is not a regular file."


def test_no_extra_ini_files_present():
    """No additional .ini files should be present in /home/user/system_configs/."""
    found_ini_files = {p for p in SYSTEM_CONFIGS_DIR.glob("*.ini") if p.is_file()}
    extra_files = found_ini_files - EXPECTED_INI_FILES
    missing_files = EXPECTED_INI_FILES - found_ini_files
    assert not missing_files, f"Missing INI files: {sorted(str(p) for p in missing_files)}"
    assert not extra_files, f"Unexpected extra INI files present: {sorted(str(p) for p in extra_files)}"


def test_incident_logs_dir_absent_initially():
    """The incident_logs directory (and thus the final log file) must *not* exist yet."""
    assert not INCIDENT_LOGS_DIR.exists(), (
        f"{INCIDENT_LOGS_DIR} should not exist before the student runs their solution."
    )


# ---------------------------------------------------------------------------
# Helper to load INI files in a case-preserving, but key-insensitive manner
# ---------------------------------------------------------------------------

def _load_ini(path: Path) -> configparser.ConfigParser:
    """
    Load an INI file with:
      • section names preserved exactly
      • key names treated in a case-insensitive way (default behaviour)
    """
    cp = configparser.ConfigParser()
    with path.open("r", encoding="utf-8") as fp:
        cp.read_file(fp)
    return cp


# ---------------------------------------------------------------------------
# Content verification – make sure the files contain the *expected* settings
# that will trigger exactly three mis-configurations later on.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ini_path", sorted(EXPECTED_INI_FILES, key=str))
def test_ini_files_are_well_formed(ini_path):
    """A sanity check that each INI file can be parsed without errors."""
    try:
        _ = _load_ini(ini_path)
    except configparser.Error as exc:
        pytest.fail(f"Failed to parse {ini_path}: {exc}")


def test_webapp_ini_content():
    cp = _load_ini(SYSTEM_CONFIGS_DIR / "webapp.ini")

    # 1. [server] enable_debug = true
    assert cp.has_section("server"), "Section [server] missing in webapp.ini"
    enable_debug = cp.get("server", "enable_debug", fallback=None)
    assert enable_debug is not None, "`enable_debug` key missing in [server] section of webapp.ini"
    assert enable_debug.strip().lower() == "true", (
        "Expected enable_debug=true in webapp.ini but found "
        f"'{enable_debug}'."
    )

    # 2. [security] secret_key = abc123  (shorter than 16 chars)
    assert cp.has_section("security"), "Section [security] missing in webapp.ini"
    secret_key = cp.get("security", "secret_key", fallback=None)
    assert secret_key is not None, "`secret_key` key missing in [security] section of webapp.ini"
    assert len(secret_key) < 16, (
        "Expected a short secret_key (<16 chars) in webapp.ini to trigger "
        "a mis-configuration, but its length is >=16."
    )


def test_db_ini_content():
    cp = _load_ini(SYSTEM_CONFIGS_DIR / "db.ini")

    # 3. [database] port = 1234  (non-standard port)
    assert cp.has_section("database"), "Section [database] missing in db.ini"
    port_value = cp.get("database", "port", fallback=None)
    assert port_value is not None, "`port` key missing in [database] section of db.ini"
    assert port_value.strip() == "1234", (
        "Expected port=1234 in db.ini so the student can flag a non-standard "
        "database port, but found '{port_value}'."
    )

    # Make sure debug_mode is false so it doesn't add an extra finding
    assert cp.has_section("options"), "Section [options] missing in db.ini"
    debug_mode = cp.get("options", "debug_mode", fallback=None)
    assert debug_mode is not None, "`debug_mode` key missing in [options] section of db.ini"
    assert debug_mode.strip().lower() == "false", (
        "debug_mode in db.ini must be false initially; otherwise it would "
        "add an extra, unintended mis-configuration."
    )


def test_cache_ini_content():
    cp = _load_ini(SYSTEM_CONFIGS_DIR / "cache.ini")

    # Ensure enable_debug=false so it doesn't count as a finding
    assert cp.has_section("cache"), "Section [cache] missing in cache.ini"
    enable_debug = cp.get("cache", "enable_debug", fallback=None)
    assert enable_debug is not None, "`enable_debug` key missing in [cache] section of cache.ini"
    assert enable_debug.strip().lower() == "false", (
        "enable_debug in cache.ini must be false; otherwise it would introduce "
        "an unintended mis-configuration."
    )

    # Ensure secret_key is long enough so it's not a finding
    assert cp.has_section("auth"), "Section [auth] missing in cache.ini"
    secret_key = cp.get("auth", "secret_key", fallback=None)
    assert secret_key is not None, "`secret_key` key missing in [auth] section of cache.ini"
    assert len(secret_key) >= 16, (
        "secret_key in cache.ini should be >=16 characters so it doesn't "
        "generate a finding, but it is shorter."
    )