# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state required for the “Python package environment backup” assignment.
#
# These tests are meant to be executed *before* the student performs any
# actions.  They assert that all prerequisite files, directories and archives
# are already present and correct.  Any failure message pinpoints exactly what
# is missing or malformed.
#
# NOTE:  Only the Python standard library and pytest are used.

import os
import tarfile
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# General constants                                                           #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
ENV_DIR = HOME / "envs" / "archive_admin"
REQ_FILE = ENV_DIR / "requirements.txt"
LOG_FILE = HOME / "backup_logs" / "package_inventory.log"
TAR_FILE = HOME / "archives" / "pip_backup.tgz"

# Exact, byte-for-byte expected contents
EXPECTED_REQ_CONTENT = b"pandas==2.0.3\nrequests==2.31.0\n"
EXPECTED_LOG_CONTENT = b"PACKAGE,VERSION\npandas,2.0.3\nrequests,2.31.0\n"


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _discover_site_packages(env_root: Path) -> Path:
    """
    Best-effort discovery of the virtual-environment's site-packages directory.

    Returns
    -------
    Path
        The discovered site-packages directory.

    Raises
    ------
    FileNotFoundError
        If no suitable site-packages directory could be found.
    """
    lib_dir = env_root / "lib"
    if not lib_dir.is_dir():
        raise FileNotFoundError(
            f"Expected '{lib_dir}' to exist inside virtual environment."
        )

    # Typical layout: lib/python3.x/site-packages
    for pyver_dir in lib_dir.iterdir():
        sp_dir = pyver_dir / "site-packages"
        if sp_dir.is_dir():
            return sp_dir

    raise FileNotFoundError(
        f"No site-packages directory found beneath '{lib_dir}'."
    )


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_virtualenv_directory_exists_and_is_valid():
    assert ENV_DIR.is_dir(), (
        f"Virtual-environment directory '{ENV_DIR}' is missing. "
        "It must already exist before running the assignment."
    )

    cfg_file = ENV_DIR / "pyvenv.cfg"
    assert cfg_file.is_file(), (
        f"Virtual-environment config file '{cfg_file}' is missing. "
        "A valid virtualenv must include this file."
    )


def test_packages_installed_inside_site_packages():
    site_packages = _discover_site_packages(ENV_DIR)

    for pkg in ("pandas", "requests"):
        pkg_path = site_packages / pkg
        assert pkg_path.exists(), (
            f"Package directory '{pkg_path}' not found in site-packages. "
            "Both 'pandas' and 'requests' must be installed in the "
            "virtual environment."
        )
        assert pkg_path.is_dir(), f"Expected '{pkg_path}' to be a directory."


def test_requirements_txt_exact_content():
    assert REQ_FILE.is_file(), f"Requirements file '{REQ_FILE}' is missing."
    content = REQ_FILE.read_bytes()
    assert (
        content == EXPECTED_REQ_CONTENT
    ), (
        f"File '{REQ_FILE}' contents differ from the required two-line file.\n"
        "Expected exactly:\n"
        f"{EXPECTED_REQ_CONTENT.decode()!r}\nGot:\n{content.decode()!r}"
    )


def test_package_inventory_log_exact_content():
    assert LOG_FILE.is_file(), f"Inventory log '{LOG_FILE}' is missing."
    content = LOG_FILE.read_bytes()
    assert (
        content == EXPECTED_LOG_CONTENT
    ), (
        f"File '{LOG_FILE}' contents differ from the required three-line CSV.\n"
        "Expected exactly:\n"
        f"{EXPECTED_LOG_CONTENT.decode()!r}\nGot:\n{content.decode()!r}"
    )


def test_backup_tarball_exists_and_contains_expected_entries(tmp_path):
    # Use tmp_path to extract the tar safely if necessary
    assert TAR_FILE.is_file(), f"Backup archive '{TAR_FILE}' is missing."
    assert TAR_FILE.stat().st_size > 0, f"Backup archive '{TAR_FILE}' is empty."

    required_entries = {
        "envs/archive_admin/pyvenv.cfg",
        "backup_logs/package_inventory.log",
    }

    with tarfile.open(TAR_FILE, "r:gz") as tar:
        names = set(tar.getnames())

    missing = required_entries - names
    assert (
        not missing
    ), (
        f"Backup archive '{TAR_FILE}' is missing the following entries: "
        f"{', '.join(sorted(missing))}.  The archive must store paths "
        "relative to '/home/user'."
    )