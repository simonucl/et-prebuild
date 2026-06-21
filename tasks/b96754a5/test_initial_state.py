# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the student begins the hardening task.  It verifies that:
#
# 1. The three legacy “*.old” configuration files exist with the expected
#    contents.
# 2. The required directories exist and are empty.
# 3. The hardened output files and the hardening log DO NOT yet exist.
#
# If any assertion fails the error message will explain precisely what is
# missing or unexpected.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LEGACY_DIR = HOME / "legacy_services"
HARDENED_DIR = LEGACY_DIR / "hardened"
HARDENING_DIR = HOME / "hardening"

NGINX_OLD = LEGACY_DIR / "nginx.conf.old"
SSHD_OLD = LEGACY_DIR / "sshd_config.old"
HTTPD_OLD = LEGACY_DIR / "httpd.conf.old"

NGINX_HARDENED = HARDENED_DIR / "nginx.conf"
SSHD_HARDENED = HARDENED_DIR / "sshd_config"
HTTPD_HARDENED = HARDENED_DIR / "httpd.conf"

HARDENING_LOG = HARDENING_DIR / "hardening.log"


@pytest.mark.parametrize(
    "path",
    [
        LEGACY_DIR,
        HARDENED_DIR,
        HARDENING_DIR,
    ],
)
def test_required_directories_exist(path: Path):
    assert path.is_dir(), f"Required directory “{path}” is missing."


@pytest.mark.parametrize(
    "path",
    [
        NGINX_OLD,
        SSHD_OLD,
        HTTPD_OLD,
    ],
)
def test_legacy_files_exist(path: Path):
    assert path.is_file(), f"Legacy configuration file “{path}” is missing."


def test_hardened_dir_is_empty():
    # Hardened directory must exist but be empty at the start.
    contents = [p for p in HARDENED_DIR.iterdir()]
    assert (
        len(contents) == 0
    ), f"Hardened directory “{HARDENED_DIR}” should be empty but contains: {contents}"


def test_hardening_dir_is_empty():
    # hardening/ directory must exist but contain no files (no log yet)
    contents = [p for p in HARDENING_DIR.iterdir()]
    assert (
        len(contents) == 0
    ), f"Hardening directory “{HARDENING_DIR}” should be empty but contains: {contents}"


@pytest.mark.parametrize(
    "path",
    [
        NGINX_HARDENED,
        SSHD_HARDENED,
        HTTPD_HARDENED,
        HARDENING_LOG,
    ],
)
def test_output_files_do_not_exist_yet(path: Path):
    assert (
        not path.exists()
    ), f"Output file “{path}” must not exist before the hardening process."


@pytest.mark.parametrize(
    "file_path, expected_lines",
    [
        (
            NGINX_OLD,
            [
                "user www-data;",
                "worker_processes auto;",
                "server_tokens on;",
                "ssl_protocols TLSv1 TLSv1.1 TLSv1.2;",
            ],
        ),
        (
            SSHD_OLD,
            [
                "# SSH Daemon Configuration",
                "PermitRootLogin yes",
                "PasswordAuthentication yes",
            ],
        ),
        (
            HTTPD_OLD,
            [
                "# Apache HTTPD Configuration",
                "ServerSignature On",
                "TraceEnable On",
            ],
        ),
    ],
)
def test_legacy_file_contents(file_path: Path, expected_lines):
    """
    Ensure each legacy file contains exactly the expected directive lines
    (order matters).  We ignore leading/trailing blank lines.
    """
    with file_path.open("r", encoding="utf-8") as f:
        contents = [line.rstrip("\n") for line in f.readlines()]

    # Remove any leading/trailing blank lines for comparison
    while contents and contents[0] == "":
        contents.pop(0)
    while contents and contents[-1] == "":
        contents.pop()

    assert contents == expected_lines, (
        f"Contents of “{file_path}” do not match expected initial state.\n"
        f"Expected lines:\n{expected_lines}\n\nActual lines:\n{contents}"
    )