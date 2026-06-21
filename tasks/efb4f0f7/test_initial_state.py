# test_initial_state.py
#
# This pytest suite validates that the **initial** operating-system / file-system
# state matches what the assignment promises *before* the student performs any
# work.  It purposely avoids checking for artefacts that the student is
# expected to create later (virtual-environment, scripts, reports, etc.).

import os
from pathlib import Path

import pytest

# Absolute base paths used throughout the assignment
NETWORK_DUMPS_DIR = Path("/home/user/network_dumps")
NETLOGS_DIR = Path("/home/user/netlogs")

# Mapping of expected ping-dump files to a marker string that must be present
PING_FILES = {
    NETWORK_DUMPS_DIR / "ping_8.8.8.8.log": "8.8.8.8",
    NETWORK_DUMPS_DIR / "ping_1.1.1.1.log": "1.1.1.1",
    NETWORK_DUMPS_DIR / "ping_example.com.log": "example.com",
}


def _read_text(path: Path) -> str:
    """Helper that reads a file and returns its text, raising with context on failure."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Failed to read {path}: {exc}")  # noqa: B011


def test_network_dumps_directory_exists():
    """The directory that holds the supplied ping dumps must exist."""
    assert NETWORK_DUMPS_DIR.is_dir(), (
        f"Expected directory {NETWORK_DUMPS_DIR} to exist, "
        "but it is missing. The initial ping-dump directory must be present."
    )


@pytest.mark.parametrize("file_path,needle", list(PING_FILES.items()))
def test_ping_dump_files_exist_with_expected_content(file_path: Path, needle: str):
    """
    Each required ping dump file must:
    1. Exist as a regular file.
    2. Be readable and non-empty.
    3. Contain an identifying string (IP / hostname) so we know the correct
       dataset is in place.
    """
    assert file_path.is_file(), f"Expected file {file_path} to exist, but it is missing."

    text = _read_text(file_path)
    assert text.strip(), f"{file_path} is empty; it should contain ping output."
    assert needle in text, (
        f"{file_path} does not contain the expected string '{needle}'. "
        "The file contents appear to be incorrect."
    )


def test_netlogs_directory_exists():
    """
    The directory where the student will later write their connectivity
    report must already exist (it may be empty at this point).
    """
    assert NETLOGS_DIR.is_dir(), (
        f"Expected directory {NETLOGS_DIR} to exist, "
        "but it is missing. Please ensure the initial log directory is present."
    )