# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “configuration
# tracker” assignment.
#
# These tests assert that:
#   • The mock API directory and its JSON resources exist exactly as
#     specified (no trailing newline, exact bytes).
#   • The target output directory (/home/user/config_tracker) is *not*
#     present yet.
#   • TCP port 8000 is currently free (no HTTP server listening).
#
# If any test fails, the assertion messages describe precisely what is
# missing or unexpectedly present.

import os
import socket
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
MOCK_API_DIR = HOME / "mock_api"
BEFORE_FILE = MOCK_API_DIR / "before.json"
AFTER_FILE = MOCK_API_DIR / "after.json"
CONFIG_TRACKER_DIR = HOME / "config_tracker"

EXPECTED_BEFORE_CONTENT = (
    '{"version":"1.0","settings":{"feature":false}}'
)

EXPECTED_AFTER_CONTENT = (
    '{"version":"2.0","settings":{"feature":true}}'
)


def _read_bytes(path: pathlib.Path) -> bytes:
    """Read a file in binary mode, fail loudly if unreadable."""
    try:
        return path.read_bytes()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


def test_mock_api_directory_exists():
    assert MOCK_API_DIR.exists(), (
        f"Directory {MOCK_API_DIR} is missing; it must be pre-populated."
    )
    assert MOCK_API_DIR.is_dir(), (
        f"{MOCK_API_DIR} exists but is not a directory."
    )


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (BEFORE_FILE, EXPECTED_BEFORE_CONTENT),
        (AFTER_FILE, EXPECTED_AFTER_CONTENT),
    ],
)
def test_mock_api_files_exist_with_exact_content(file_path, expected_content):
    assert file_path.exists(), (
        f"Required file {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )

    data = _read_bytes(file_path)
    # Expect no trailing newline; read as bytes to be strict.
    expected_bytes = expected_content.encode()
    assert (
        data == expected_bytes
    ), (
        f"Contents of {file_path} do not match the expected "
        f"pre-populated JSON.\n"
        f"Expected: {expected_content!r}\n"
        f"Actual:   {data.decode(errors='replace')!r}"
    )


def test_config_tracker_directory_absent_initially():
    assert not CONFIG_TRACKER_DIR.exists(), (
        f"{CONFIG_TRACKER_DIR} should NOT exist before the student runs "
        f"their solution script."
    )


def test_port_8000_is_free():
    """
    Verify that nothing is listening on 127.0.0.1:8000.

    Rather than attempting to `connect` (which could hang), we try to
    bind to the address; if the bind succeeds the port is free.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 8000))
    except OSError:
        pytest.fail(
            "TCP port 8000 is already in use; the HTTP server must NOT be "
            "running at the initial state."
        )
    finally:
        sock.close()