# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# BEFORE the student performs any action for the “checksums” task.
#
# It asserts that:
#   1. /home/user/docs exists and is a directory.
#   2. /home/user/docs/manual_v1.2.pdf exists, is a regular file, and is empty.
#   3. The checksums directory (/home/user/docs/checksums) does NOT yet exist.
#   4. The checksum log file (/home/user/docs/checksums/sha256sum.txt) does NOT yet exist.
#
# If any of these conditions is not met, the student is starting from an
# unexpected state and the test will fail with a clear explanation.
#
# Only Python’s standard library and pytest are used, as required.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
DOCS_DIR = HOME / "docs"
PDF_FILE = DOCS_DIR / "manual_v1.2.pdf"
CHECKSUMS_DIR = DOCS_DIR / "checksums"
CHECKSUM_FILE = CHECKSUMS_DIR / "sha256sum.txt"


def _assert_has_permissions(path: Path, expected_bits: int) -> None:
    """
    Assert that `path` has at least the permission bits in `expected_bits`
    set for the owner (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR, etc.).

    This is a helper that avoids false positives on platforms that mask modes
    (e.g. Windows).  It only checks that the *owner* bits include the expected
    permissions; group / other bits are not enforced.
    """
    st_mode = path.stat().st_mode
    if (st_mode & expected_bits) != expected_bits:
        human = stat.filemode(st_mode)
        needed = stat.filemode(expected_bits | 0o600)  # readable depiction
        pytest.fail(
            f"Path {path} exists but lacks required permissions: "
            f"has {human}, needs owner bits >= {needed}"
        )


def test_docs_directory_exists_and_is_directory():
    assert DOCS_DIR.exists(), (
        f"The directory {DOCS_DIR} is expected to exist before you start "
        f"but was not found."
    )
    assert DOCS_DIR.is_dir(), f"{DOCS_DIR} exists but is not a directory."
    # Expect owner to have at least rwx (octal 700) on the directory
    _assert_has_permissions(DOCS_DIR, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


def test_pdf_placeholder_exists_and_is_empty():
    assert PDF_FILE.exists(), (
        f"The placeholder file {PDF_FILE} is expected to exist before you "
        f"start but was not found."
    )
    assert PDF_FILE.is_file(), f"{PDF_FILE} exists but is not a regular file."
    size = PDF_FILE.stat().st_size
    assert size == 0, (
        f"The placeholder PDF {PDF_FILE} should be empty (0 bytes) "
        f"but its size is {size} bytes."
    )
    # Expect owner to have at least rw (octal 600) on the file
    _assert_has_permissions(PDF_FILE, stat.S_IRUSR | stat.S_IWUSR)


def test_checksums_directory_does_not_yet_exist():
    assert not CHECKSUMS_DIR.exists(), (
        f"The directory {CHECKSUMS_DIR} should NOT exist before you run the "
        f"task, but it is already present."
    )


def test_checksum_file_does_not_yet_exist():
    assert not CHECKSUM_FILE.exists(), (
        f"The file {CHECKSUM_FILE} should NOT exist before you run the task, "
        f"but it is already present."
    )