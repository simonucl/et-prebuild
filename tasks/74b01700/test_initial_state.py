# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state
# before the student carries out the exercise.
#
# DO NOT MODIFY.

import hashlib
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

HOME_DIR = Path("/home/user")
LOG_FILE = HOME_DIR / "logs" / "user_mgmt.log"
OUTPUT_DIR = HOME_DIR / "output"

# Exact contents of /home/user/logs/user_mgmt.log (must end with a newline)
EXPECTED_LOG_CONTENT = (
    "[2023-09-30 23:59:59] INFO system: ADD user=alice id=1001\n"
    "[2023-10-01 00:00:01] INFO system: ADD user=bob id=1002\n"
    "[2023-10-05 12:34:56] INFO system: DEL user=charlie id=1003\n"
    "[2023-10-15 08:00:00] INFO system: ADD user=david id=1004\n"
    "[2023-10-20 14:15:30] INFO system: DEL user=alice id=1001\n"
    "[2023-10-31 23:59:59] INFO system: ADD user=erin id=1005\n"
    "[2023-11-01 00:00:01] INFO system: ADD user=frank id=1006\n"
)

EXPECTED_LOG_SHA256 = hashlib.sha256(EXPECTED_LOG_CONTENT.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def sha256_of_file(path: Path) -> str:
    """Return the SHA-256 hex digest of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_log_file_exists():
    """The raw log file must exist at the exact path and be a regular file."""
    assert LOG_FILE.exists(), f"Expected log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_contents_are_exact():
    """
    The log file must match the expected byte-for-byte contents, including the
    trailing newline.  Any deviation will cause the subsequent processing
    instructions to be incorrect.
    """
    file_hash = sha256_of_file(LOG_FILE)
    assert (
        file_hash == EXPECTED_LOG_SHA256
    ), (
        "The contents of /home/user/logs/user_mgmt.log do not match the expected "
        "initial state.  Ensure no one has modified the file."
    )

    # Extra paranoia: confirm the file ends with a single newline
    with LOG_FILE.open("rb") as fh:
        data = fh.read()
        assert data.endswith(b"\n"), (
            f"{LOG_FILE} must end with exactly one trailing newline."
        )


def test_output_directory_absent():
    """
    The /home/user/output directory should **not** exist yet.  The student
    will create it during their solution.  If the directory is already present,
    it might indicate the environment has been used before.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} already exists, but the initial state should "
        "not contain it."
    )


def test_no_preexisting_output_files():
    """
    No files related to the forthcoming task should be present anywhere in the
    home tree.  We look for any path that contains the pattern
    'oct2023_user_changes' in its name.
    """
    offending_paths = []
    for root, _dirs, files in os.walk(HOME_DIR):
        for fname in files:
            if "oct2023_user_changes" in fname:
                offending_paths.append(Path(root) / fname)

    assert (
        not offending_paths
    ), (
        "Found unexpected pre-existing output files:\n"
        + "\n".join(str(p) for p in offending_paths)
    )