# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “SHA-256 compliance audit” exercise.
#
# The following **must** already be present *before* the student starts:
#   • /home/user/audit_samples/archive1.tar.gz
#   • /home/user/audit_samples/config.cfg
#   • /home/user/audit_samples/script.sh
#   • /home/user/audit_samples/reference.sha256
#
# Nothing else is checked here (especially **not** any output artefacts),
# so that the student can freely create them later on.

import hashlib
import os
import pathlib
import pytest


SAMPLE_DIR = pathlib.Path("/home/user/audit_samples")
REFERENCE_FILE = SAMPLE_DIR / "reference.sha256"

EXPECTED_REFERENCE_CONTENT = {
    "archive1.tar.gz": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "config.cfg":      "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "script.sh":       "0000000000000000000000000000000000000000000000000000000000000000",
}

SAMPLE_FILES = [SAMPLE_DIR / fname for fname in EXPECTED_REFERENCE_CONTENT]


@pytest.mark.parametrize("path", SAMPLE_FILES)
def test_sample_files_exist(path):
    """
    Ensure each vendor-supplied sample file is present.
    """
    assert path.is_file(), f"Required sample file missing: {path}"


def test_reference_file_exists():
    """
    Ensure the vendor-supplied reference checksum list is present.
    """
    assert REFERENCE_FILE.is_file(), f"Reference checksum file missing: {REFERENCE_FILE}"


def test_reference_file_contents():
    """
    Verify that /home/user/audit_samples/reference.sha256 contains exactly the
    expected three lines in the standard “<hash><two_spaces><filename>” format.
    """
    with REFERENCE_FILE.open("rt", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # Helpful failure if the line count is wrong
    assert len(lines) == 3, (
        f"reference.sha256 should contain exactly 3 lines, found {len(lines)}"
    )

    parsed = {}
    for ln in lines:
        # split() collapses any amount of whitespace, which covers both single
        # and double-space separation.
        parts = ln.split()
        assert len(parts) == 2, (
            "Malformed line in reference.sha256 "
            f"(expected '<hash><space><space><filename>'): '{ln}'"
        )
        digest, filename = parts
        parsed[filename] = digest.lower()

    # Ensure every expected filename is present with the precise digest
    for fname, expected_digest in EXPECTED_REFERENCE_CONTENT.items():
        assert fname in parsed, (
            f"File '{fname}' missing from reference.sha256"
        )
        assert parsed[fname] == expected_digest, (
            f"Digest for '{fname}' in reference.sha256 is "
            f"'{parsed[fname]}' but expected '{expected_digest}'"
        )


def _sha256_hex(path: pathlib.Path) -> str:
    """
    Return the hexadecimal SHA-256 digest of the given file.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_actual_vs_reference_digests():
    """
    Confirm that the real digests of the supplied files match (or deliberately
    do *not* match) the vendor reference list as described in the task
    statement.

    Expected relationship:
      • archive1.tar.gz : digest SHOULD match reference (OK)
      • config.cfg      : digest SHOULD match reference (OK)
      • script.sh       : digest SHOULD NOT match reference (FAIL)
    """
    for path in SAMPLE_FILES:
        fname = path.name
        actual = _sha256_hex(path)
        reference = EXPECTED_REFERENCE_CONTENT[fname]

        if fname == "script.sh":
            assert actual != reference, (
                "For test-setup purposes, script.sh is supposed to have a "
                "non-matching digest, but it unexpectedly MATCHES."
            )
        else:
            assert actual == reference, (
                f"Digest mismatch for {fname}: expected {reference}, got {actual}"
            )