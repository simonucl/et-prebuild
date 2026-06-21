# test_initial_state.py
#
# Pytest suite to verify the *initial* filesystem state BEFORE the student
# carries out any repository-curation work.  These tests make sure the
# starting fixture is present exactly as described in the assignment:
#
#   • Only /home/user/incoming/ exists (besides /home/user itself).
#   • That directory contains exactly three zero-byte files with the precise
#     filenames supplied in the specification.
#   • No repository tree (/home/user/repositories) has been created yet.
#
# Any failure message pin-points the missing, extra or malformed element so
# that the learner can immediately see what is wrong with the fixture.
#
# NOTE:  This file **must run before** the learner’s solution, so it must NOT
#        look for any output artefacts (manifest.csv, activity.log, etc.).
#        It checks *only* the initial state.

from pathlib import Path
import stat

import pytest


# Constants for paths and expected filenames
HOME = Path("/home/user")
INCOMING = HOME / "incoming"
REPOSITORIES = HOME / "repositories"

EXPECTED_FILES = {
    "app-1.0.0-linux-amd64.tar.gz",
    "plugin-2.3.4.zip",
    "agent.v1.5.1.bin",
}


def test_incoming_directory_exists_and_is_directory():
    assert INCOMING.exists(), f"Expected directory {INCOMING} to exist."
    assert INCOMING.is_dir(), f"{INCOMING} exists but is not a directory."


def test_incoming_has_exactly_three_expected_files():
    present = {p.name for p in INCOMING.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - present
    extra = present - EXPECTED_FILES

    assert not missing, (
        "The following expected files are missing from "
        f"{INCOMING}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"The directory {INCOMING} contains unexpected files: "
        f"{', '.join(sorted(extra))}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_each_expected_file_is_zero_bytes_and_regular(filename):
    path = INCOMING / filename
    assert path.is_file(), f"Expected file {path} to exist."
    size = path.stat().st_size
    assert size == 0, f"Expected {path} to be zero bytes, found {size} bytes."
    # Sanity-check that it is a regular file (not symlink, device, etc.)
    mode = path.stat().st_mode
    assert stat.S_ISREG(mode), f"{path} is not a regular file."


def test_no_repository_tree_yet():
    """
    Before the learner runs their solution, /home/user/repositories should
    not exist.  If it exists already, the fixture is corrupt.
    """
    assert not REPOSITORIES.exists(), (
        f"Found {REPOSITORIES} in the initial fixture, but it should **not** "
        "exist before any actions are taken."
    )