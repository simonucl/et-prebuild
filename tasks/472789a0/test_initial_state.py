# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state for the “suspicious checksum” exercise.  These tests run **before**
# the learner performs any action and therefore assert the ground-truth
# conditions that must already be in place when the container starts.

import hashlib
import os
import stat
import pytest

HOME = "/home/user"
ARTIFACT_DIR = os.path.join(HOME, "incident_artifacts")
SUSPICIOUS_FILE = os.path.join(ARTIFACT_DIR, "suspicious.bin")
CHECKSUM_LOG = os.path.join(ARTIFACT_DIR, "suspicious_checksum.log")

# Cryptographic ground-truth: SHA-256 of an empty file.
EXPECTED_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def sha256_hex(path, chunk_size=8192):
    """Return the SHA-256 hex digest for `path`."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha.update(chunk)
    return sha.hexdigest()


@pytest.fixture(scope="module")
def suspicious_stat():
    """os.stat_result for the suspicious binary."""
    return os.stat(SUSPICIOUS_FILE)


def test_artifact_directory_exists_and_is_directory():
    assert os.path.exists(
        ARTIFACT_DIR
    ), f"Required directory missing: {ARTIFACT_DIR!r}"
    assert os.path.isdir(
        ARTIFACT_DIR
    ), f"Expected {ARTIFACT_DIR!r} to be a directory, but it is not."


def test_artifact_directory_permissions():
    dir_mode = stat.S_IMODE(os.stat(ARTIFACT_DIR).st_mode)
    # Expect 0o755 but be lenient on group/other write bits as long as owner can read/write.
    assert dir_mode & stat.S_IRUSR, f"{ARTIFACT_DIR!r} is not readable by owner."
    assert dir_mode & stat.S_IWUSR, f"{ARTIFACT_DIR!r} is not writable by owner."
    assert dir_mode & stat.S_IXUSR, f"{ARTIFACT_DIR!r} is not executable by owner."


def test_suspicious_file_exists_and_is_regular(suspicious_stat):
    assert os.path.exists(
        SUSPICIOUS_FILE
    ), f"Required file missing: {SUSPICIOUS_FILE!r}"
    assert stat.S_ISREG(
        suspicious_stat.st_mode
    ), f"Expected {SUSPICIOUS_FILE!r} to be a regular file."


def test_suspicious_file_size_is_zero(suspicious_stat):
    assert (
        suspicious_stat.st_size == 0
    ), f"{SUSPICIOUS_FILE!r} should be zero bytes, found {suspicious_stat.st_size} byte(s)."


def test_suspicious_file_permissions(suspicious_stat):
    mode = stat.S_IMODE(suspicious_stat.st_mode)
    assert mode & stat.S_IRUSR, f"{SUSPICIOUS_FILE!r} is not readable by owner."
    # The file is expected to be read-only for group/others; we do not strictly
    # enforce the numeric value to avoid false negatives across filesystems.


def test_suspicious_file_sha256_matches_ground_truth():
    actual = sha256_hex(SUSPICIOUS_FILE)
    assert (
        actual == EXPECTED_SHA256
    ), f"SHA-256 mismatch for {SUSPICIOUS_FILE!r}: expected {EXPECTED_SHA256}, got {actual}"


def test_checksum_log_not_yet_present():
    assert not os.path.exists(
        CHECKSUM_LOG
    ), f"{CHECKSUM_LOG!r} should NOT exist before the learner starts the task."