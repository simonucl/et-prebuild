# test_initial_state.py
#
# This test-suite validates the *initial* filesystem / OS state
# **before** the student performs any actions for the “package-versions”
# exercise.  It purposefully DOES NOT touch or test for the eventual
# output file (/home/user/pkg_scan/package_versions.log); that file
# belongs to the *solution* phase and must not influence the initial
# checks.
#
# What we verify:
#   1. The working directory /home/user/pkg_scan exists and is writable.
#   2. The input file /home/user/pkg_scan/installed_packages.txt exists,
#      is readable, and contains at least the two required package lines
#      (openssl and nmap) with the expected version strings.

import os
import stat
import re
import pytest
from pathlib import Path

PKG_SCAN_DIR = Path("/home/user/pkg_scan")
PKG_LIST_FILE = PKG_SCAN_DIR / "installed_packages.txt"

OPENSSL_VERSION_EXPECTED = "1.1.1f-1ubuntu2"
NMAP_VERSION_EXPECTED = "7.80+dfsg1-2"

REQUIRED_PACKAGES = {
    "openssl": OPENSSL_VERSION_EXPECTED,
    "nmap": NMAP_VERSION_EXPECTED,
}

@pytest.mark.describe("Filesystem setup")
def test_pkg_scan_directory_exists_and_writable():
    """The working directory must exist and be writable by the current user."""
    assert PKG_SCAN_DIR.is_dir(), (
        f"Expected directory {PKG_SCAN_DIR} to exist, but it is missing."
    )

    # Check write permission by confirming the user write bit is set OR
    # os.access with os.W_OK (handles ACLs and effective user IDs).
    is_writable = os.access(PKG_SCAN_DIR, os.W_OK)
    assert is_writable, (
        f"Directory {PKG_SCAN_DIR} exists but is not writable by the current user."
    )


@pytest.mark.describe("Input file presence")
def test_installed_packages_file_exists_and_readable():
    """The installed_packages.txt input file must exist and be readable."""
    assert PKG_LIST_FILE.is_file(), (
        f"Expected file {PKG_LIST_FILE} to exist, but it is missing."
    )

    assert os.access(PKG_LIST_FILE, os.R_OK), (
        f"File {PKG_LIST_FILE} exists but is not readable."
    )


@pytest.mark.describe("Input file contents")
def test_required_packages_present_with_expected_versions():
    """
    The input file must contain lines for 'openssl' and 'nmap'
    with the exact expected version strings.
    """
    missing_packages = set(REQUIRED_PACKAGES)
    bad_version_packages = {}

    # Regular expression to capture dpkg-like columns: status, package, version
    dpkg_line_re = re.compile(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+")

    with PKG_LIST_FILE.open("r", encoding="utf-8") as fp:
        for line in fp:
            match = dpkg_line_re.match(line)
            if not match:
                continue  # Skip lines that do not match the dpkg layout

            _status, package, version = match.groups()

            if package in missing_packages:
                expected_version = REQUIRED_PACKAGES[package]
                if version == expected_version:
                    missing_packages.discard(package)
                else:
                    bad_version_packages[package] = (expected_version, version)

    assert not missing_packages, (
        f"The following required package(s) are missing from {PKG_LIST_FILE}: "
        f"{', '.join(sorted(missing_packages))}."
    )

    assert not bad_version_packages, (
        "Version mismatch detected in installed_packages.txt:\n" +
        "\n".join(
            f"  * {pkg}: expected '{exp}', found '{found}'"
            for pkg, (exp, found) in bad_version_packages.items()
        )
    )