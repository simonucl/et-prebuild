# test_initial_state.py
#
# Pytest suite that validates the *initial* container state **before**
# the student has performed any actions.  These tests make sure that
# exactly the two static micro-service trees exist and that no diagnostic
# artefacts from the future exercise are already present.

import os
import socket
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
MS_ROOT = HOME / "microservices"
AUTH_DIR = MS_ROOT / "auth"
BILL_DIR = MS_ROOT / "billing"
AUTH_INDEX = AUTH_DIR / "index.html"
BILL_INDEX = BILL_DIR / "index.html"
DIAG_LOG = HOME / "diagnostics" / "network_report.log"


# ----------------------------------------------------------------------
# Helper(s)
# ----------------------------------------------------------------------
def _file_content(path: pathlib.Path) -> str:
    """Return file content as text; raises if file does not exist."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def _port_is_listening(port: int) -> bool:
    """
    Return True iff something is already bound to 127.0.0.1:<port>.
    Nothing should be listening at test time.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_microservice_directories_exist():
    """Both micro-service directories must be present."""
    for path in (AUTH_DIR, BILL_DIR):
        assert path.is_dir(), (
            f"Required directory '{path}' is missing. "
            "The starting filesystem should already contain it."
        )


def test_index_files_exist_with_correct_content():
    """index.html files must exist and contain the expected greeting lines."""
    expected = {
        AUTH_INDEX: "Hello from auth service\n",
        BILL_INDEX: "Hello from billing service\n",
    }
    for path, expected_content in expected.items():
        assert path.is_file(), f"File '{path}' is missing."
        actual = _file_content(path)
        assert (
            actual == expected_content
        ), f"File '{path}' has unexpected content: {actual!r}"


def test_diagnostics_log_absent_initially():
    """
    The diagnostics report must NOT exist before the student runs their
    networking sweep.
    """
    assert not DIAG_LOG.exists(), (
        f"File '{DIAG_LOG}' should not exist yet. "
        "It must be created by the student's solution."
    )


@pytest.mark.parametrize("port", [5001, 5002])
def test_ports_not_listening_initially(port):
    """
    The legacy micro-services should not be running yet; nothing should
    be listening on 127.0.0.1:5001 or :5002.
    """
    assert not _port_is_listening(port), (
        f"Port {port} already has a listener. "
        "No service should be running before the exercise starts."
    )