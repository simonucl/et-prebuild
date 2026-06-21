# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / OS state
# before the student’s automation runs.  It checks that the expected
# raw INI configuration files are present and well-formed and that no
# deployment artefacts have been created yet.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import configparser
import pytest

HOME = Path("/home/user")
IOT_DIR = HOME / "iot_configs"
DEPLOY_DIR = HOME / "deployment"
EXPECTED_DEVICES = {
    "device_alpha": {
        "ip": "192.168.10.11",
        "location": "RoofTop",
        "enabled": "temp,humidity,pressure",
        "os": "TinyLinux",
        "last_maintained": "2023-05-10",
    },
    "device_beta": {
        "ip": "192.168.10.12",
        "location": "Warehouse55",
        "enabled": "temp,vibration",
        "os": "TinyLinux",
        "last_maintained": "2023-04-01",
    },
    "device_gamma": {
        "ip": "192.168.10.13",
        "location": "Dock",
        "enabled": "temp,humidity,air_quality,co2",
        "os": "TinyLinux",
        "last_maintained": "2022-12-15",
    },
}


def _load_ini(path: Path) -> configparser.ConfigParser:
    """Load an INI file case-insensitively with no interpolation."""
    cp = configparser.ConfigParser(interpolation=None)
    # ConfigParser is already case-insensitive for section & option names
    with path.open() as fh:
        cp.read_file(fh)
    return cp


def test_iot_configs_directory_exists_and_is_directory():
    assert IOT_DIR.exists(), f"Required directory {IOT_DIR} does not exist."
    assert IOT_DIR.is_dir(), f"{IOT_DIR} exists but is not a directory."


def test_exact_set_of_ini_files_present():
    present_ini_files = {p.stem for p in IOT_DIR.glob("*.ini")}
    expected_ini_files = set(EXPECTED_DEVICES.keys())
    missing = expected_ini_files - present_ini_files
    unexpected = present_ini_files - expected_ini_files
    assert not missing, (
        "The following expected INI files are missing from "
        f"{IOT_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "Unexpected INI files found in "
        f"{IOT_DIR}: {', '.join(sorted(unexpected))}"
    )


@pytest.mark.parametrize("device_id, expected_values", EXPECTED_DEVICES.items())
def test_ini_contents(device_id, expected_values):
    ini_path = IOT_DIR / f"{device_id}.ini"
    assert ini_path.exists(), f"INI file expected at {ini_path} is missing."
    cp = _load_ini(ini_path)

    # Normalise section & key access to be case-insensitive
    for section, key in [
        ("Network", "ip"),
        ("Network", "location"),
        ("Sensors", "enabled"),
        ("System", "os"),
        ("System", "last_maintained"),
    ]:
        assert cp.has_section(section), (
            f"{ini_path}: expected section [{section}] is missing."
        )
        assert cp.has_option(section, key), (
            f"{ini_path}: expected key '{key}' (case-insensitive) "
            f"missing in section [{section}]."
        )
        value = cp.get(section, key, fallback="").strip()
        assert value, (
            f"{ini_path}: key '{key}' in section [{section}] is present "
            "but empty."
        )
        # Verify the value matches the ground-truth declared above so tests
        # fail if the initial dataset has been changed.
        expected_value = expected_values[key]
        assert value == expected_value, (
            f"{ini_path}: key '{key}' expected to be '{expected_value}' "
            f"but found '{value}'."
        )


def test_deployment_directory_absent_initially():
    assert not DEPLOY_DIR.exists(), (
        f"{DEPLOY_DIR} should NOT exist before the deployment script runs."
    )
    # Even if someone manually created the directory, ensure that it is empty
    # and contains none of the expected artefacts.
    if DEPLOY_DIR.exists():
        assert not (DEPLOY_DIR / "device_report.csv").exists(), (
            f"{DEPLOY_DIR}/device_report.csv should not exist before the "
            "deployment script runs."
        )
        assert not (DEPLOY_DIR / "validation.log").exists(), (
            f"{DEPLOY_DIR}/validation.log should not exist before the "
            "deployment script runs."
        )