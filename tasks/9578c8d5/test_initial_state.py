# test_initial_state.py
#
# This test-suite validates the pristine state of the filesystem **before**
# the student carries out any actions.  It checks that the expected
# directory and artifact are present, that their contents match the
# specification, and that the supplemental files that the student is
# supposed to create do *not* yet exist.
#
# Only the Python standard library and pytest are used.

import hashlib
import os
import stat
import errno
import pytest

# Canonical paths used throughout the tests
RELEASE_DIR = "/home/user/builds/releases"
BIN_FILE     = os.path.join(RELEASE_DIR, "hello-1.0.0.bin")
SUMS_FILE    = os.path.join(RELEASE_DIR, "SHA256SUMS")
LOG_FILE     = os.path.join(RELEASE_DIR, "checksum_verification.log")

# Ground-truth checksum of the binary (for 5-byte file "hello")
GROUND_TRUTH_SHA256 = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)


@pytest.fixture(scope="module")
def bin_contents():
    """
    Return the raw bytes of the artifact. The fixture will fail with a
    clear error if the file cannot be read.
    """
    if not os.path.exists(BIN_FILE):
        pytest.fail(f"Required artifact missing: {BIN_FILE!r} should exist.")
    if not os.path.isfile(BIN_FILE):
        pytest.fail(f"{BIN_FILE!r} exists but is not a regular file.")
    try:
        with open(BIN_FILE, "rb") as fh:
            return fh.read()
    except OSError as exc:
        pytest.fail(f"Could not read {BIN_FILE!r}: {exc}")


def test_release_directory_exists_and_writable():
    assert os.path.isdir(RELEASE_DIR), (
        f"The directory {RELEASE_DIR!r} must exist."
    )

    # Check write permission for the current real UID
    if not os.access(RELEASE_DIR, os.W_OK):
        st = os.stat(RELEASE_DIR)
        perms = stat.filemode(st.st_mode)
        pytest.fail(
            f"The directory {RELEASE_DIR!r} is not writable by the current user "
            f"(mode {perms})."
        )


def test_hello_bin_exists_and_correct_size(bin_contents):
    expected_size = 5  # bytes
    actual_size = len(bin_contents)
    assert (
        actual_size == expected_size
    ), f"{BIN_FILE!r} should be {expected_size} bytes but is {actual_size} bytes."


def test_hello_bin_contents(bin_contents):
    expected = b"hello"
    assert (
        bin_contents == expected
    ), f"{BIN_FILE!r} should contain the ASCII bytes {expected!r} with NO newline."


def test_hello_bin_sha256(bin_contents):
    sha256 = hashlib.sha256(bin_contents).hexdigest()
    assert (
        sha256 == GROUND_TRUTH_SHA256
    ), (
        f"The SHA-256 of {BIN_FILE!r} is wrong.\n"
        f"Expected: {GROUND_TRUTH_SHA256}\n"
        f"Actual:   {sha256}"
    )


def test_supplementary_files_do_not_exist_yet():
    """
    At the initial state, the checksum metadata must not yet be present.
    """
    missing = []
    for path in (SUMS_FILE, LOG_FILE):
        if os.path.exists(path):
            missing.append(path)
    assert not missing, (
        "Supplementary files should NOT exist before the student runs the task, "
        f"but these were found: {', '.join(missing)}"
    )