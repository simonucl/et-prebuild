# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating system /
filesystem before the student’s solution is executed.

The checks deliberately focus on what must already be present **before**
any work is done:

1. Required directories exist, are writable by the current user and (where
   applicable) are empty.
2. Exactly two ini files are present in /home/user/configs/ and no others.
3. Both ini files match the expected structure and numeric values.

If any check fails, the corresponding assertion message explains precisely
what is missing or unexpected so that the student can correct the starting
state before continuing with the task.
"""
import os
import stat
import configparser
import pytest
from pathlib import Path

HOME = Path("/home/user")
CONFIG_DIR = HOME / "configs"
BIN_DIR = HOME / "bin"
REPORTS_DIR = HOME / "reports"

# ---------- helpers ---------- #
def is_writable(path: Path) -> bool:
    """Return True if the current user has write permission on *path*."""
    return os.access(path, os.W_OK)


def read_ini(path: Path) -> configparser.ConfigParser:
    """Read an INI file and return a ConfigParser object."""
    parser = configparser.ConfigParser()
    read = parser.read(path)
    if not read:
        pytest.fail(f"Failed to read INI file {path}")
    return parser


# ---------- expected values ---------- #
EXPECTED_INIS = {
    "appA.ini": {
        "meta": {"name": "Application Alpha", "version": "1.2.3"},
        "cpu": {"threshold": "75", "limit": "90"},
        "memory": {"threshold": "1024", "limit": "2048"},
        "io": {"threshold": "120", "limit": "150"},
    },
    "appB.ini": {
        "meta": {"name": "Beta Service", "version": "4.5.6"},
        "cpu": {"threshold": "85", "limit": "80"},
        "memory": {"threshold": "1500", "limit": "1400"},
        "io": {"threshold": "100", "limit": "200"},
    },
}


# ---------- tests ---------- #
def test_directories_exist_and_empty():
    """The expected directories must exist, be writable and (where required) empty."""
    for directory in (CONFIG_DIR, BIN_DIR, REPORTS_DIR):
        assert directory.is_dir(), f"Missing directory: {directory}"
        assert is_writable(directory), f"Directory not writable: {directory}"

    # /home/user/bin/ must be empty
    bin_contents = list(BIN_DIR.iterdir())
    assert (
        len(bin_contents) == 0
    ), f"{BIN_DIR} is expected to be empty but contains: {[p.name for p in bin_contents]}"

    # /home/user/reports/ must be empty
    reports_contents = list(REPORTS_DIR.iterdir())
    assert (
        len(reports_contents) == 0
    ), f"{REPORTS_DIR} is expected to be empty but contains: {[p.name for p in reports_contents]}"


def test_ini_files_present_and_only_those():
    """Exactly two INI files (appA.ini and appB.ini) must be present."""
    ini_files = sorted(p.name for p in CONFIG_DIR.glob("*.ini"))
    expected_files = sorted(EXPECTED_INIS.keys())
    assert (
        ini_files == expected_files
    ), f"Expected INI files {expected_files} but found {ini_files}"


@pytest.mark.parametrize("ini_name, expected_sections", EXPECTED_INIS.items())
def test_ini_file_content(ini_name, expected_sections):
    """Each INI file must contain the expected sections and key/value pairs."""
    ini_path = CONFIG_DIR / ini_name
    assert ini_path.is_file(), f"Missing INI file: {ini_path}"

    parser = read_ini(ini_path)

    # Sections check
    expected_section_names = set(expected_sections.keys())
    actual_section_names = set(parser.sections())
    assert (
        expected_section_names == actual_section_names
    ), f"{ini_name}: Expected sections {sorted(expected_section_names)} but found {sorted(actual_section_names)}"

    # Key/value checks per section
    for section, expected_kv in expected_sections.items():
        for key, expected_value in expected_kv.items():
            assert parser.has_option(
                section, key
            ), f"{ini_name}: Missing key '{key}' in section [{section}]"
            actual_value = parser.get(section, key)
            assert (
                actual_value == expected_value
            ), (
                f"{ini_name}: Expected {section}.{key} = {expected_value} "
                f"but found {actual_value}"
            )

    # Numeric sanity for threshold/limit keys
    for section in ("cpu", "memory", "io"):
        for numeric_key in ("threshold", "limit"):
            value_str = parser.get(section, numeric_key)
            assert value_str.isdigit(), (
                f"{ini_name}: Value for {numeric_key} in section [{section}] "
                f"must be an integer, got '{value_str}'"
            )