# test_initial_state.py
#
# Pytest suite that validates the ORIGINAL state of the filesystem
# ​before​ the student carries out the localisation task.
#
# It asserts that:
#   • The expected project layout exists.
#   • Locale YAML files contain exactly the keys/values described in the
#     specification (no more, no less).
#   • build_info.toml holds the original values (build_number = 17 and
#     no last_updated key yet).
#   • The update log file does ​not​ exist yet.
#
# Only the Python standard library and pytest are used.

import re
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project-locale")
CONFIG_DIR = PROJECT_ROOT / "config"
LOCALES_DIR = CONFIG_DIR / "locales"

EN_FILE = LOCALES_DIR / "en.yaml"
ES_FILE = LOCALES_DIR / "es.yaml"
FR_FILE = LOCALES_DIR / "fr.yaml"
BUILD_INFO_FILE = CONFIG_DIR / "build_info.toml"

LOG_FILE = PROJECT_ROOT / "update_log_2023-07-01T12-00-00.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _parse_simple_yaml(path: Path) -> dict:
    """
    Very small YAML-subset parser sufficient for the files in question.
    Accepts lines in the form:   key: "value"
    Returns a dict {key: value}.
    """
    pattern = re.compile(r'^\s*([^:#\s]+)\s*:\s*"([^"]*)"\s*$')
    data = {}
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip empty & comment lines
        m = pattern.match(line)
        assert m, (
            f"{path} line {lineno!r} is not in the expected YAML format "
            f'"key: \"value\"" → {line!r}'
        )
        key, value = m.groups()
        assert key not in data, f"Duplicate key {key!r} in {path}"
        data[key] = value
    return data


def _parse_toml_subset(path: Path) -> dict:
    """
    Tiny TOML-subset parser good enough for 'key = value' pairs on their own
    lines where the value is either an integer or a quoted string.
    """
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*=\s*(.+?)\s*$')
    data = {}
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = pattern.match(line)
        assert m, f"{path} line {lineno} is not in simple TOML format → {line!r}"
        key, raw_value = m.groups()
        if raw_value.startswith('"') and raw_value.endswith('"'):
            value = raw_value.strip('"')
        else:
            # attempt integer conversion
            try:
                value = int(raw_value)
            except ValueError:
                value = raw_value
        assert key not in data, f"Duplicate key {key!r} in {path}"
        data[key] = value
    return data


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_structure_exists():
    assert PROJECT_ROOT.is_dir(), f"Missing project root directory at {PROJECT_ROOT}"
    assert CONFIG_DIR.is_dir(), f"Missing 'config' directory at {CONFIG_DIR}"
    assert LOCALES_DIR.is_dir(), f"Missing 'config/locales' directory at {LOCALES_DIR}"


def test_locale_en_initial_content():
    assert EN_FILE.is_file(), f"Missing English locale file at {EN_FILE}"
    data = _parse_simple_yaml(EN_FILE)
    expected = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "login": "Login",
        "logout": "Logout",
        "profile": "Profile",
    }
    assert data == expected, (
        f"{EN_FILE} must contain exactly the five canonical keys/values.\n"
        f"Expected: {expected}\nFound   : {data}"
    )


def test_locale_es_initial_content():
    assert ES_FILE.is_file(), f"Missing Spanish locale file at {ES_FILE}"
    data = _parse_simple_yaml(ES_FILE)
    expected_present = {
        "greeting": "Hola",
        "farewell": "Adiós",
        "login": "Iniciar sesión",
    }
    expected_missing = {"logout", "profile"}
    assert data == expected_present, (
        f"{ES_FILE} should initially contain only these three keys/values.\n"
        f"Expected: {expected_present}\nFound   : {data}"
    )
    for key in expected_missing:
        assert key not in data, f"{ES_FILE} should not yet contain the key {key!r}"


def test_locale_fr_initial_content():
    assert FR_FILE.is_file(), f"Missing French locale file at {FR_FILE}"
    data = _parse_simple_yaml(FR_FILE)
    expected_present = {
        "greeting": "Bonjour",
        "farewell": "Au revoir",
    }
    expected_missing = {"login", "logout", "profile"}
    assert data == expected_present, (
        f"{FR_FILE} should initially contain only these two keys/values.\n"
        f"Expected: {expected_present}\nFound   : {data}"
    )
    for key in expected_missing:
        assert key not in data, f"{FR_FILE} should not yet contain the key {key!r}"


def test_build_info_initial_content():
    assert BUILD_INFO_FILE.is_file(), f"Missing build info file at {BUILD_INFO_FILE}"
    data = _parse_toml_subset(BUILD_INFO_FILE)
    expected = {
        "version": "1.4.2",
        "build_number": 17,
    }
    assert data.get("version") == expected["version"], (
        f"{BUILD_INFO_FILE} 'version' should be {expected['version']!r}."
    )
    assert data.get("build_number") == expected["build_number"], (
        f"{BUILD_INFO_FILE} 'build_number' should be {expected['build_number']}."
    )
    assert "last_updated" not in data, (
        f"{BUILD_INFO_FILE} should not yet have a 'last_updated' key."
    )
    # Guard against accidental premature bump:
    assert data["build_number"] != 18, (
        f"{BUILD_INFO_FILE} build_number has already been incremented to 18; "
        "it should still be 17 at this stage."
    )


def test_update_log_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"The update log {LOG_FILE} should NOT exist before the student starts."
    )