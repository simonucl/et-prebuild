# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student runs any commands.  These tests assert the exact initial
# conditions described in the task specification.
#
# Only the Python standard library and pytest are used.

import os
import hashlib
import stat
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants – absolute, canonical paths that must already exist on disk
# ---------------------------------------------------------------------------
CONFIG_FILE      = Path("/home/user/configs/nginx.conf")
CHECKSUMS_FILE   = Path("/home/user/checksums.txt")
LOGS_DIR         = Path("/home/user/logs")
LOG_FILE         = LOGS_DIR / "nginx_checksum.log"

# The well-known SHA-256 of an empty file (i.e. the empty byte string b"")
EMPTY_FILE_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

# The *exact* single line that must appear in /home/user/checksums.txt
EXPECTED_CHECKSUM_LINE = (
    f"{EMPTY_FILE_SHA256}  {CONFIG_FILE.as_posix()}"
)  # Note TWO spaces before the path


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------
def sha256_of_file(path: Path) -> str:
    """
    Return the hexadecimal SHA-256 digest of the file at *path*.
    """
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_nginx_conf_exists_and_is_empty():
    assert CONFIG_FILE.exists(), (
        "Required file '/home/user/configs/nginx.conf' is missing."
    )
    assert CONFIG_FILE.is_file(), (
        "'/home/user/configs/nginx.conf' exists but is not a regular file."
    )
    size = CONFIG_FILE.stat().st_size
    assert size == 0, (
        f"'/home/user/configs/nginx.conf' should be empty (0 bytes) but is "
        f"{size} bytes."
    )
    actual_hash = sha256_of_file(CONFIG_FILE)
    assert actual_hash == EMPTY_FILE_SHA256, (
        "Checksum of '/home/user/configs/nginx.conf' does not match the "
        "expected SHA-256 for an empty file."
    )


def test_checksums_file_contents():
    assert CHECKSUMS_FILE.exists(), (
        "Reference checksum file '/home/user/checksums.txt' is missing."
    )
    assert CHECKSUMS_FILE.is_file(), (
        "'/home/user/checksums.txt' exists but is not a regular file."
    )

    contents = CHECKSUMS_FILE.read_text(encoding="utf-8")
    lines = contents.splitlines()
    assert len(lines) == 1, (
        f"'/home/user/checksums.txt' must contain exactly one line, "
        f"found {len(lines)}."
    )

    actual_line = lines[0]
    assert actual_line == EXPECTED_CHECKSUM_LINE, (
        "Contents of '/home/user/checksums.txt' are incorrect.\n"
        f"Expected exactly:\n  {EXPECTED_CHECKSUM_LINE!r}\n"
        f"But found:\n  {actual_line!r}"
    )


def test_logs_directory_exists_and_is_writable():
    assert LOGS_DIR.exists(), (
        "Log directory '/home/user/logs/' is missing."
    )
    assert LOGS_DIR.is_dir(), (
        "'/home/user/logs/' exists but is not a directory."
    )

    # Check write permission for the current user
    is_writable = os.access(LOGS_DIR, os.W_OK)
    assert is_writable, (
        "Directory '/home/user/logs/' is not writable by the current user."
    )

    # In addition to os.access, verify mode bits allow user write
    mode = LOGS_DIR.stat().st_mode
    assert bool(mode & stat.S_IWUSR), (
        "Directory '/home/user/logs/' does not have the user-write bit set."
    )


def test_checksum_log_file_does_not_yet_exist():
    assert not LOG_FILE.exists(), (
        "Log file '/home/user/logs/nginx_checksum.log' should NOT exist "
        "before the student runs their verification command."
    )