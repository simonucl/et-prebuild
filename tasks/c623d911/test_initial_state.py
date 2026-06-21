# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem state
BEFORE the student’s solution is run.

What we check:
1. The directory /home/user/api_configs exists and is a directory.
2. The file   /home/user/api_configs/services.ini exists and is readable.
3. The INI file contains exactly the expected three sections:
      • UserService
      • OrderService
      • InventoryService
4. Each section contains (at least) the required keys:
      • endpoint
      • token
      • timeout

We deliberately DO NOT look for any output artefacts such as
/home/user/api_summary or report.txt; those belong to the student's
solution and must not be tested here.
"""

import configparser
import pathlib
import stat
import pytest


API_CONFIG_DIR = pathlib.Path("/home/user/api_configs")
INI_PATH = API_CONFIG_DIR / "services.ini"


def test_api_config_directory_exists_and_is_directory():
    assert API_CONFIG_DIR.exists(), (
        f"Required directory does not exist: {API_CONFIG_DIR}"
    )
    assert API_CONFIG_DIR.is_dir(), (
        f"Path exists but is not a directory: {API_CONFIG_DIR}"
    )
    # Optional: ensure directory is accessible (r-x for owner at least)
    mode = API_CONFIG_DIR.stat().st_mode
    assert bool(mode & stat.S_IRUSR), (
        f"Directory {API_CONFIG_DIR} is not readable by the owner."
    )
    assert bool(mode & stat.S_IXUSR), (
        f"Directory {API_CONFIG_DIR} is not traversable by the owner."
    )


def test_services_ini_exists_and_readable():
    assert INI_PATH.exists(), f"INI file missing at expected path: {INI_PATH}"
    assert INI_PATH.is_file(), f"Path exists but is not a file: {INI_PATH}"
    # Ensure the file is readable
    mode = INI_PATH.stat().st_mode
    assert bool(mode & stat.S_IRUSR), (
        f"INI file {INI_PATH} is not readable by the owner."
    )


@pytest.fixture(scope="session")
def parsed_ini():
    """Return a ConfigParser loaded with services.ini."""
    parser = configparser.ConfigParser()
    with INI_PATH.open() as fp:
        parser.read_file(fp)
    return parser


def test_expected_sections_present(parsed_ini):
    expected_sections = {"UserService", "OrderService", "InventoryService"}
    actual_sections = set(parsed_ini.sections())

    missing = expected_sections - actual_sections
    unexpected = actual_sections - expected_sections

    assert not missing, (
        "Missing expected section(s) in services.ini: "
        + ", ".join(sorted(missing))
    )
    assert not unexpected, (
        "Unexpected extra section(s) in services.ini: "
        + ", ".join(sorted(unexpected))
    )


@pytest.mark.parametrize("section", ["UserService", "OrderService", "InventoryService"])
def test_required_keys_in_each_section(parsed_ini, section):
    required_keys = {"endpoint", "token", "timeout"}
    assert section in parsed_ini, f"Section [{section}] missing in services.ini."

    keys_in_section = set(k.lower() for k in parsed_ini[section].keys())
    missing = required_keys - keys_in_section
    assert not missing, (
        f"Section [{section}] in services.ini is missing required key(s): "
        + ", ".join(sorted(missing))
    )