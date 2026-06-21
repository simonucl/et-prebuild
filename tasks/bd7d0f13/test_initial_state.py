# test_initial_state.py
#
# This test-suite validates that the operating-system is in the
# correct **initial** state before the student performs any actions.
#
# IMPORTANT:
#   • We *only* verify the pre-existing wheel repository; we do NOT
#     touch or check any of the files/directories that the student is
#     expected to create later (e.g. /home/user/buildenv or its
#     manifest file), in accordance with the task rules.
#   • All paths are absolute and platform-independent.

import os
from pathlib import Path

import pytest

# Constants ------------------------------------------------------------------

REPO_DIR = Path("/home/user/package_repo").resolve()
EXPECTED_WHEELS = {
    "colorama-0.4.6-py2.py3-none-any.whl",
    "humanfriendly-10.0-py2.py3-none-any.whl",
    "pytz-2023.3-py2.py3-none-any.whl",
}


# Helper ---------------------------------------------------------------------

def list_wheels_in_repo():
    """
    Return a set containing the filenames of all *.whl files inside
    the repository (non-recursively).
    """
    return {p.name for p in REPO_DIR.glob("*.whl") if p.is_file()}


# Tests ----------------------------------------------------------------------

def test_repository_directory_exists():
    """The local wheel repository directory must exist."""
    assert REPO_DIR.exists(), f"Expected directory {REPO_DIR} is missing."
    assert REPO_DIR.is_dir(), f"Path {REPO_DIR} exists but is not a directory."


@pytest.mark.parametrize("wheel_name", sorted(EXPECTED_WHEELS))
def test_expected_wheels_present(wheel_name):
    """
    Each expected wheel file must be present inside the repository and
    must be a non-empty regular file.
    """
    wheel_path = REPO_DIR / wheel_name
    assert wheel_path.exists(), f"Missing wheel: {wheel_path}"
    assert wheel_path.is_file(), f"Expected a file but found something else: {wheel_path}"
    size = wheel_path.stat().st_size
    assert size > 0, f"Wheel file {wheel_path} is empty (size == 0 bytes)."


def test_no_unexpected_wheels():
    """
    The repository must contain *exactly* the three expected wheels and
    nothing else. This guards against accidental extra dependencies.
    """
    present_wheels = list_wheels_in_repo()
    extra = present_wheels - EXPECTED_WHEELS
    missing = EXPECTED_WHEELS - present_wheels

    assert not missing, (
        "The following expected wheel(s) are missing from the repository:\n"
        + "\n".join(sorted(missing))
    )
    assert not extra, (
        "Found unexpected wheel file(s) in the repository (there should be none):\n"
        + "\n".join(sorted(extra))
    )