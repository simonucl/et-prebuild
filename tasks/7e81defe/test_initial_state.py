# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state before the student’s solution runs.

import os
from pathlib import Path

# Absolute paths used throughout the assignment
PKG_INVENTORY = Path("/home/user/repo/package_inventory.csv")
INSTALLED_PKGS = Path("/home/user/installed/installed_packages.txt")
ALERTS_DIR = Path("/home/user/alerts")
ALERT_LOG = ALERTS_DIR / "monitoring_pkg_alerts.log"
ALERT_LOG_GZ = ALERTS_DIR / "monitoring_pkg_alerts.log.gz"


def read_file_lines(path: Path):
    """
    Read file using binary mode to *guarantee* UNIX line endings only.
    Returns a list of decoded lines without their trailing newline.
    """
    with path.open("rb") as fh:
        data = fh.read()
    assert b"\r" not in data, (
        f"{path} contains Windows (CRLF) line endings; "
        "file must use UNIX LF line endings only."
    )
    text = data.decode("utf-8")
    return text.splitlines()  # removes the \n characters


def test_package_inventory_file_exists_and_contents():
    """Verify /home/user/repo/package_inventory.csv exists and has exact contents."""
    assert PKG_INVENTORY.is_file(), (
        f"Required inventory file missing: {PKG_INVENTORY}"
    )

    expected_lines = [
        "htop,3.2.2",
        "sysstat,12.5.4",
        "iftop,1.0pre4",
        "net-tools,2.10",
        "glances,3.3.0",
    ]
    actual_lines = read_file_lines(PKG_INVENTORY)

    assert actual_lines == expected_lines, (
        f"Unexpected contents in {PKG_INVENTORY}.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}"
    )


def test_installed_packages_file_exists_and_contents():
    """Verify /home/user/installed/installed_packages.txt exists and has exact contents."""
    assert INSTALLED_PKGS.is_file(), (
        f"Required installed-package file missing: {INSTALLED_PKGS}"
    )

    expected_lines = [
        "bash,5.0",
        "coreutils,8.30",
        "glances,3.3.0",
    ]
    actual_lines = read_file_lines(INSTALLED_PKGS)

    assert actual_lines == expected_lines, (
        f"Unexpected contents in {INSTALLED_PKGS}.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}"
    )


def test_alerts_directory_does_not_exist_yet():
    """
    The /home/user/alerts directory (and any expected artefacts inside it)
    must NOT exist before the student’s solution runs.
    """
    assert not ALERTS_DIR.exists(), (
        f"{ALERTS_DIR} should NOT exist at the start of the task, "
        "but it does."
    )
    # Sanity check: if someone accidentally created one of the output files
    # elsewhere, fail loudly so the initial state stays clean.
    assert not ALERT_LOG.exists(), (
        f"Output log {ALERT_LOG} should not exist before the task is performed."
    )
    assert not ALERT_LOG_GZ.exists(), (
        f"Gzipped log {ALERT_LOG_GZ} should not exist before the task is performed."
    )