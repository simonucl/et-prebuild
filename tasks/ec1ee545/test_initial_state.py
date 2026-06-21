# test_initial_state.py
#
# This pytest suite validates the INITIAL state of the workstation
# *before* the learner runs their solution code for the “pkg_overview”
# exercise.  Per the authoring rules, we deliberately do NOT check for
# the presence (or absence) of the final output directory or file
# (/home/user/docs and /home/user/docs/pkg_overview.md).  Instead, we
# confirm that the underlying prerequisites needed to *generate* that
# file are in place—namely:
#
#   1. The `dpkg-query` utility is available and executable.
#   2. The Debian/Ubuntu packages `bash`, `coreutils`, and `grep`
#      are already installed and have non-empty Version and Description
#      fields in the package database.
#
# Any failure message is written so that the learner immediately knows
# what is missing or mis-configured on the system.

import subprocess
from pathlib import Path

import pytest


PACKAGE_LIST = ["bash", "coreutils", "grep"]


def run_cmd(cmd):
    """Helper wrapper around subprocess.run that returns (rc, stdout, stderr)."""
    completed = subprocess.run(
        cmd,
        shell=False,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_dpkg_query_exists_and_works():
    """
    Ensure that `dpkg-query` is present and executable.

    The learner's solution relies on this utility to retrieve package
    metadata.  If it is missing, no further tests make sense.
    """
    dpkg_path = Path("/usr/bin/dpkg-query")
    assert dpkg_path.exists(), (
        "The utility '/usr/bin/dpkg-query' is not present. "
        "Please install the 'dpkg' package so that package metadata can be queried."
    )
    assert dpkg_path.is_file(), "'/usr/bin/dpkg-query' exists but is not a regular file."
    assert dpkg_path.stat().st_mode & 0o111, "'/usr/bin/dpkg-query' is not executable."

    # Smoke-test that the command can run at all.
    rc, out, err = run_cmd([str(dpkg_path), "--version"])
    assert rc == 0, (
        "Running 'dpkg-query --version' failed with exit code "
        f"{rc}. stderr:\n{err.strip()}"
    )
    assert "dpkg-query" in out, "Unexpected output from 'dpkg-query --version'."


@pytest.mark.parametrize("pkg_name", PACKAGE_LIST)
def test_package_is_installed_with_version_and_description(pkg_name):
    """
    For each required package, verify that:

    1. The package is _installed_ (dpkg-query exit status 0).
    2. The Version field is non-empty.
    3. The Description/Summary field is non-empty.

    The learner's Markdown output must include these exact values, so we
    validate that the system can supply them up-front.
    """
    query_cmd = [
        "/usr/bin/dpkg-query",
        "-W",
        "-f=${Version}\\t${binary:Summary}\\n",
        pkg_name,
    ]
    rc, out, err = run_cmd(query_cmd)

    assert rc == 0, (
        f"Package '{pkg_name}' does not appear to be installed "
        f"(dpkg-query exit code {rc}). stderr:\n{err.strip()}"
    )

    # dpkg-query -f format above prints "<version>\t<description>\n"
    out = out.strip()
    assert out, (
        f"dpkg-query output for package '{pkg_name}' is empty. "
        "Cannot retrieve Version and Description."
    )

    try:
        version, description = out.split("\t", 1)
    except ValueError:  # pragma: no cover
        raise AssertionError(
            f"Unexpected dpkg-query output for package '{pkg_name}': '{out}'. "
            "Expected a tab-separated 'version<TAB>description' format."
        )

    assert version.strip(), (
        f"The Version field for package '{pkg_name}' is empty. "
        "The package database seems corrupt or incomplete."
    )
    assert description.strip(), (
        f"The Description (short synopsis) for package '{pkg_name}' is empty. "
        "The package database seems corrupt or incomplete."
    )