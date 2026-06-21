# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the
student performs any action for the “router checksum verification” exercise.

What we assert:
1. /home/user/network_configs exists and is a directory.
2. /home/user/network_configs/router.cfg exists, is a regular file and
   its content exactly matches the reference shown in the task
   description (including the final newline).
3. /home/user/network_configs/router.cfg.sha256 exists, is a regular file,
   contains exactly one 64-character lower-case hexadecimal string plus a
   single trailing newline, and that hash matches the true SHA-256 of
   router.cfg.

We deliberately do **not** test for any output artefacts such as
/home/user/verify_logs or checksum_verification.log – those belong to the
student’s solution and are verified elsewhere.
"""

import hashlib
import os
import stat
import string
import pytest

# Absolute paths used throughout the tests
CONFIG_DIR = "/home/user/network_configs"
CONFIG_FILE = os.path.join(CONFIG_DIR, "router.cfg")
SHA_FILE = os.path.join(CONFIG_DIR, "router.cfg.sha256")

# Expected exact content of router.cfg (UNIX LF line endings), including
# the final newline.
EXPECTED_CONFIG_CONTENT = (
    "!\n"
    "version 15.2\n"
    "hostname TestRouter\n"
    "interface GigabitEthernet0/0\n"
    " ip address 192.168.1.1 255.255.255.0\n"
    " no shutdown\n"
    "!\n"
    "end\n"
)


def _is_regular_file(path: str) -> bool:
    """Return True if path exists and is a regular file."""
    try:
        mode = os.stat(path, follow_symlinks=True).st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode)


def test_network_configs_directory_exists():
    assert os.path.isdir(
        CONFIG_DIR
    ), f"Required directory {CONFIG_DIR!r} does not exist or is not a directory."


def test_router_cfg_exists_and_matches_expected_content():
    assert _is_regular_file(
        CONFIG_FILE
    ), f"Expected configuration file {CONFIG_FILE!r} is missing or not a regular file."

    with open(CONFIG_FILE, "r", encoding="utf-8", newline="") as fh:
        actual_content = fh.read()

    assert (
        actual_content == EXPECTED_CONFIG_CONTENT
    ), (
        f"Content of {CONFIG_FILE!r} does not match the expected reference "
        "provided in the task description."
    )


def test_sha256_file_exists_has_single_line_and_matches_router_cfg():
    assert _is_regular_file(
        SHA_FILE
    ), f"SHA-256 reference file {SHA_FILE!r} is missing or not a regular file."

    with open(SHA_FILE, "r", encoding="utf-8", newline="") as fh:
        sha_file_content = fh.read()

    # The file must end with exactly one newline and nothing else.
    assert sha_file_content.endswith(
        "\n"
    ), f"{SHA_FILE!r} must end with a single newline."
    # Strip the final newline to get the actual hash string.
    hash_line = sha_file_content[:-1]

    # Assert exactly one non-empty line of 64 lower-case hex digits.
    assert (
        len(hash_line) == 64
    ), f"{SHA_FILE!r} must contain exactly 64 hexadecimal characters (found {len(hash_line)})."
    valid_hex_digits = set(string.hexdigits.lower())
    assert set(hash_line).issubset(
        valid_hex_digits
    ), f"{SHA_FILE!r} contains invalid non-hexadecimal characters."
    assert hash_line == hash_line.lower(), f"{SHA_FILE!r} must use lower-case hexadecimal."

    # Compute actual SHA-256 of the config file and compare.
    with open(CONFIG_FILE, "rb") as cf:
        data = cf.read()
    actual_digest = hashlib.sha256(data).hexdigest()

    assert (
        actual_digest == hash_line
    ), (
        f"The SHA-256 stored in {SHA_FILE!r} does not match the true "
        f"checksum of {CONFIG_FILE!r}.\nExpected: {hash_line}\nActual:   {actual_digest}"
    )