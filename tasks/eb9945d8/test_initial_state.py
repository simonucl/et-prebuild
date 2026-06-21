# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any actions for the “uptime checksum”
# exercise.  It checks that the required directories, files, file
# contents, digests, and checksum reference file are all present and
# correct.

import hashlib
import os
from pathlib import Path
import re

# Hard-coded paths used throughout the test suite.
MONITORING_DIR = Path("/home/user/monitoring")
RAW_LOGS_DIR = MONITORING_DIR / "raw_logs"
CHECKSUM_FILE = MONITORING_DIR / "checksums.sha256"

RAW_FILES_EXPECTED = {
    "node_a_uptime.log": b"hello",   # no trailing newline
    "node_b_uptime.log": b"abc",     # no trailing newline
    "node_c_uptime.log": b"foo",     # no trailing newline
}

EXPECTED_CHECKSUMS = {
    "raw_logs/node_a_uptime.log": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    "raw_logs/node_b_uptime.log": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "raw_logs/node_c_uptime.log": "0000000000000000000000000000000000000000000000000000000000000000",
}


def sha256_digest(data: bytes) -> str:
    """Return the hexadecimal SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def test_required_directories_exist():
    """Verify that /home/user/monitoring and its raw_logs subdir exist."""
    assert MONITORING_DIR.is_dir(), (
        f"Missing directory: {MONITORING_DIR}"
    )
    assert RAW_LOGS_DIR.is_dir(), (
        f"Missing directory: {RAW_LOGS_DIR}"
    )


def test_raw_log_files_present_with_exact_contents_and_no_trailing_newline():
    """
    Ensure each raw log file exists, has the expected exact ASCII content,
    and does NOT end with a newline.
    """
    for filename, expected_bytes in RAW_FILES_EXPECTED.items():
        file_path = RAW_LOGS_DIR / filename
        assert file_path.is_file(), f"Missing raw log file: {file_path}"

        data = file_path.read_bytes()
        assert data == expected_bytes, (
            f"Content mismatch in {file_path}. "
            f"Expected {expected_bytes!r} but got {data!r}"
        )

        # Verify there is no trailing newline character in the file
        assert not data.endswith(b"\n"), (
            f"{file_path} should not end with a newline character"
        )


def test_sha256_digests_of_raw_logs_are_correct():
    """Recalculate SHA-256 digests and make sure they match expectations."""
    for rel_path, expected_hex in EXPECTED_CHECKSUMS.items():
        # We only want to verify the *actual* digests for the real files,
        # i.e. non-zero expected hashes for node_a and node_b.  For node_c
        # we still compute for completeness and compare to its correct value
        # (which is *not* all zeroes).
        file_path = MONITORING_DIR / rel_path
        # Guard: the mapping above uses forward slashes, Path will normalise.
        assert file_path.is_file(), f"Missing raw log file for digest check: {file_path}"
        actual_hex = sha256_digest(file_path.read_bytes())

        # Derive the *true* expected digest for validation:
        true_expected_hex = {
            "raw_logs/node_a_uptime.log": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            "raw_logs/node_b_uptime.log": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            "raw_logs/node_c_uptime.log": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
        }[rel_path]

        assert actual_hex == true_expected_hex, (
            f"SHA-256 mismatch for {file_path}.\n"
            f"Expected: {true_expected_hex}\n"
            f"Actual:   {actual_hex}"
        )


def test_checksum_reference_file_exists_and_has_correct_format_and_values():
    """Validate /home/user/monitoring/checksums.sha256 content and format."""
    assert CHECKSUM_FILE.is_file(), f"Missing checksum reference file: {CHECKSUM_FILE}"

    lines = CHECKSUM_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    assert len(lines) == 3, (
        f"{CHECKSUM_FILE} should contain exactly 3 lines, found {len(lines)}"
    )

    # Regular expression for a valid line:
    # 64 hex chars, two spaces, raw_logs/..., newline
    line_re = re.compile(
        r"^(?P<hash>[0-9a-f]{64})  (?P<relpath>raw_logs/[^\n\r]+)\n$"
    )

    for i, line in enumerate(lines, 1):
        m = line_re.match(line)
        assert m, (
            f"Line {i} in {CHECKSUM_FILE} is incorrectly formatted:\n{line!r}\n"
            "Expected: 64 lowercase hex chars, two spaces, relative path, newline"
        )
        rel_path = m.group("relpath")
        reported_hash = m.group("hash")
        expected_hash = EXPECTED_CHECKSUMS.get(rel_path)
        assert expected_hash is not None, (
            f"Unexpected relative path '{rel_path}' on line {i} of {CHECKSUM_FILE}"
        )
        assert reported_hash == expected_hash, (
            f"Hash mismatch on line {i} of {CHECKSUM_FILE} for {rel_path}.\n"
            f"Expected hash in reference file: {expected_hash}\n"
            f"Found:                          {reported_hash}"
        )