# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the student performs any actions.  It intentionally checks ONLY the
# pre-existing inputs and never references the expected output location
# (/home/user/release/reports/…), per the project instructions.

import configparser
from pathlib import Path

import pytest

CONFIG_DIR = Path("/home/user/release/configs")

# Mapping of expected data for each INI file: {filename: {section: {key: value}}}
EXPECTED_INI_CONTENT = {
    "frontend.ini": {
        "production": {"version": "5.4.2", "port": "8080"},
        "staging": {"version": "5.4.2-rc1", "port": "8081"},
    },
    "backend.ini": {
        "production": {"version": "2.18.0", "port": "9090"},
        "staging": {"version": "2.18.0-rc1", "port": "9091"},
    },
    "worker.ini": {
        "production": {"version": "1.3.7", "port": "7070"},
        "staging": {"version": "1.3.7-rc2", "port": "7071"},
    },
}


def _read_ini(path: Path) -> configparser.ConfigParser:
    """Read an .ini file and return a ConfigParser with case-sensitive keys."""
    parser = configparser.ConfigParser()
    # Preserve case of keys
    parser.optionxform = str  # type: ignore[attr-defined]
    with path.open() as fh:
        parser.read_file(fh)
    return parser


def test_configs_directory_exists_and_is_directory():
    assert CONFIG_DIR.exists(), f"Required directory {CONFIG_DIR} is missing."
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", EXPECTED_INI_CONTENT.keys())
def test_each_expected_ini_file_exists(filename):
    ini_path = CONFIG_DIR / filename
    assert ini_path.exists(), f"Required file {ini_path} is missing."
    assert ini_path.is_file(), f"{ini_path} exists but is not a file."


@pytest.mark.parametrize(
    "filename,expected_sections", EXPECTED_INI_CONTENT.items(), ids=list(EXPECTED_INI_CONTENT)
)
def test_ini_file_contents(filename, expected_sections):
    """
    Verify that each INI file has exactly the expected sections and key/value pairs.

    The test is strict: any missing section/key or mismatched value causes failure.
    Extra sections or keys will also fail the test.
    """
    ini_path = CONFIG_DIR / filename
    parser = _read_ini(ini_path)

    # Check that the set of sections matches exactly
    expected_section_names = set(expected_sections)
    actual_section_names = set(parser.sections())
    assert (
        actual_section_names == expected_section_names
    ), f"{ini_path} sections mismatch.\nExpected: {expected_section_names}\nFound:    {actual_section_names}"

    # For each section, check keys and values
    for section, expected_kvs in expected_sections.items():
        assert parser.has_section(section), f"{ini_path} is missing section [{section}]."

        actual_kvs = dict(parser.items(section))
        expected_keys = set(expected_kvs)
        actual_keys = set(actual_kvs)

        assert (
            actual_keys == expected_keys
        ), f"{ini_path} section [{section}] keys mismatch.\nExpected keys: {expected_keys}\nFound keys:    {actual_keys}"

        for key, expected_value in expected_kvs.items():
            actual_value = actual_kvs[key]
            assert (
                actual_value == expected_value
            ), (
                f"{ini_path} [{section}] {key} value mismatch.\n"
                f"Expected: {expected_value!r}\nFound:    {actual_value!r}"
            )