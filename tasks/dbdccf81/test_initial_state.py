# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the system *before* the
# student performs any actions for the “routine integrity-audit” task.
#
# What we check:
#   • The user’s home directory (/home/user) is present.
#   • No audit log matching  /home/user/audit/pkg_audit_????????.log
#     is found (the student hasn’t created it yet).
#   • The packages that must be audited (coreutils, tar, gzip) are
#     installed and have non-empty version strings retrievable via
#     `dpkg-query`.
#   • The target file whose checksum will be required
#     (/etc/apt/sources.list) exists.
#
# We purposely do NOT check for the presence of /home/user/audit itself;
# the task allows for it to be either absent (needs creation) or already
# present.  We only insist that the definitive audit file is *not* there
# yet, guaranteeing the exercise hasn’t been completed in advance.

import subprocess
from pathlib import Path
import glob
import pytest


HOME_DIR = Path("/home/user")
AUDIT_DIR = HOME_DIR / "audit"
AUDIT_GLOB_PATTERN = str(AUDIT_DIR / "pkg_audit_????????.log")
REQUIRED_PACKAGES = ("coreutils", "tar", "gzip")
APT_SOURCES = Path("/etc/apt/sources.list")


def _dpkg_query(package: str, query_format: str = "${Version}") -> str:
    """
    Helper that wraps `dpkg-query`.

    Returns the raw stdout as a string and raises pytest.fail with a clear
    message if the command cannot be executed or the package is not found.
    """
    try:
        completed = subprocess.run(
            ["dpkg-query", "-W", f"-f={query_format}", package],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        pytest.fail(
            "dpkg-query command is not available on this system; "
            "cannot verify required packages."
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Package '{package}' is not installed or dpkg-query failed:\n{exc.stderr}"
        )
    return completed.stdout.strip()


def test_home_directory_exists():
    assert HOME_DIR.is_dir(), f"Expected home directory {HOME_DIR} to exist."


def test_audit_log_not_present_yet():
    """
    There must be *no* file that matches the grader’s filename pattern.
    A premature presence would indicate the student has already performed
    the task, so the initial-state test should fail.
    """
    matches = glob.glob(AUDIT_GLOB_PATTERN)
    assert (
        len(matches) == 0
    ), (
        "Found audit log(s) that should not exist yet:\n"
        f"  {', '.join(matches)}\n"
        "Please remove or rename them before starting the exercise."
    )


@pytest.mark.parametrize("package_name", REQUIRED_PACKAGES)
def test_required_packages_installed(package_name):
    """
    Confirms that each required package is installed and that its
    version string is non-empty.
    """
    version = _dpkg_query(package_name, "${Version}")
    assert version, (
        f"dpkg-query returned an empty version string for package "
        f"'{package_name}'. The package may not be installed correctly."
    )


def test_apt_sources_list_exists():
    assert APT_SOURCES.is_file(), (
        f"Expected {APT_SOURCES} to exist so its SHA-256 digest can be "
        "recorded during the audit."
    )