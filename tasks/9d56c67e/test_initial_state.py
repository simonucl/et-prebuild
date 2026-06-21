# test_initial_state.py
#
# Pytest suite that validates the pristine on-disk state **before** the student
# starts working on the “vulnscan” hardening task.
#
# Checked items (all must already be true):
#   • /home/user/vulnscan        → exists and is a directory
#   • /home/user/vulnscan/services.conf
#   • /home/user/vulnscan/services.conf.fixed
#   • /home/user/vulnscan/patches (directory)
#
#   The two *.conf files must match the exact baseline content supplied by the
#   grading instructions and must *differ* from one another (the task is to
#   patch the former so it becomes identical to the latter).
#
# NOTE: The tests deliberately do *not* look for any of the artefacts that the
#       student is expected to create (patches/services_services.patch,
#       patches/patch_log.txt, etc.), in accordance with the problem statement.

import os
import hashlib
import pytest

BASE_DIR = "/home/user/vulnscan"
PATCHES_DIR = os.path.join(BASE_DIR, "patches")
SERVICES_CONF = os.path.join(BASE_DIR, "services.conf")
SERVICES_CONF_FIXED = os.path.join(BASE_DIR, "services.conf.fixed")

# Expected file contents with trailing newline kept intentionally.
EXPECTED_SERVICES_CONF = (
    "# Service configuration\n"
    "ssh: enabled\n"
    "telnet: enabled\n"
    "ftp: enabled\n"
    "http: enabled\n"
    "https: disabled\n"
    "snmp: enabled\n"
    "# End of file\n"
)

EXPECTED_SERVICES_CONF_FIXED = (
    "# Service configuration\n"
    "ssh: enabled\n"
    "telnet: disabled\n"
    "ftp: disabled\n"
    "http: enabled\n"
    "https: enabled\n"
    "snmp: disabled\n"
    "# End of file\n"
)


def _read_file(path: str) -> str:
    """Read a text file exactly as-is (binary → utf-8)."""
    with open(path, "rb") as fh:
        data = fh.read()
    # Decode with strict errors; the files are plain ascii/utf-8.
    return data.decode("utf-8")


def test_base_directory_exists():
    assert os.path.isdir(BASE_DIR), (
        f"Required directory {BASE_DIR!r} is missing. "
        "The initial workspace must already exist."
    )


def test_patches_directory_exists():
    assert os.path.isdir(PATCHES_DIR), (
        f"Required directory {PATCHES_DIR!r} is missing. "
        "It should be pre-created and writable."
    )


@pytest.mark.parametrize(
    "path, description",
    [
        (SERVICES_CONF, "current (vulnerable) live configuration"),
        (SERVICES_CONF_FIXED, "hardened reference configuration"),
    ],
)
def test_conf_files_exist(path, description):
    assert os.path.isfile(path), f"The {description} file {path!r} is missing."


def test_services_conf_content_is_exact():
    content = _read_file(SERVICES_CONF)
    assert content == EXPECTED_SERVICES_CONF, (
        f"{SERVICES_CONF} does not match the expected baseline content.\n"
        "Ensure the initial file has not been modified before patching."
    )


def test_services_conf_fixed_content_is_exact():
    content = _read_file(SERVICES_CONF_FIXED)
    assert content == EXPECTED_SERVICES_CONF_FIXED, (
        f"{SERVICES_CONF_FIXED} does not match the expected baseline content.\n"
        "The reference file must remain unaltered."
    )


def test_conf_files_are_different():
    live = _read_file(SERVICES_CONF)
    fixed = _read_file(SERVICES_CONF_FIXED)
    assert live != fixed, (
        "The live configuration already matches the hardened version. "
        "Nothing would remain to patch, which contradicts the task setup."
    )


def test_initial_md5_is_different():
    """Optional sanity check: MD5 sums of the two files should differ."""
    live_md5 = hashlib.md5(_read_file(SERVICES_CONF).encode()).hexdigest()
    fixed_md5 = hashlib.md5(_read_file(SERVICES_CONF_FIXED).encode()).hexdigest()
    assert live_md5 != fixed_md5, (
        "MD5 checksums of services.conf and services.conf.fixed are equal, "
        "but they should differ prior to patching."
    )