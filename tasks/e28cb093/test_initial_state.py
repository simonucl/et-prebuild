# test_initial_state.py
#
# This pytest suite validates that the operating-system state **before** the
# student’s work begins matches the assumptions laid out in the task
# description.  It intentionally *does not* look for the final archive that
# the student must create; it only checks the pre-existing filesystem layout.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
INCIDENT_DIR = HOME / "incidents" / "2024-06-15"
ARCHIVES_DIR = HOME / "archives"

REQUIRED_FILES = {
    "app.log",
    "sys.log",
    "readme.txt",
}


def test_incident_directory_exists():
    """The incident directory must be present and be a directory."""
    assert INCIDENT_DIR.exists(), (
        f"Expected incident directory {INCIDENT_DIR} to exist, but it does not."
    )
    assert INCIDENT_DIR.is_dir(), (
        f"Expected {INCIDENT_DIR} to be a directory, but it is not."
    )


def test_incident_directory_contents():
    """
    The incident directory must contain exactly the required plaintext files
    and absolutely nothing else.
    """
    observed = {p.name for p in INCIDENT_DIR.iterdir() if p.is_file()}
    missing = REQUIRED_FILES - observed
    extra = observed - REQUIRED_FILES

    if missing:
        pytest.fail(
            f"The following required file(s) are missing from {INCIDENT_DIR}: "
            f"{', '.join(sorted(missing))}"
        )

    if extra:
        pytest.fail(
            f"The following unexpected file(s) are present in {INCIDENT_DIR}: "
            f"{', '.join(sorted(extra))}. "
            "Directory must contain only the specified three files."
        )


@pytest.mark.parametrize("filename", sorted(REQUIRED_FILES))
def test_each_required_file_is_non_empty(filename):
    """Each required log/readme file should be a non-empty regular file."""
    path = INCIDENT_DIR / filename
    assert path.is_file(), f"Expected {path} to be a regular file."
    size = path.stat().st_size
    assert size > 0, f"File {path} exists but is empty (0 bytes)."


def test_archives_directory_exists():
    """
    The destination directory for the student's tarball must already exist.
    The test *does not* look for the tarball itself—only the directory.
    """
    assert ARCHIVES_DIR.exists(), (
        f"Expected destination directory {ARCHIVES_DIR} to exist, but it does not."
    )
    assert ARCHIVES_DIR.is_dir(), (
        f"Expected {ARCHIVES_DIR} to be a directory, but it is not."
    )