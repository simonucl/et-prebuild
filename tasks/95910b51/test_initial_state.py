# test_initial_state.py
"""
Pytest suite that verifies the initial filesystem state *before* the student
runs their migration script.

The checks performed here intentionally avoid looking for any artefacts the
student is expected to create (e.g. the tar-gz archive, the restored copies,
or the migration log).  Only the pre-existing directories and source config
files are validated.
"""

from pathlib import Path
import pytest


# ---------------------------------------------------------------------------
# Constants describing the expected initial layout and file contents
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
MIGRATION_DIR = HOME / "migration"

SOURCE_DIR = MIGRATION_DIR / "source_configs"
ARCHIVES_DIR = MIGRATION_DIR / "archives"
RESTORE_DIR = MIGRATION_DIR / "restore"

EXPECTED_SOURCE_FILES = {
    "config1.conf": "server_name=alpha\nport=8080\n",
    "config2.conf": "server_name=beta\nport=9090\n",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def read_text(path: Path) -> str:
    """
    Read text from *path* using UTF-8 encoding, ensuring the file can be
    opened and read in one go.  Any I/O error will naturally fail the test.
    """
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_source_directory_exists_and_is_correct():
    """
    The directory /home/user/migration/source_configs must exist, be a
    directory, and contain exactly the two expected configuration files—
    nothing more, nothing less.
    """
    assert SOURCE_DIR.exists(), (
        f"Required directory {SOURCE_DIR} does not exist."
    )
    assert SOURCE_DIR.is_dir(), (
        f"{SOURCE_DIR} exists but is not a directory."
    )

    # Collect all *files* in the directory (ignore sub-directories, if any)
    present_files = {p.name for p in SOURCE_DIR.iterdir() if p.is_file()}

    assert present_files == set(EXPECTED_SOURCE_FILES), (
        "The source configuration directory must contain exactly "
        f"{sorted(EXPECTED_SOURCE_FILES)} but currently contains "
        f"{sorted(present_files)}."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_SOURCE_FILES.items())
def test_source_file_contents(filename, expected_content):
    """
    Each source configuration file must have the exact expected content.
    """
    file_path = SOURCE_DIR / filename
    assert file_path.is_file(), (
        f"Expected file {file_path} is missing."
    )

    actual_content = read_text(file_path)
    assert actual_content == expected_content, (
        f"Content mismatch in {file_path}.\n"
        "Expected:\n"
        f"{expected_content!r}\n"
        "Found:\n"
        f"{actual_content!r}"
    )


def test_archives_directory_exists_and_is_empty():
    """
    The directory /home/user/migration/archives must exist *and* be empty at
    the outset.  The student will later place the tarball here.
    """
    assert ARCHIVES_DIR.exists(), (
        f"Required directory {ARCHIVES_DIR} does not exist."
    )
    assert ARCHIVES_DIR.is_dir(), (
        f"{ARCHIVES_DIR} exists but is not a directory."
    )

    contents = list(ARCHIVES_DIR.iterdir())
    assert not contents, (
        f"{ARCHIVES_DIR} should be empty initially, but contains: "
        f"{[str(p) for p in contents]}"
    )


def test_restore_directory_exists_and_is_empty():
    """
    The directory /home/user/migration/restore must exist and be empty before
    extraction.  The student's script will later populate it.
    """
    assert RESTORE_DIR.exists(), (
        f"Required directory {RESTORE_DIR} does not exist."
    )
    assert RESTORE_DIR.is_dir(), (
        f"{RESTORE_DIR} exists but is not a directory."
    )

    contents = list(RESTORE_DIR.iterdir())
    assert not contents, (
        f"{RESTORE_DIR} should be empty initially, but contains: "
        f"{[str(p) for p in contents]}"
    )