# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# for the “local-only” package bundles task.  These checks must
# all pass *before* the student begins any work.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOCALPKGS = HOME / "localpkgs"

@pytest.fixture(scope="session")
def expected_packages():
    """
    Mapping of package name to its expected version string (with trailing newline).
    Only the initial, provided packages should appear here.
    """
    return {
        "bash": "5.1.16\n",
        "coreutils": "8.32\n",
    }

def test_localpkgs_directory_exists():
    """/home/user/localpkgs must exist and be a directory."""
    assert LOCALPKGS.exists(), (
        f"Expected directory {LOCALPKGS} does not exist. "
        "The initial package root is missing."
    )
    assert LOCALPKGS.is_dir(), (
        f"{LOCALPKGS} exists but is not a directory. "
        "The initial package root must be a directory."
    )

@pytest.mark.parametrize("pkg_name", ["bash", "coreutils"])
def test_package_directory_and_single_file(pkg_name):
    """
    Each package directory must exist and contain exactly one file: version.txt.
    """
    pkg_dir = LOCALPKGS / pkg_name
    assert pkg_dir.exists(), (
        f"Missing expected package directory {pkg_dir}."
    )
    assert pkg_dir.is_dir(), (
        f"{pkg_dir} exists but is not a directory."
    )

    # List directory contents (excluding hidden files just in case)
    entries = [e for e in os.listdir(pkg_dir) if not e.startswith(".")]
    assert entries == ["version.txt"], (
        f"{pkg_dir} should contain ONLY one file named 'version.txt', "
        f"but it contains: {entries}"
    )

def test_version_file_contents(expected_packages):
    """
    Verify that version.txt exists for each package and contains the
    exact expected version string ending with a newline.
    """
    for pkg_name, expected_content in expected_packages.items():
        version_file = LOCALPKGS / pkg_name / "version.txt"
        assert version_file.exists(), (
            f"Missing version.txt for package '{pkg_name}' "
            f"at expected location {version_file}."
        )
        assert version_file.is_file(), (
            f"{version_file} exists but is not a regular file."
        )

        content = version_file.read_text(encoding="utf-8")
        assert content == expected_content, (
            f"Incorrect contents in {version_file}.\n"
            f"Expected: {repr(expected_content)}\n"
            f"Found   : {repr(content)}"
        )