# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student performs any action.  It deliberately
# avoids testing for the eventual output file `config_checksums.txt`.
#
# What is verified:
#   1. The directory /home/user/device_configs exists.
#   2. The sub-directories site_a/ and site_b/ exist.
#   3. Exactly three “.cfg” files are present, no more and no fewer.
#   4. Each of the three files contains the exact, line-by-line text
#      described in the task specification.

import hashlib
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/device_configs")

# Relative paths -> expected full textual content (including the final “\n”)
EXPECTED_FILES = {
    "site_a/gateway.cfg": (
        "gateway_id=GW-001\n"
        "ip_address=192.168.1.1\n"
        "port=1883\n"
    ),
    "site_a/sensor1.cfg": (
        "sensor_id=S-100\n"
        "frequency=30\n"
        "unit=celsius\n"
    ),
    "site_b/sensor2.cfg": (
        "sensor_id=S-200\n"
        "frequency=15\n"
        "unit=humidity\n"
    ),
}


def test_base_directory_exists():
    """The top-level directory must be present."""
    assert BASE_DIR.is_dir(), f"Required directory {BASE_DIR} is missing."


@pytest.mark.parametrize("relative_path", EXPECTED_FILES.keys())
def test_each_cfg_file_exists(relative_path):
    """Every expected .cfg file must exist."""
    full_path = BASE_DIR / relative_path
    assert full_path.is_file(), f"Expected file {full_path} is missing."


def test_no_extra_or_missing_cfg_files():
    """Exactly the three .cfg files described in the spec must be present."""
    found_cfgs = sorted(str(p.relative_to(BASE_DIR)) for p in BASE_DIR.rglob("*.cfg"))
    expected_cfgs = sorted(EXPECTED_FILES.keys())
    assert (
        found_cfgs == expected_cfgs
    ), f"Unexpected set of .cfg files.\nExpected: {expected_cfgs}\nFound:    {found_cfgs}"


@pytest.mark.parametrize("relative_path,expected_text", EXPECTED_FILES.items())
def test_cfg_file_contents(relative_path, expected_text):
    """
    The contents of each configuration file must match the
    exact text (including terminal newlines) given in the task description.
    """
    full_path = BASE_DIR / relative_path
    actual_text = full_path.read_text(encoding="utf-8")
    assert (
        actual_text == expected_text
    ), f"Contents of {full_path} differ from expectation."


def test_md5_sanity():
    """
    As an additional guard, verify that the MD5 digests of the three
    files are distinct—this helps catch accidental duplication.
    """
    digests = []
    for rel_path in EXPECTED_FILES:
        data = (BASE_DIR / rel_path).read_bytes()
        digest = hashlib.md5(data).hexdigest()
        digests.append(digest)

    assert len(digests) == len(set(digests)), (
        "MD5 digests for the configuration files are not unique; "
        "there may be duplicate or incorrect file contents."
    )