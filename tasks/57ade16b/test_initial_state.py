# test_initial_state.py
#
# This PyTest suite validates the *initial* state of the operating system
# and filesystem **before** the student starts working on the task
# “mock_api build-and-publish”.
#
# It checks ONLY the prerequisites that must already be in place:
#   • The mock API directory and both JSON artifacts must exist and contain
#     the expected content.
#   • Nothing should yet be listening on 127.0.0.1:9090 (the student will
#     launch that service later).
#
# IMPORTANT:
#   • We intentionally do *not* test for any output directory or files
#     (e.g. /home/user/build_outputs or artifact_summary.log) because those
#     are products of the student’s work and must not be asserted here.
#   • Only standard-library modules and pytest are used.

import json
import os
import socket
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MOCK_API_DIR = Path("/home/user/mock_api")
ARTIFACTS = {
    "artifactA.json": {
        "artifact": "library-core",
        "version": "1.4.2",
        "checksum": "3b7f3aaf79be67fcb10",
    },
    "artifactB.json": {
        "artifact": "service-api",
        "version": "2.0.0",
        "checksum": "7dcb73d9ce5fa26c881",
    },
}
HOST = "127.0.0.1"
PORT = 9090


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def load_json(path: Path):
    """Load and return JSON from *path*.

    A helpful error is raised if the content cannot be parsed.
    """
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")


def port_is_open(host: str, port: int) -> bool:
    """Return True if *host*:*port* is accepting TCP connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_mock_api_directory_exists():
    assert MOCK_API_DIR.is_dir(), (
        f"Directory {MOCK_API_DIR} must exist with the two JSON artifacts."
    )


@pytest.mark.parametrize("filename, expected_payload", ARTIFACTS.items())
def test_artifact_file_exists_and_content(filename, expected_payload):
    file_path = MOCK_API_DIR / filename
    assert file_path.is_file(), f"Missing artifact file: {file_path}"

    data = load_json(file_path)

    # Verify that all required keys are present
    for key in ("artifact", "version", "checksum"):
        assert key in data, f'Key "{key}" missing in {file_path}'

    # Verify exact expected content
    assert data == expected_payload, (
        f"Content mismatch in {file_path}.\n"
        f"Expected: {expected_payload}\n"
        f"Found:    {data}"
    )


def test_port_9090_not_yet_in_use():
    assert not port_is_open(HOST, PORT), (
        f"Nothing should be listening on {HOST}:{PORT} before the student starts. "
        "Port is already in use."
    )