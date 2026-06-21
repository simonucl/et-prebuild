# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any task.  These checks guarantee
# that the exercise starts from the expected clean slate.
#
# The tests assert, among other things, that:
#   • the repository directory and its two binary files already exist;
#   • the binaries have the exact content and size specified;
#   • no manifest nor fetch log has been created yet;
#   • nothing is listening on 127.0.0.1:8080 (the student must start it
#     later).
#
# If any assertion fails, the error messages clearly describe what is
# missing or unexpectedly present.

from pathlib import Path
import socket
import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
ARTIFACT_DIR = HOME / "artifacts"
WIDGET = ARTIFACT_DIR / "widget-1.0.0.bin"
GADGET = ARTIFACT_DIR / "gadget-2.1.3.bin"
MANIFEST = ARTIFACT_DIR / "repository_manifest.log"
FETCH_LOG = HOME / "manifest_fetch.log"

# Expected (filename, expected_bytes)
EXPECTED_BINARIES = [
    (WIDGET, b"WIDGET\n"),
    (GADGET, b"GADGET\n"),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_port_listening(host: str, port: int, timeout: float = 0.3) -> bool:
    """
    Return True iff a TCP connection to (host, port) succeeds.
    We deliberately use a small timeout: if the connection hangs we assume
    nothing is listening.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_artifact_directory_exists_and_is_directory():
    assert ARTIFACT_DIR.exists(), f"Expected directory {ARTIFACT_DIR} to exist."
    assert ARTIFACT_DIR.is_dir(), f"{ARTIFACT_DIR} exists but is not a directory."

    # Basic permission sanity: directory should be world-read-executable (755)
    mode = ARTIFACT_DIR.stat().st_mode
    expected_bits = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
                    stat.S_IRGRP | stat.S_IXGRP | \
                    stat.S_IROTH | stat.S_IXOTH
    assert mode & expected_bits == expected_bits, (
        f"{ARTIFACT_DIR} should have 755-like permissions."
    )


@pytest.mark.parametrize("path, expected_bytes", EXPECTED_BINARIES)
def test_binaries_exist_with_expected_content(path: Path, expected_bytes: bytes):
    assert path.exists(), f"Expected binary {path} to exist."
    assert path.is_file(), f"{path} exists but is not a regular file."

    size = path.stat().st_size
    assert size == len(expected_bytes), (
        f"{path} should be {len(expected_bytes)} bytes, found {size}."
    )

    data = path.read_bytes()
    assert data == expected_bytes, (
        f"Contents of {path} differ from the expected "
        f"{expected_bytes!r}; got {data!r}."
    )


def test_manifest_does_not_yet_exist():
    assert not MANIFEST.exists(), (
        f"{MANIFEST} should NOT exist before the student creates it."
    )


def test_fetch_log_does_not_yet_exist():
    assert not FETCH_LOG.exists(), (
        f"{FETCH_LOG} should NOT exist before the student records the HTTP fetch."
    )


def test_no_process_listening_on_localhost_8080():
    host = "127.0.0.1"
    port = 8080
    assert not _is_port_listening(host, port), (
        f"A process is already listening on {host}:{port}. "
        "The student must start this server as part of the tasks; "
        "the port should be free at the outset."
    )