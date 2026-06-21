# test_initial_state.py
#
# This pytest file validates that the **initial** on-disk state expected by the
# exercise is present *before* the student’s solution is executed.  It checks
# that the relevant directories exist, that the uploads directory contains the
# exact files (and only those files) specified in the task description, and
# that their cryptographic hashes as well as the reference databases are
# correct.

import hashlib
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

BASE_DIR = Path("/home/user/investigation")
UPLOADS_DIR = BASE_DIR / "uploads"
REFERENCE_DIR = BASE_DIR / "reference"

EXPECTED_UPLOADS = {
    "safe.txt": {
        "size": 5,
        "md5": "5d41402abc4b2a76b9719d911017c592",
        "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    },
    "malicious.bin": {
        "size": 0,
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    "unknown.dat": {
        "size": 4,
        "md5": "098f6bcd4621d373cade4e832627b4f6",
        "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    },
}

SAFE_REF_FILE = REFERENCE_DIR / "known_safe_hashes.txt"
MALWARE_REF_FILE = REFERENCE_DIR / "known_malware_hashes.txt"


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _hash_file(path: Path, algo_name: str) -> str:
    """
    Compute the hex digest of a file using the requested algorithm.
    Only hashlib algorithms from the stdlib are allowed.
    """
    h = hashlib.new(algo_name)
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    """
    /home/user/investigation/, its uploads/ subdirectory, and the reference/
    subdirectory must exist.
    """
    for directory in (BASE_DIR, UPLOADS_DIR, REFERENCE_DIR):
        assert directory.exists(), f"Expected directory {directory} is missing."
        assert directory.is_dir(), f"{directory} exists but is not a directory."


def test_uploads_contains_expected_files_only():
    """
    The uploads directory must contain *exactly* the files specified in
    EXPECTED_UPLOADS, with no extras.
    """
    present_files = sorted(p.name for p in UPLOADS_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_UPLOADS)
    assert (
        present_files == expected_files
    ), (
        "Mismatch in uploads directory contents.\n"
        f"Expected files: {expected_files}\n"
        f"Found files   : {present_files}"
    )


@pytest.mark.parametrize("filename,meta", EXPECTED_UPLOADS.items())
def test_upload_file_size_and_hashes(filename, meta):
    """
    For every file in uploads/, verify byte-size, MD5, and SHA-256 digests.
    """
    path = UPLOADS_DIR / filename
    assert path.exists(), f"{path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_size = path.stat().st_size
    assert (
        actual_size == meta["size"]
    ), f"{filename}: expected size {meta['size']} bytes, found {actual_size}."

    actual_md5 = _hash_file(path, "md5")
    assert (
        actual_md5 == meta["md5"]
    ), f"{filename}: MD5 mismatch.\nExpected: {meta['md5']}\nFound   : {actual_md5}"

    actual_sha256 = _hash_file(path, "sha256")
    assert (
        actual_sha256 == meta["sha256"]
    ), (
        f"{filename}: SHA-256 mismatch.\n"
        f"Expected: {meta['sha256']}\nFound   : {actual_sha256}"
    )


def test_reference_files_exist():
    """
    Ensure that the reference hash databases are present as regular files.
    """
    for ref_path in (SAFE_REF_FILE, MALWARE_REF_FILE):
        assert ref_path.exists(), f"Reference file {ref_path} is missing."
        assert ref_path.is_file(), f"Reference path {ref_path} exists but is not a file."


def test_reference_files_contain_expected_hashes():
    """
    known_safe_hashes.txt must contain SHA-256 of safe.txt.
    known_malware_hashes.txt must contain SHA-256 of malicious.bin.
    """
    safe_hash_expected = EXPECTED_UPLOADS["safe.txt"]["sha256"]
    malware_hash_expected = EXPECTED_UPLOADS["malicious.bin"]["sha256"]

    safe_hashes = {line.strip() for line in SAFE_REF_FILE.read_text().splitlines() if line.strip()}
    malware_hashes = {line.strip() for line in MALWARE_REF_FILE.read_text().splitlines() if line.strip()}

    assert (
        safe_hash_expected in safe_hashes
    ), f"SHA-256 of safe.txt ({safe_hash_expected}) not found in {SAFE_REF_FILE}"
    assert (
        malware_hash_expected in malware_hashes
    ), f"SHA-256 of malicious.bin ({malware_hash_expected}) not found in {MALWARE_REF_FILE}"