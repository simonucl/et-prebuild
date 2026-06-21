# test_initial_state.py
#
# This test-suite validates the **starting** filesystem state that must be
# present *before* the student begins their work.  It purposefully avoids
# looking for any of the files / directories that are expected **after**
# the exercise is completed.

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants describing the required initial layout
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
DOWNLOADS = HOME / "downloads"

PLACEHOLDERS = {
    "alpha-1.0.jar": 17,    # expected size in bytes
    "bravo-2.1.rpm": 18,
    "charlie-3.4.deb": 20,
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_is_file(p: Path, size: int) -> None:
    """Assert that *p* exists, is a regular file and has the given *size*."""
    assert p.exists(), f"Missing file: {p}"
    assert p.is_file(), f"Expected a regular file, but {p} is not a file."
    actual_size = p.stat().st_size
    assert (
        actual_size == size
    ), f"File {p} has size {actual_size} bytes, expected {size}."


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_downloads_directory_exists():
    """The /home/user/downloads directory must exist and be a directory."""
    assert DOWNLOADS.exists(), f"Directory {DOWNLOADS} is missing."
    assert DOWNLOADS.is_dir(), f"Path {DOWNLOADS} exists but is not a directory."


def test_placeholder_binaries_present_with_correct_size():
    """
    All three placeholder binaries must exist in /home/user/downloads and have
    the exact byte-size described in the specification.
    """
    for filename, expected_size in PLACEHOLDERS.items():
        path = DOWNLOADS / filename
        _assert_is_file(path, expected_size)


def test_no_extra_binary_artifacts_in_downloads():
    """
    There should be **exactly** the three specified binaries (and only those)
    with extensions .jar, .rpm or .deb inside /home/user/downloads.
    """
    allowed = set(PLACEHOLDERS)
    extras = [
        p.name
        for p in DOWNLOADS.iterdir()
        if p.is_file() and p.suffix in {".jar", ".rpm", ".deb"} and p.name not in allowed
    ]
    assert (
        not extras
    ), f"Unexpected binary files found in {DOWNLOADS}: {', '.join(extras)}"