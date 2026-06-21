# test_initial_state.py
#
# This test-suite asserts the *initial* filesystem state that must be
# present **before** the student starts working on the task described
# in the prompt.  It verifies that the three legacy configuration files
# are in place, still encoded in Windows-1252, still using CRLF line
# endings, and still contain the expected textual payload and byte
# sizes.  No output / artefact files or directories are tested here.

import os
import pytest

BASE_DIR = "/home/user/project/config"

# Mapping: filename -> (expected_byte_size, expected_text_lines)
EXPECTED_FILES = {
    "build.cfg": (
        64,
        [
            "project_name=AwesomeApp",
            "version=1.2.3",
            "maintainer=DevOps Team",
        ],
    ),
    "deploy.cfg": (
        52,
        [
            "deploy_env=production",
            "servers=5",
            "strategy=rolling",
        ],
    ),
    "test.cfg": (
        44,
        [
            "tests_enabled=true",
            "timeout=300",
            "retries=2",
        ],
    ),
}


@pytest.mark.parametrize("filename, meta", EXPECTED_FILES.items())
def test_file_exists_and_size(filename, meta):
    """
    Ensure each expected .cfg file exists as a regular file and has
    the exact byte size that the exercise specifies.
    """
    expected_size, _ = meta
    abs_path = os.path.join(BASE_DIR, filename)

    assert os.path.isfile(
        abs_path
    ), f"Required file missing: {abs_path!r}"

    actual_size = os.path.getsize(abs_path)
    assert (
        actual_size == expected_size
    ), f"{abs_path!r} has size {actual_size}, expected {expected_size} bytes."


@pytest.mark.parametrize("filename, meta", EXPECTED_FILES.items())
def test_file_encoding_and_content(filename, meta):
    """
    Verify that each file:
      • contains CRLF line endings (0x0D 0x0A)
      • decodes cleanly with Windows-1252
      • has the exact textual lines specified in the prompt
      • does *not* contain lone LF characters
    """
    expected_size, expected_lines = meta
    abs_path = os.path.join(BASE_DIR, filename)

    # Read the raw bytes once for multiple checks
    with open(abs_path, "rb") as fh:
        raw = fh.read()

    # --- Line-ending checks ------------------------------------------------
    assert b"\r\n" in raw, f"{abs_path!r} does not appear to use CRLF endings."
    assert b"\n" in raw, "No LF bytes found at all—unexpected."
    # Ensure there are no lone '\n' characters (LF not preceded by CR)
    lone_lf_positions = [
        idx
        for idx in range(len(raw))
        if raw[idx : idx + 1] == b"\n" and raw[idx - 1 : idx] != b"\r"
    ]
    assert (
        not lone_lf_positions
    ), f"{abs_path!r} contains {len(lone_lf_positions)} lone LF characters; should be pure CRLF."

    # File should end with CRLF (trailing newline)
    assert raw.endswith(
        b"\r\n"
    ), f"{abs_path!r} is expected to end with a CRLF sequence."

    # --- Encoding & textual content checks --------------------------------
    try:
        text = raw.decode("cp1252")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{abs_path!r} is not valid Windows-1252: {exc}")

    # Round-trip sanity: encoding back to cp1252 should reproduce raw bytes
    assert text.encode("cp1252") == raw, (
        f"Re-encoding {abs_path!r} to Windows-1252 fails to reproduce "
        "original bytes — file may have been modified."
    )

    # Split lines *without* keeping line endings
    actual_lines = text.rstrip("\r\n").split("\r\n")
    assert (
        actual_lines == expected_lines
    ), f"Content mismatch in {abs_path!r}.\nExpected lines: {expected_lines}\nActual lines:   {actual_lines}"

    # Finally, double-check byte size again (safety net)
    assert len(raw) == expected_size, (
        f"Byte-size check failed for {abs_path!r}: "
        f"{len(raw)} bytes on disk, expected {expected_size}."
    )