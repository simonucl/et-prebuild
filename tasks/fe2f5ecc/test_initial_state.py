# test_initial_state.py
#
# This pytest suite checks the **initial** filesystem state
# before the student starts solving the task.  It verifies
# that only the staging area is present with the expected
# empty files and that no part of the final repository
# already exists.

import hashlib
import os
import stat
import pytest

# Constants -------------------------------------------------------------

HOME               = "/home/user"
STAGING_DIR        = os.path.join(HOME, "temp", "artifacts")
BINARY_REPO_ROOT   = os.path.join(HOME, "binary-repo")

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

STAGING_FILES = [
    "toolA-1.0.bin",
    "toolB-2.5.bin",
    "utilC-0.9.bin",
]

FINAL_DIRS_SHOULD_NOT_EXIST = [
    BINARY_REPO_ROOT,
    os.path.join(BINARY_REPO_ROOT, "tools"),
    os.path.join(BINARY_REPO_ROOT, "utils"),
]

FINAL_FILES_SHOULD_NOT_EXIST = [
    os.path.join(BINARY_REPO_ROOT, "manifest.csv"),
    os.path.join(BINARY_REPO_ROOT, "actions.log"),
    os.path.join(BINARY_REPO_ROOT, "tools", "toolA-1.0.bin"),
    os.path.join(BINARY_REPO_ROOT, "tools", "toolB-2.5.bin"),
    os.path.join(BINARY_REPO_ROOT, "utils", "utilC-0.9.bin"),
]

# Helpers ---------------------------------------------------------------

def sha256_of_file(path: str) -> str:
    """Return the hex‐encoded SHA-256 of the file at *path*."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Tests -----------------------------------------------------------------

def test_staging_directory_exists():
    """The staging directory must exist and be a directory."""
    assert os.path.isdir(STAGING_DIR), (
        f"Required staging directory missing: {STAGING_DIR}"
    )
    # Ensure it is not a symlink to something strange
    st = os.lstat(STAGING_DIR)
    assert stat.S_ISDIR(st.st_mode), (
        f"{STAGING_DIR} exists but is not a directory (mode {oct(st.st_mode)})"
    )

@pytest.mark.parametrize("fname", STAGING_FILES)
def test_staging_files_exist_are_empty_and_correct_digest(fname):
    """Each expected binary must exist, be empty, and match empty SHA-256."""
    fpath = os.path.join(STAGING_DIR, fname)
    assert os.path.isfile(fpath), (
        f"Staging file missing: {fpath}"
    )

    size = os.path.getsize(fpath)
    assert size == 0, (
        f"Staging file {fpath} is expected to be empty (0 bytes) "
        f"but is {size} bytes."
    )

    digest = sha256_of_file(fpath)
    assert digest == EMPTY_SHA256, (
        f"SHA-256 mismatch for {fpath}: expected {EMPTY_SHA256}, got {digest}"
    )

def test_no_final_repository_yet():
    """The final /home/user/binary-repo/ tree must not exist yet."""
    for d in FINAL_DIRS_SHOULD_NOT_EXIST:
        assert not os.path.exists(d), (
            f"Directory {d} should NOT exist before the task is executed."
        )
    for f in FINAL_FILES_SHOULD_NOT_EXIST:
        assert not os.path.exists(f), (
            f"File {f} should NOT exist before the task is executed."
        )