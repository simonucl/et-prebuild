# test_initial_state.py
#
# Pytest suite that validates the ORIGINAL on-disk state
# prior to the student’s solution being executed.
#
# It checks that:
#   • the /home/user/incidents/ directory exists and has the correct permissions
#   • the two hot-fix payloads are present with the exact byte content expected
#   • the two vendor-supplied “*.sha256” files are present and well-formed
#   • no checksum_report.log file exists yet
#
# Only Python’s standard library and pytest are used.

import os
import stat
import hashlib
import pytest

INCIDENT_DIR = "/home/user/incidents"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_bytes(path):
    """Read a file in binary mode and return its raw bytes."""
    with open(path, "rb") as fh:
        return fh.read()

def _read_text(path):
    """Read a file in text mode (UTF-8) and return its text."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_exists_and_permissions():
    assert os.path.isdir(INCIDENT_DIR), (
        f"Required directory {INCIDENT_DIR!r} is missing."
    )

    mode = os.stat(INCIDENT_DIR).st_mode & 0o777
    expected_mode = 0o700
    assert mode == expected_mode, (
        f"Directory {INCIDENT_DIR} must have permissions "
        f"{oct(expected_mode)}, found {oct(mode)}."
    )

@pytest.mark.parametrize(
    "filename, expected_bytes",
    [
        ("update1.txt", b"test"),  # length 4, no newline
        ("update2.txt", b"abc"),   # length 3, no newline
    ],
)
def test_payload_files_exist_and_contents(filename, expected_bytes):
    path = os.path.join(INCIDENT_DIR, filename)
    assert os.path.isfile(path), f"Payload file {path!r} is missing."

    data = _read_bytes(path)
    assert data == expected_bytes, (
        f"Incorrect content in {path}. "
        f"Expected {expected_bytes!r} (hex: {expected_bytes.hex()}), "
        f"but got {data!r} (hex: {data.hex()})."
    )

@pytest.mark.parametrize(
    "payload, expected_hash",
    [
        (
            "update1.txt",
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        ),
        (
            "update2.txt",
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",  # intentionally wrong
        ),
    ],
)
def test_sha256_sidecar_files(payload, expected_hash):
    """
    Validate that the '*.sha256' files exist, end with a single NL,
    and contain exactly two whitespace-separated fields:

        <hash>  <filename>\n

    The first field must match `expected_hash` from the truth table,
    the second field must be the bare payload filename.
    """
    sidecar = os.path.join(INCIDENT_DIR, f"{payload}.sha256")
    assert os.path.isfile(sidecar), f"Checksum sidecar {sidecar!r} is missing."

    text = _read_text(sidecar)
    assert text.endswith("\n"), f"{sidecar} must end with a single newline."

    stripped = text.rstrip("\n")
    parts = stripped.split()

    assert len(parts) == 2, (
        f"{sidecar} must have exactly two whitespace-separated fields "
        f"(<hash> and <filename>). Got: {parts}"
    )

    hash_field, file_field = parts
    assert (
        hash_field == expected_hash
    ), f"{sidecar} contains wrong hash. Expected {expected_hash}, got {hash_field}."

    assert (
        file_field == payload
    ), f"{sidecar} contains wrong filename. Expected {payload}, got {file_field}."

def test_no_report_file_yet():
    """
    The verification log must NOT exist before the student runs their solution.
    """
    report_path = os.path.join(INCIDENT_DIR, "checksum_report.log")
    assert not os.path.exists(report_path), (
        f"{report_path} should NOT exist in the initial state."
    )